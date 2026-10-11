# RO-CDFV-001-Ref-01B 独立审阅报告

- **审阅对象**：`RO-CDFV-001-Ref-01B`
- **仓库**：`ANRI-Aerospace`
- **审阅模式**：只读（允许执行清单验证命令，禁止提交/推送）
- **依据清单**：`Reviews/RO-CDFV-001-Ref-01B_Review_Checklist.md`
- **审阅时 HEAD**：`abc91031930943c308edea73a97a120cbd6b8bf5`（`abc9103 Add ANRI research object validation workflow`），分支 `feat/research-object-v0.1`
- **执行环境**：Windows，`core.autocrlf=true`，Python `3.13.14`
- **报告生成**：本文档由审阅方整理，未修改被审仓库的任何文件（被清单命令覆盖的结果文件已恢复）

---

> 归档说明：本文件是独立审阅报告的仓库内冻结副本。报告中引用的本机绝对路径已替换为仓库相对形式或 `<user-home>` 占位符，以符合“不写入本机绝对路径”的要求；判定内容、命令、证据与数值未作任何改动。
> 逐字原件保留在仓库之外，其 SHA-256 记录在 `Research_Objects/RO-CDFV-001-Ref-01B.json` 的 `review.reviews[0].external_source_sha256`。

## Decision

`REQUEST_CHANGES`

---

## Blocking Findings

### F1 — 记录的 7 个 SHA-256 全部对 CRLF 计算，Linux checkout 下 6 个不匹配 — Severity: `BLOCKER`

- **位置**：`Research_Objects/RO-CDFV-001-Ref-01B.json` 的 `artifacts[*].sha256`（第 89、94、99、104、109、114、119 行）；`.gitattributes:1-6`；本机 `core.autocrlf=true`。
- **实际观察**：`git ls-files --eol` 显示这些文件 `i/lf w/crlf`，即索引/仓库内是 LF，工作区被换成 CRLF。字节统计证实：`Models/CDFV-001/Ref-01B/baseline_model.py` 工作区 CR=319/LF=319，索引内容 CR=0/LF=319。Windows 工作区 `Get-FileHash` 与 RO 记录 **7/7 一致**；索引内容（= Linux fresh checkout 的字节）只有 `verify_baseline.py` **1/7 一致**。把索引内容导出成树后运行 `validate_research_object.py --repo-root <LF树>`，退出码 1，报出 6 条 `sha256 mismatch`。
- **影响**：`.github/workflows/anri-validation.yml:9` 是 `runs-on: ubuntu-latest`，其第 16 步正是该校验器。**该分支推送到 GitHub 后第一步即失败**，"clean checkout 可复现"在 CI 上直接不成立。
- **修复**：以索引（LF）字节重算并写入 7 个哈希，用 LF 重生成结果；提交数据文件时保持唯一换行约定（建议仓库内一律 LF），并在文档中写明 `core.autocrlf=false`，或改用 `.gitattributes` 强制全部为 LF 后重新检入。

### F2 — RO 未对承载结论的验证产物做哈希，而该产物每次运行都被改写 — Severity: `BLOCKER`

- **位置**：`verify_baseline.py:360-363`（写 `verification.json`、`verification_report.md`）、`:343`（`datetime.now(timezone.utc)`）；RO `evidence[1].source` = `.../results/verification_report.md`、`validators[0].result_ref` = `.../results/verification.json`，但 `artifacts` 只有 7 项，**均不含这两个文件**。
- **实际观察**：运行 `verify_baseline.py` 后 `git status --short` 出现 2 个已跟踪文件被修改；比对提交版与本次运行版，`files[].status/rows`、`tolerance_n`、`overall_status` 全部相同，**唯一变化是 `generated_utc`（`2026-10-04T17:49:04…` → `2026-10-10T13:03:02…`）**。
- **影响**：`validate_research_object.py` 只校验 `artifacts` 里的路径与哈希（第 83-94 行），因此承载 claim 的 `verification.json`/报告处于哈希管辖之外，可无声变更而 RO 仍 PASS；同时该文件因含时间戳而字节不可复现，永不可能有稳定的哈希。
- **修复**：把时间戳移出被哈希产物（或单独生成只含 `reference/tolerance/files` 的 `verification_core.json`），再把这两个文件以 `role: report`/`result` 登入 RO `artifacts` 并固定哈希。

