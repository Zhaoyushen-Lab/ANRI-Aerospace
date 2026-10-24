"""公开前的识别性信息扫描器。

设计约束（很重要）：
    本脚本本身是公开的，因此**不得硬编码任何识别性词**。
    识别性词表放在 `.private-terms.txt`，该文件被 .gitignore 排除，只存在于本地。

    若词表文件未被 gitignore，脚本拒绝运行——因为那样它随时可能被提交。

用法：
    py -3 scripts/scan_identifiers.py              # 扫描全部被 git 跟踪的文件
    py -3 scripts/scan_identifiers.py --staged     # 只扫描暂存区（pre-commit 钩子用）
    py -3 scripts/scan_identifiers.py --history    # 扫描提交信息（只报告，不阻断）
    py -3 scripts/scan_identifiers.py --summary    # 只打印暴露面统计

退出码：
    0  无 BLOCK 级命中
    1  存在 BLOCK 级命中
    2  配置或环境问题（如词表未被忽略）
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TERMS_FILE = ROOT / ".private-terms.txt"

# 结构性检查：与具体项目无关，因此可以公开写在这里
#
# 两条正则都踩过坑，写在这里备查：
#   A1 最初写成 r"[A-Za-z]:\\\\Users\\\\"，在原始字符串里那是「两个反斜杠」，
#      永远匹配不到 C:\Users\；而 /home/[^/\s]+/ 又会命中散文里的
#      "drive/UNC/home/`file://`"。两条都收紧到真实路径形态。
#   A3 不能只是 18 位数字：CSV 里的小数动辄十几位有效数字，
#      单纯的 \d{18} 会把 0.24225000000000002 判成身份证号（实测误报 5 万余处）。
#      真正的身份证号第 7–14 位必须是合法日期。
STRUCTURAL = [
    ("A1_绝对路径",
     re.compile(r"(?<![A-Za-z])[A-Za-z]:\\Users\\[A-Za-z0-9_.-]+"
                r"|(?<![\w/])/home/[A-Za-z0-9_.-]+/"),
     "warn"),
    ("A2_手机号",
     re.compile(r"(?<![0-9A-Za-z])1[3-9]\d{9}(?![0-9A-Za-z])"),
     "block"),
    ("A3_身份证号",
     re.compile(r"(?<![0-9A-Za-z])[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])"
                r"(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?![0-9A-Za-z])"),
     "block"),
    ("A4_邮箱", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "warn"),
]

# 行内豁免：同一行出现这个标记就跳过该行的全部检查。
# 用于确实需要写出「坏例子」的场合——例如验证器自测里的合成绝对路径。
SUPPRESS_MARK = "scan:ignore"

TEXT_SUFFIXES = {
    ".md", ".py", ".json", ".yaml", ".yml", ".txt", ".csv", ".toml",
    ".cfg", ".ini", ".sh", ".ps1", ".cff", ".bib", ".tex",
}


def mask(term: str) -> str:
    """把命中词遮蔽，避免报告本身再次泄露它。"""
    if len(term) <= 1:
        return "*"
    if len(term) == 2:
        return term[0] + "*"
    return term[0] + "*" * (len(term) - 2) + term[-1]


def load_terms() -> list[tuple[str, str]]:
    """读取词表，返回 [(词, 级别)]。缺失时返回空表并警告。"""
    if not TERMS_FILE.exists():
        print(f"  ⚠️  未找到词表 {TERMS_FILE.name}，仅执行结构性检查。")
        print("     要启用识别性词检查，请创建该文件（格式见脚本末尾说明）。")
        print()
        return []

    # 关键安全检查：词表本身必须被忽略
    proc = subprocess.run(
        ["git", "check-ignore", "-q", str(TERMS_FILE)],
        cwd=ROOT, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        print("=" * 72)
        print("  拒绝运行：词表没有被 .gitignore 排除。")
        print()
        print(f"  {TERMS_FILE.name} 含有识别性词，一旦被提交就等于公开。")
        print("  请先把该文件名加入 .gitignore，再重试。")
        print("=" * 72)
        raise SystemExit(2)

    terms: list[tuple[str, str]] = []
    for raw in TERMS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            term, level = (s.strip() for s in line.split("|", 1))
        else:
            term, level = line, "block"
        if term:
            terms.append((term, level.lower()))
    return terms


def tracked_files() -> list[pathlib.Path]:
    proc = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    return [ROOT / p for p in proc.stdout.splitlines() if p.strip()]


def staged_files() -> list[pathlib.Path]:
    proc = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    return [ROOT / p for p in proc.stdout.splitlines() if p.strip()]


def scan_files(paths: list[pathlib.Path], terms: list[tuple[str, str]]) -> list[dict]:
    hits: list[dict] = []
    for path in paths:
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()

        # P2：路径本身命中
        for term, level in terms:
            if term in rel:
                hits.append({"kind": "P2_路径", "level": level, "file": rel,
                             "line": 0, "shown": mask(term), "text": ""})

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for lineno, line in enumerate(content.splitlines(), 1):
            if SUPPRESS_MARK in line:
                continue
            for term, level in terms:
                if term in line:
                    hits.append({"kind": "P1_词表", "level": level, "file": rel,
                                 "line": lineno, "shown": mask(term),
                                 "text": line.strip()[:70]})
            for name, pattern, level in STRUCTURAL:
                if pattern.search(line):
                    hits.append({"kind": name, "level": level, "file": rel,
                                 "line": lineno, "shown": name,
                                 "text": line.strip()[:70]})
    return hits


def scan_history(terms: list[tuple[str, str]]) -> list[dict]:
    proc = subprocess.run(
        ["git", "log", "--format=%H%x09%s"], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    hits: list[dict] = []
    for row in proc.stdout.splitlines():
        if "\t" not in row:
            continue
        sha, subject = row.split("\t", 1)
        for term, level in terms:
            if term in subject:
                hits.append({"kind": "H1_提交信息", "level": level, "file": sha[:10],
                             "line": 0, "shown": mask(term), "text": subject[:70]})
    return hits


def report(hits: list[dict], title: str) -> int:
    blocks = [h for h in hits if h["level"] == "block"]
    warns = [h for h in hits if h["level"] != "block"]

    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)
    print()

    if not hits:
        print("  无命中。")
        print()
        return 0

    for group, label in ((blocks, "BLOCK"), (warns, "WARN")):
        if not group:
            continue
        print(f"  [{label}] {len(group)} 处")
        print()
        for h in group[:40]:
            loc = f"{h['file']}:{h['line']}" if h["line"] else h["file"]
            print(f"    {h['kind']}  {h['shown']}   {loc}")
            if h["text"]:
                print(f"        {h['text']}")
        if len(group) > 40:
            print(f"    …… 另有 {len(group) - 40} 处")
        print()

    print(f"  合计：BLOCK {len(blocks)} 处，WARN {len(warns)} 处")
    print()
    return 1 if blocks else 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--staged", action="store_true", help="只扫描暂存区")
    ap.add_argument("--history", action="store_true", help="扫描提交信息（只报告）")
    ap.add_argument("--summary", action="store_true", help="只打印暴露面统计")
    args = ap.parse_args()

    terms = load_terms()
    print(f"  词表条目：{len(terms)}")
    print()

    if args.history:
        return report(scan_history(terms), "提交信息扫描（不可回溯修改，仅报告）")

    paths = staged_files() if args.staged else tracked_files()
    hits = scan_files(paths, terms)

    if args.summary:
        by_file: dict[str, int] = {}
        for h in hits:
            if h["level"] == "block":
                by_file[h["file"]] = by_file.get(h["file"], 0) + 1
        print("=" * 72)
        print("  暴露面统计（BLOCK 级，按文件）")
        print("=" * 72)
        for f, n in sorted(by_file.items(), key=lambda kv: -kv[1]):
            print(f"    {n:4d}  {f}")
        print()
        print(f"  文件数：{len(by_file)}   命中总数：{sum(by_file.values())}")
        print()
        return 0

    title = "暂存区扫描" if args.staged else f"全仓库扫描（{len(paths)} 个被跟踪文件）"
    code = report(hits, title)

    if code:
        print("  ⚠️  存在 BLOCK 级命中。")
        print()
        print("  处置原则（见 D-ANRI-013 §10）：")
        print("    · 方法与代码 -> 可以公开")
        print("    · 实例与参数 -> 不公开")
        print("    · 单位名 / 人名 / 项目代号 -> 不公开（它们不服务于任何验证目的）")
        print()
        print("  对已有内容：用「某国防院所」「校内导师」一类等义表述替换，")
        print("  并在文档头部注明参数来源为 literature-default。")
    return code


# 词表文件格式（.private-terms.txt，需被 .gitignore 排除）：
#
#   # 注释行
#   <词>|<block 或 warn>
#
#   例：
#   某某研究所|block
#   某某老师|block
#   某项目代号|block
#   某技术方向|warn
#
# 级别含义：
#   block  命中即失败，禁止提交
#   warn   命中仅提示（用于那些在文档中必须被讨论、但不宜出现在代码/数据里的词）

if __name__ == "__main__":
    raise SystemExit(main())
