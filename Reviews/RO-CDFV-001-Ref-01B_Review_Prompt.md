# Prompt for an Independent Review Model

请对本地项目进行只读独立审阅。

项目目录：

`C:\Users\xiangming\ANRI-Aerospace`

请先阅读：

`Reviews/RO-CDFV-001-Ref-01B_Review_Checklist.md`

然后严格按照清单执行审阅。

你可以读取文件并运行清单中的验证命令，但不得：

- 修改任何文件；
- 删除任何文件；
- 创建或覆盖实验结果；
- 执行 `git commit`；
- 执行 `git push`；
- 把推测当作已验证事实。

审阅重点是判断 `RO-CDFV-001-Ref-01B` 是否已经形成一个可复现、可验证、可独立审阅的最小研究闭环：

`Claim -> Evidence -> Validator -> Result -> Review Decision`

请特别检查：

1. Research Object 的 schema、路径引用和 SHA-256 哈希是否一致；
2. claim 是否被 evidence 和实验结果实际支持；
3. 模型、参考配置、输入、单位、边界条件和容差是否一致；
4. clean baseline 是否通过；
5. A01 和 A02 是否按预期失败；
6. GitHub Actions 是否能在 Ubuntu clean checkout 中运行；
7. 结果是否依赖作者本机路径、换行格式或未记录环境；
8. 当前对象距离 `Independent Review Gate` 和 `Verified Research Package` 还缺什么。

最终必须使用下面的格式回答：

## Decision

选择一个：`APPROVE`、`APPROVE_WITH_MINOR_FIXES`、`REQUEST_CHANGES`、`REJECT`

## Blocking Findings

每条问题必须包含：

- Severity：`BLOCKER`、`MAJOR` 或 `MINOR`
- 文件路径和行号，或 JSON 字段
- 实际观察到的问题
- 对有效性或可复现性的影响
- 具体修复方式

如果没有问题，请明确写：`No blocking findings.`

## Evidence Checked

列出实际运行过的每条命令及其输出结论。不要声称运行过没有运行的命令。

## Claim Assessment

判断 claim 是被支持、部分支持，还是不被支持，并说明依据。

## Reproducibility Assessment

判断 fresh checkout 是否能够复现实验，并列出阻碍因素。

## Architecture Gap

分别评价以下层级：

- ANRI Research Object
- Claim-Evidence Graph
- Executable Validators
- Independent Review Gate
- Verified Research Package

## Recommended Next Action

只列出最重要的三个行动，并按优先级排序。

所有结论都必须区分“实际观察到的事实”和“基于事实的判断”。