### F3 — `run_manifest.json` 记录的 4 个 SHA-256 相对已提交内容即为错值 — Severity: `BLOCKER`

- **位置**：`Benchmarks/ANRI-RV-001/run_manifest.json:91-96`（`outputs.sha256`），其 `:151` 的 `next_action` 仍写着 "Fill the repository commit, Python version, creation time, and SHA-256 values"。
- **实际观察**：把 `HEAD:<该路径>` 取出后计算 SHA-256，与清单记录逐一比对：

  | 文件 | HEAD 内容摘要 | 清单记录 | 一致 |
  |---|---|---|---|
  | `Models/CDFV-001/Ref-01B/results/verification.json` | `08ccb47e587d75528d68ce6801eebdce8b05189cb6083c54710a774c6e5aa7b9` | `275032a1e253619075451486e376dd9d6cda86a84af06b8423578bb5745fbf3d` | 否 |
  | `Models/CDFV-001/Ref-01B/results/verification_report.md` | `2d2eb956a47518e2afe14ae638d28137f34d9835d337efa2c2b557f88e02a731` | `dcf3b33100a3f2697fdcc666515130cd77748cca501046a309da1648509c2e5b` | 否 |
  | `Benchmarks/…/A01_wrong_weight/results/verification.json` | `25c2fd0b2f31c012057e0593b9ba26e40d49b1037f492f85a237ae30bd828821` | `42ba42924904e6660f0ec462685cfd9250f5d0f5f84b9c78578bdc817e4fbeeb` | 否 |
  | `Benchmarks/…/A02_broken_force_balance/results/verification.json` | `7ad1a7ba7b5641b32ff5eeabcda288f455f1f441ed94d8a1cde8a65e559e6d60` | `e9bf693e2d75019a08202c247ee811e98fb88d917e240c1b96e230dbd857768a` | 否 |

  **4/4 不匹配**（我运行任何命令之前、该文件被任何改写之前即已如此）。唯一原因就是 F2 的时间戳。
- **影响**：这是仓库中唯一记录 A01/A02 对抗结果的运行台账，其完整性记录在提交时就是错的，无法用于独立复核。
- **修复**：按 F2 消除非确定性后重算这 4 个摘要，并删除 `next_action` 中的占位语句。

### F4 — `run_manifest.json` 的 displaced volume 与证据矛盾 — Severity: `MAJOR`

- **位置**：`Benchmarks/ANRI-RV-001/run_manifest.json:32`，字段 `reference_configuration.displaced_volume_m3` = `0.0020539453`。
- **实际观察**：`π(D/2)²L`（D=0.090、L=0.323）= `0.00205483721489674`，与 `verification.json:13` 及三个 CSV 一致。差 `8.919e-7 m³`，按 `ρg·ΔV` 折算 = `0.00875 N`，是清单自己声明的容差 `1e-4 N`（`:37`）的 **87 倍**。
- **影响**：运行台账的参考值与它引用的证据不一致，对抗性结论的数值前提不可信。
- **修复**：改为推导值，或从清单中删除派生量、改为引用 `verification.json`。

### F5 — gravity 常量三处不一致，且不在 RO assumptions 中 — Severity: `MAJOR`

- **位置**：`Research_Planning/CDFV-001_Reference_Configuration.md:116`（`9.81`）与 `:124`（`W ≈ 19.91 N`）；`Research_Planning/Ref-01B_Baseline_Model.md:246`（`9.81`）；`baseline_model.py:58` 与 `verify_baseline.py:35`（`9.80665`）；RO `assumptions`（第 122-138 行）只有 `A-FRESHWATER`/`A-FREE-SURFACE-ZERO`/`A-PRESCRIBED-MOTION`。
- **实际观察**：被 RO 哈希锁定的输入文档写 9.81，实际执行的两个脚本用 9.80665。`m·g` 相差 `0.0068 N` = 容差的 **68 倍**；若照文档重实现，`weight_reference` 必然 FAIL。RO 完全未记录 gravity。
- **影响**：参考配置与实现不一致，且关键输入未进入假设登记——正是清单判 BLOCKER 的"输入/单位/容差未记录"。
- **修复**：全仓库统一为 9.80665（或声明 9.81 并把容差放到合理量级），重算哈希，并在 RO 增加 `A-GRAVITY`（含值与单位）。

