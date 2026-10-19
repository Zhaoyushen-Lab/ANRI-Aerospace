# DeepSeek Harness 本机修复指令

你是本项目的本机代码维护 Agent。你拥有对本地仓库的完整读写权限，可以编辑、创建、移动和删除项目文件，可以运行 Python、PowerShell 和 Git 命令。

## 项目位置

`C:\Users\xiangming\ANRI-Aerospace`

请先进入该目录并执行：

```powershell
Set-Location "C:\Users\xiangming\ANRI-Aerospace"
git branch --show-current
git status --short
```

当前任务是修复 `RO-CDFV-001-Ref-01B` 独立审阅报告中指出的问题，使它能在 Windows 和 GitHub Actions Ubuntu clean checkout 中复现。

## 执行规则

1. 先阅读本仓库的 Research Object、schema、验证脚本、模型、结果、run manifest、GitHub workflow，以及 `Reviews/RO-CDFV-001-Ref-01B_Independent_Review_Report.md`。
2. 可以修改本地代码、JSON、Markdown、CSV、YAML 和结果生成逻辑。
3. 不得使用 `git reset --hard`、`git checkout --` 或覆盖用户修改的命令。
4. 不要删除已有内容，除非确认它是报告 F10 指出的重复生成结果，并记录删除原因。
5. 不要修改科学结论来掩盖失败；冲突必须修正来源并重新计算。
6. 路径使用仓库相对 POSIX 路径，不要写入 `C:\Users\...`。
7. 不要执行 `git push`。可以创建本地 commit，但提交前输出变更摘要和测试结果。
8. 例行编辑不需要询问；遇到科学定义无法判断的冲突时才暂停。

## 阶段 1：确定性和哈希

优先修复 F1、F2、F3、F8、F10：

- 全仓库统一使用 `g=9.80665 m/s^2`，并同步参考配置、模型、验证器、README、RO 和 manifest。
- 移除 `verification.json` 和报告中的动态 `generated_utc`，或把动态信息放进不参与冻结哈希的独立元数据。
- 移除结果和 manifest 中的本机绝对路径。
- 统一冻结文本文件为 LF。
- 用 Git index 中的 LF 字节重新计算 SHA-256。
- 修正 `run_manifest.json` 中四个错误摘要和错误的 `displaced_volume_m3`。
- 清理或明确弃用 `Models/CDFV-001/Ref-01B/` 根目录下与 `results/` 重复的结果树。
- 明确区分 frozen artifact 与 generated output。

阶段出口：

- Windows 工作区 validator 通过；
- Git index 导出的 LF 树 validator 通过；
- 连续运行两次，冻结文件 SHA-256 不变；
- 验证命令不会修改已跟踪冻结结果。

## 阶段 2：扩展校验器

修复 F5、F6、F7：

- 在 RO assumptions 中加入 `A-GRAVITY`，包括数值、单位和来源。
- `validate_research_object.py` 必须加载并验证 `schema/research_object.schema.json`。
- 检查每个 `evidence[].source` 和 `validators[].result_ref` 的存在性。
- 将 schema 加入 artifacts 并计算哈希。
- 确保 claim、evidence、validator、result 和 report 的引用闭合。
- 关键输入至少要有质量、直径、长度、密度、重力和容差等机器可读字段。
- 验证失败时返回非零退出码并打印具体字段或路径。

阶段出口：

- 删除 evidence 文件会失败；
- 修改 schema 会失败或要求更新哈希；
- 修改 gravity 会被校验器或数值验证发现；
- 不存在的 result 引用会失败。

## 阶段 3：Independent Review Gate

修复 F9：

- 将作者文档中的 `accepted` 改为 `author_self_check`，除非有独立审查证据。
- 定义 `pending`、`revision_requested`、`approved`、`rejected` 状态。
- 在 `review` 中填写审查人、日期、决策引用和报告 SHA-256。
- 将 DeepSeek Harness 报告登记为真实的 `revision_requested` 审查记录。
- 更新 `decision_log.md`，删除日期和状态占位符。
- CI 必须阻止 `review.status != approved` 时发布 `verified`。

## 阶段 4：对抗测试

修复 F11、F12：

- 为每个速度工况生成对抗案例。
- 覆盖多个列族，而不是只修改第一个 CSV 的第一行。
- 增加缺列、时间非单调、位置非单调、浮力超界和单位错误案例。
- CI 从 clean baseline 重新生成对抗输入。
- 精确列名匹配优先于包含匹配，并增加负例测试。
- 清理 README、参考配置和模型文档中的旧重力值和旧对象 ID。

## 最终验收命令

实际运行并记录：

```powershell
py -3 .\scripts\validate_research_object.py `
  .\Research_Objects\RO-CDFV-001-Ref-01B.json `
  --repo-root .

py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py

py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py `
  --results-dir .\Benchmarks\ANRI-RV-001\adversarial\A01_wrong_weight\results

py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py `
  --results-dir .\Benchmarks\ANRI-RV-001\adversarial\A02_broken_force_balance\results

git diff --check
git status --short
```

还必须在 Git index 导出的 LF 树上重复 Research Object validator 并确认通过。

## 完成条件

只有满足以下全部条件才可报告完成：

- Windows validator 通过；
- LF clean tree validator 通过；
- baseline verification 通过；
- A01 和 A02 按预期失败；
- 连续两次生成不会改变冻结文件哈希；
- manifest 哈希与实际提交内容一致；
- 无本机绝对路径；
- schema、evidence、validator result 引用都存在；
- review 状态真实记录为 `revision_requested` 或 `approved`；
- `git diff --check` 通过；
- 最终报告列出所有修改文件和测试结果。

## 最终报告格式

```markdown
# Repair Report

## Changed Files
列出每个修改、创建、移动或删除的文件及原因。

## Findings Addressed
逐项说明 F1-F12 哪些已修复，哪些未修复。

## Commands Run
列出实际运行的命令、退出码和关键结果。

## Hash and Reproducibility Result
说明 Windows 工作区、LF clean tree 和 GitHub Actions 预期结果。

## Review Gate Status
说明当前 review 状态、审阅报告路径和报告哈希。

## Remaining Risks
只列出仍然存在的具体风险。

## Commit Recommendation
判断是否适合本地 commit。不要执行 git push。
```
