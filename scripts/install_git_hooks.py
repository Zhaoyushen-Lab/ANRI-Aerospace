"""安装本地 git 钩子：提交前自动执行识别性信息扫描。

钩子文件写在 .git/hooks/ 下，属本地配置，不进版本库。
本安装脚本本身可以进版本库，因为下一次 clone 的人也能一键装上。

用法：
    py -3 scripts/install_git_hooks.py
    py -3 scripts/install_git_hooks.py --uninstall
"""

from __future__ import annotations

import argparse
import pathlib
import stat
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOOK = ROOT / ".git" / "hooks" / "pre-commit"

HOOK_BODY = """#!/bin/sh
# 由 scripts/install_git_hooks.py 安装。
# 提交前扫描暂存区，命中 BLOCK 级识别性词则阻止提交。
# 绕过方式：git commit --no-verify（应仅在你确认内容可公开时使用）

cd "$(git rev-parse --show-toplevel)" || exit 1

if command -v py >/dev/null 2>&1; then
    PY=py
elif command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi

$PY -3 scripts/scan_identifiers.py --staged
status=$?

if [ $status -ne 0 ]; then
    echo ""
    echo "  提交被拒绝：暂存区含 BLOCK 级识别性词。"
    echo "  处置见 D-ANRI-013 §10。确认内容可公开时才用 --no-verify 绕过。"
    echo ""
fi

exit $status
"""


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--uninstall", action="store_true")
    args = ap.parse_args()

    if not (ROOT / ".git").is_dir():
        print("  失败：当前目录不是 git 仓库根。")
        return 1

    if args.uninstall:
        if HOOK.exists():
            HOOK.unlink()
            print(f"  已移除 {HOOK.relative_to(ROOT)}")
        else:
            print("  钩子不存在。")
        return 0

    HOOK.parent.mkdir(parents=True, exist_ok=True)
    HOOK.write_bytes(HOOK_BODY.encode("utf-8"))
    HOOK.chmod(HOOK.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    print(f"  已安装 {HOOK.relative_to(ROOT)}")
    print()
    print("  验证方式：制造一次带识别性词的暂存，确认提交被拒绝。")
    print("  移除方式：py -3 scripts/install_git_hooks.py --uninstall")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