### F6 — 校验器未做清单声称的证据/校验器路径检查，也未套用 schema — Severity: `MAJOR`

- **位置**：`scripts/validate_research_object.py:83-98`。
- **实际观察**：只解析并哈希 `artifacts[]`；从不解析 `evidence[].source`、`validators[].result_ref`，也从不加载 `schema/research_object.schema.json`（该 schema 自身也不在 `artifacts` 中，可被改动而不被发现）。跨引用只查 claim↔evidence/validator/limitation 的 id。
- **影响**：清单"每个 evidence、validator、artifact 路径都存在"无法由该工具保证；`PASS` 的强度远低于字面含义。
- **修复**：加载并执行 JSON Schema；显式检查每个 `evidence.source` 与 `validators[].result_ref` 存在性；把 schema 文件本身登入 `artifacts`。

### F7 — 结果与记录中含作者本机绝对路径 — Severity: `MAJOR`

- **位置**：`Models/CDFV-001/Ref-01B/results/verification.json:3` 与 `verification_report.md:5`；`Models/CDFV-001/Ref-01B/verification.json:3`；`Benchmarks/ANRI-RV-001/adversarial/A01_wrong_weight/mutation.json:4`、`A02_.../mutation.json:4`。
- **实际观察**：写入 `<user-home>\...`（`verify_baseline.py:344` 与 `make_adversarial_cases.py:65`）。
- **影响**：违反清单 "No personal absolute Windows path is used as research provenance"，且（配合 F2）正是输出不可复现的机制。
- **修复**：所有生成记录改为仓库相对 POSIX 路径，机器信息只放单独的 environment 记录。

### F8 — 运行清单命令会弄脏已提交结果（固定产物与生成物混同） — Severity: `MINOR`

- **位置**：`verify_baseline.py:360-363`；`.github/workflows/anri-validation.yml:18,23-24,34-35`。
- **实际观察**：执行清单命令后 6 个已跟踪文件被改写（clean 2 个 + A01 2 个 + A02 2 个）；审阅方已用 `git checkout --` 恢复。
- **影响**：生成物进入版本控制又每次被覆盖，哈希与"固定 provenance 产物"无法区分；CI 里意味着每次运行都产生未提交差异。
- **修复**：生成物不纳入版本控制（或明确标注为 generated 并停止哈希它们），只固定输入与脚本。

### F9 — 无 Independent Review Gate 记录 — Severity: `MAJOR`

- **位置**：RO `review`（第 151-156 行）：`status: pending`、`reviewer_refs: []`、无 `decision_ref`；`Benchmarks/ANRI-RV-001/decision_log.md:6-7` 仍是 `Date: YYYY-MM-DD` / `Status: candidate / accepted / rejected`；而 `Research_Planning/Ref-01B_Baseline_Model.md:330` 已自称 "accepted"。
- **实际观察**：schema 支持 `review.decision_ref` 与 `approved/rejected/revision_requested`（`schema/research_object.schema.json:182-184`），但无任何一项被填写；`Independent Review Gate`/`Verified Research Package` 两个词在整个仓库只出现在本次审阅提示里。
- **影响**：闭环最后一环缺失，作者自评被当作独立验收。
- **修复**：定义 gate（审查人资格、必备证据、裁定载体），在 `review` 与 `decision_log.md` 记录审查人、结论、依据的哈希；把模型笔记中的 "accepted" 降级为作者自检。

### F10 — 重复且未登记的结果树 — Severity: `MINOR`

- **位置**：`Models/CDFV-001/Ref-01B/` 根下 `Ref-01B-B-0p10/25/50mps.csv`、`summary.csv`、`verification.json`、`verification_report.md`，与 `results/` 同名文件并存；`git ls-files --eol` 显示这些根下文件为 `i/crlf w/crlf`（唯一以 CRLF 入库者）。
- **实际观察**：这 6 个文件不在 RO `artifacts` 中。
- **影响**：无法判断哪棵树是冻结结果；CRLF 入库文件与 F1 叠加。
- **修复**：删除或明确弃用，并在 `results/README.md` 标注 generated/frozen 与生成命令。

### F11 — 对抗覆盖过窄 — Severity: `MINOR`

- **位置**：`Benchmarks/ANRI-RV-001/make_adversarial_cases.py:42,53-60,95-108`（只改 `csv_files[0]` 的第 0 行：`weight_N +0.1`、`constraint_force_N +1.0`）。
- **实际观察**：A01/A02 只改一个文件的第 1 行；0.25/0.50 两文件始终 PASS，且 CI 不重跑生成器。另：突变文件用 `lineterminator="\n"`（`:58`）写入，未突变的副本由 `shutil.copy2` 原样拷贝——生成器内部换行约定不统一。
- **影响**：只证明 1/7757 行的灵敏度，无法界定校验器覆盖面。
- **修复**：每个 case 文件、多列族各加突变（时间/位置非单调、浮力超界、缺列），并在 CI 中由 clean 结果重新生成对抗输入。

### F12 — 其它一致性缺口 — Severity: `MINOR`

- `Models/CDFV-001/Ref-01B/README.md:59-63` 与 `Research_Planning/CDFV-001_Reference_Configuration.md:116-127` 用 9.81 得到 20.16/19.91 N，而实际 `FULL_BUOYANCY_N=20.1510694`、`WEIGHT_N=19.9074995`；`CDFV-001_Reference_Configuration.md:5` 仍写 `CDFV-001-Ref-01`、`:287` 版式混乱。
- `verify_baseline.py` 的 column 别名走"包含"回退（`:86-93`），`constraint_force_abs_N` 会被 `constraint` 别名潜在误选（实测本轮正则命中 `constraint_force_n` 故未触发），建议加精确优先与负例测试。
- RO `provenance.git_commit` = `167d0fc`（`git log` 中 "Add ANRI-RV-001 run manifest"），而当前 HEAD = `abc9103`（"Add ANRI research object validation workflow"）；RO 自身在第 4 个提交之后。记录提交有效但语义不清，建议改为"本对象最后修改的提交"。

---

## Evidence Checked

以下命令全部实际执行（工作目录 `ANRI-Aerospace`），列出命令与其输出结论：

| 命令 | 实际结果 |
|---|---|
| `git status --short`（运行前） | `?? Reviews/`；分支 `feat/research-object-v0.1` |
| `git log -1 --oneline` / `git rev-parse HEAD` | `abc9103 Add ANRI research object validation workflow` / `abc91031930943c308edea73a97a120cbd6b8bf5` |
| `git ls-files --eol`（两次，含限定路径） | 数据/脚本 `i/lf w/crlf`；`verify_baseline.py`、`schema/research_object.schema.json`、`scripts/validate_research_object.py` 为 `w/lf`；`Models/CDFV-001/Ref-01B/*.csv\|json\|md` 根下文件为 `i/crlf w/crlf` |
| `git config --get core.autocrlf` / `core.eol` | `true` / 空 |
| `git check-attr -a -- <关键文件>` | `text: set`、`eol: lf`（`.gitattributes` 生效） |
| `Get-FileHash` × 7（工作区） | **7/7 与 RO 记录一致** |
| `git cat-file -e 167d0fc…` / `a2d241d…` | 均 exit 0，两个提交都存在 |
| `py -3 .\scripts\validate_research_object.py .\Research_Objects\RO-CDFV-001-Ref-01B.json --repo-root .` | `PASS`，exit 0；claims 1 / evidence 2 / validators 1 / artifacts 7 |
| `py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py` | `Overall status: PASS`，exit 0；4846/1940/971 行均 PASS；随后 `git status` 显示 2 个已跟踪文件被改写 |
| `py -3 …\verify_baseline.py …\A01_wrong_weight\results` | `FAIL`，exit 1（0.10 FAIL，0.25/0.50 PASS）——按预期失败 |
| `py -3 …\verify_baseline.py …\A02_broken_force_balance\results` | `FAIL`，exit 1（同上）——按预期失败 |
| `py -3 --version` | `Python 3.13.14` |
| `git ls-files … \| Set-Content` + `git checkout-index -a --prefix=<临时目录>` | 得到索引内容（LF）树；字节统计 CR=0 |
| `py -3 <LF树>\scripts\validate_research_object.py <LF树>\Research_Objects\…json --repo-root <LF树>` | **`FAIL`，exit 1，6 条 `sha256 mismatch`** |
| `py -3 <LF树>\…\verify_baseline.py <LF树>\…\results` | `PASS`，exit 0（数值部分跨平台可复现） |
| A01/A02 在 LF 树重跑 | 均 `FAIL`，exit 1 |
| `git show HEAD:<4 个 verification 文件>` + `Get-FileHash` | 与 `run_manifest.json` 记录 **4/4 不匹配** |
| `ConvertFrom-Json` 比对提交版/运行版 `verification.json` | 仅 `generated_utc` 变化，其余字段全同 |
| `git checkout -- <6 个被覆盖文件>` + 复核 | 恢复后 `git status --short` = `?? Reviews/`，7 个 RO 哈希复算 0 处不匹配，校验器复跑仍 `PASS` |

**未运行**：`git commit`、`git push`、任何写文件的生成脚本（未运行 `baseline_model.py`、`make_adversarial_cases.py`），以及任何真实 GitHub Actions 运行——CI 结论基于本地等价 LF 树实测，属基于事实的判断。

---

## Claim Assessment

**判定：部分支持。**

Claim（`C-CDFV-001-BASELINE-CONSISTENT`）："The baseline is internally computationally consistent within the stated assumptions; it is not experimental validation of free-surface loading."

支持该 claim 的**实际观察事实**：`constraint_force_N + buoyancy_N − weight_N` 在输出行中恒为 0（提交版报告记 `3.55271368e-15 N`，远小于 `1e-4 N` 容差）；我独立重算 `2.030 × 9.80665 = 19.9074995 N`、`π(0.045)²(0.323)×1000×9.80665 = 20.1510694 N`、满浸没约束力 `−0.2435699 N`，与 `summary.csv` 的 min/max 及 CSV 首行逐一吻合；三种速度下 `z` 均扫过 `±0.75L = ±0.24225 m`，行数 4846/1940/971 与 `ceil(Δz/v/dt)+1` 一致，末行 `submerged_length_m=0, buoyancy=0, constraint=+19.9074995`（完全出水）符合模型定义；`baseline_model.py`、README 与 RO 均把 free-surface/drag/added mass 列为排除项；措辞明确否认实验验证，与 `task.md:37-40` 的要求一致。

削弱该 claim 为"部分支持"的**判断依据**：其一，RO 用以支撑 claim 的 `E-CDFV-001-CONFIG` 是类型 `literature`、实际指向仓库内规划文档，而该文档（被哈希锁定）写的重力与实现相差 68 倍容差（F5）——参考配置与实现并不一致；其二，承载结论的 `verification.json`/报告不在哈希管辖内且每次运行字节不同（F2）；其三，唯一的运行台账哈希在提交时即为错值（F3）、其中参考体积与证据矛盾（F4）；其四，claim 只在 `1.2%` 的近中性裕度内成立（满浸没约束力 0.2436 N vs 重量 19.9075 N），RO 未给出该裕度与输入不确定度预算。因此：**具体数值恒等式成立且可复现；作为"研究主张"只被部分支持**，因为它所依赖的参考配置、证据完整性与运行台账尚不自洽。

---

## Reproducibility Assessment

**判定：不能。** 一份 fresh checkout 目前无法端到端复现所报告的结果。

可复现的部分（实际观察）：`verify_baseline.py` 仅用标准库，数值判定完全不依赖平台——我在 Windows 工作区与 LF 树两处运行，均得 `PASS` / `exit 0`；A01、A02 在两处均 `FAIL` / `exit 1`，失败原因分别正是 `weight_reference`（0.1 N）与 `force_balance`（1 N）。路径处理用 `Path(__file__).resolve().parent` 与可选位置参数，工作流引用的四个路径小写且实际存在、大小写完全一致（Ubuntu 可解析），也无需 `pip install`。这些是真实优点。

阻碍因素（按严重度）：

1. **换行格式（F1，决定性）**：Linux checkout 的字节与 RO 记录不同，校验器在 CI 第一步即 6 条不匹配失败。
2. **非确定性写入（F2）**：`generated_utc` 使 `verification.json`/报告每次运行字节不同，任何记录的摘要都瞬时失效（已实测提交版 vs 运行版仅此一处不同）。
3. **台账摘要本就错误（F3/F4）**：HEAD 版本对不上记录摘要，且参考体积与证据矛盾。
4. **本机绝对路径（F7）** 与 **重复结果树（F10）**：结果记录携带作者机器状态，且存在未登记的重名结果树。
5. **环境未完整记录**：台账记 Windows/PowerShell/Python 3.13.14（`run_manifest.json:14-20`），但 RO 未记录环境与依赖；RO 命令用 `python`（`validators[0].command`），清单用 `py -3`——两者均实测可行，但不是同一次调用。
6. **provenance 语义不清**：`git_commit=167d0fc` 早于当前 HEAD `abc9103`（F12）。

---

## Architecture Gap

- **ANRI Research Object** — *部分实现。* 事实：有真正带 `additionalProperties: false` 与枚举的 schema（`schema/research_object.schema.json`）、有填充完整的对象（16 个必填字段齐备、id 精确为 `RO-CDFV-001-Ref-01B`、7 个工件路径真实存在）、有可执行的校验器。判断：校验器不套用 schema、不检查 evidence/validator 路径（F6）；RO 不对自己的结果产物做哈希（F2）；assumptions 缺 gravity（F5）；`review` 与 `decision_ref` 闲置（F9）；provenance 含本机路径（F7）；`Research_Planning/Active_Questions.md`、`Decision_Log.md`、`schema/`、`Benchmarks/ANRI-RV-001/README.md`、`task.md`、`rubric.yaml`、`run_manifest.json` 等被审阅依赖的文件均未纳入工件。**缺少能力**：CI 强制的 schema 合规 + 可冻结的确定性结果产物。
- **Claim–Evidence Graph** — *部分实现。* 事实：1 个 claim、2 个 evidence、1 个 validator，id 级引用完整性有校验（脚本第 65-81 行）。判断：evidence 的 mass/diameter/length/density/gravity 只存在于自由文本 `conditions`，无法机器核对，所以"参考配置与实现一致"这一项无法自动检查（F5 正是它漏掉的真实缺陷）；`E-CDFV-001-CONFIG` 类型标为 `literature` 而实际是内部规划文档；`E-CDFV-001-RESULTS` 指向未哈希的报告。**缺少能力**：带单位与容差的数值型证据绑定。
- **Executable Validators** — *部分实现。* 事实：校验器真实、小、零依赖、别名容错、区分 PASS/PARTIAL/FAIL、失败时非零退出，且经实测确实按设计意图抓住两种注入错误。判断：不校验对象与台账（F6）、输出非确定（F2）、覆盖面窄（F11）。**缺少能力**：既校验数值、也校验对象与记录的确定性校验器。
- **Independent Review Gate** — *基本缺失。* 事实：仓库内无定义该 gate 的工件；两个术语只出现在本次审阅提示中；`review.status=pending`、`reviewer_refs=[]`、无 `decision_ref`；`decision_log.md` 为未填模板；模型笔记已自称 accepted（F9）。判断：无法阻止作者自评充当独立验收，也没有把审查裁定绑定到具体证据哈希的载体。**缺少能力**：gate 定义 + 审查人身份 + 绑定证据哈希的裁定工件 + 把准则逐条结果写回对象。
- **Verified Research Package** — *不存在。* 事实：无打包步骤、无环境/锁文件记录、无一份第三方可在 clean checkout 上一次跑通并自检的清单；唯一运行台账未被 RO 引用、且部分过期、部分错值（F2/F3/F4/F9）。判断：当前对象最准确的定位是"作用域清晰、数值自洽、本地校验器可用，但记录与哈希不可复现的计算基线"，尚非 verified package。**缺少能力**：一个确定性的自校验捆绑包（对象 + schema + 脚本 + 冻结输入输出 + 哈希 + 运行记录 + 审查裁定），任何字节不符即显式失败。

---

## Recommended Next Action

1. **让记录先确定、再冻结哈希（F1、F2、F3、F8、F10）。** 把 `generated_utc` 移出被哈希产物、把所有绝对路径改为仓库相对 POSIX 路径、统一数据文件换行约定（以索引 LF 字节为准）、删除或弃用 `Models/CDFV-001/Ref-01B/` 根下的重复结果树；然后重算并冻结脚本、输入、结果、报告与 `run_manifest.json` 的 SHA-256，并把它们全部登入 RO `artifacts`。这是其他一切的前置条件——目前"记录哈希"本身在 Linux 上就是错的。
2. **建立 Independent Review Gate 并落记录（F9、F12）。** 定义审查人资格、必备证据与裁定载体，在 RO `review` 中填入 `decision_ref` 与 `reviewer_refs`，用真实日期与逐条准则结果填好 `decision_log.md`（含被审证据的哈希），并把 `Ref-01B_Baseline_Model.md:330` 的 "accepted" 降级为作者自检。此后本分支的 CI 才有意义。
3. **补齐自洽性与校验能力（F5、F6、F7、F11）。** 全仓库统一 `g=9.80665`（或改为 9.81 并给出量级合理的容差）、在 RO assumptions 增加 `A-GRAVITY`、修正清单体积值与 9.81 派生的 20.16/19.91 N 文档值；扩展 `validate_research_object.py` 执行 JSON Schema 并检查每个 `evidence.source`/`validators[].result_ref`；把对抗突变扩展到每个 case 文件与多个列族，并由 clean 结果在 CI 中重新生成。

---

## 审阅限制（不得当作已验证）

- 本次未执行任何 git 写操作（无 `commit`、无 `push`），未运行两个生成脚本（`baseline_model.py`、`make_adversarial_cases.py`），未触发真实 GitHub Actions。
- CI 结论来自用 `git checkout-index` 导出的索引内容（LF）树上的等价实测；`git ls-files --eol` 的 `w/crlf` 结论在导出时被同一 smudge 机制复现（导出树 CR=0），因此"导出树与 Linux fresh checkout 字节等价"属基于事实的判断，而非在 Linux 上的直接运行。
- 审阅方运行清单验证命令后，`verify_baseline.py` 覆盖了 2 个已跟踪结果文件；审阅方已用 `git checkout --` 恢复这 6 个文件（clean 2 + A01 2 + A02 2），并删除工作区中的临时探针目录。仓库最终状态与运行前一致（仅 `?? Reviews/`），7 个 RO 哈希复核仍全部一致。

## 键值速查

| 项目 | 值 |
|---|---|
| `WEIGHT_N` | `19.9074995`（2.030 × 9.80665） |
| `FULL_BUOYANCY_N` | `20.1510694`（1000 × 9.80665 × π(0.045)² × 0.323） |
| 满浸没约束力 | `−0.2435699 N`（≈ 重量的 1.2%） |
| 完全出水约束力 | `+19.9074995 N` |
| 最大力平衡残差 | `3.55271368e-15 N`（容差 `1e-4 N`） |
| 扫描范围 | `z ∈ [−0.24225, +0.24225] m`（`±0.75L`） |
| 行数 | `4846 / 1940 / 971`（0.10 / 0.25 / 0.50 m/s） |
| RO 哈希一致（Windows 工作区） | `7/7` |
| RO 哈希一致（LF = Linux checkout） | `1/7`（仅 `verify_baseline.py`） |
| 台账摘要一致（HEAD 内容） | `0/4` |
| 清单命令改写已跟踪文件数 | `6` |
