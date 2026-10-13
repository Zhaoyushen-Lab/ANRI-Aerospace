# ANRI / AI4S / AI4E 日报 — 2026-10-11

> 首份日报。本文件用于建立**可跨日复现**的评估口径：日期、层级判定、概率分解与
> 触发条件在每个后续日报中保持同一格式，便于逐日对比 Δ。

- 日期：2026-10-11（周六）
- 口径版本：`v1`（首次建立）
- 状态快照：`Research_Log/2026-10-11_ANRI_State.json`（由 `scripts/collect_state.py` 生成，`checks_all_ok = true`）
- 数据来源：公开网络检索 + 本地仓库 `C:\Users\xiangming\ANRI-Aerospace` 实测
- 评估对象：图中的 "改进版 ANRI-ResearchOS" 五层体系

> 本日报的**事实数字**改为引用状态快照，不再手工转述。
> 生成命令：`py -3 .\scripts\collect_state.py --out "Research_Log\2026-10-11_ANRI_State.json"`。
> 快照中 `head.commit = abc91031930943c308edea73a97a120cbd6b8bf5`，
> `worktree.pending_entries = 98`（staged 96 / untracked 2），
> `line_endings.worktree_crlf = 0`，`research_object.artifact_count = 64`，
> `review_gate.independent_human_reviews = 0`，8 项检查退出码全部符合预期。

---

## 1. 一句话摘要

今天最重要的两件事：**一是上游出现了直接对标 ANRI 五层体系中"第三方可校验研究产物"
的学术工作（Ara, 2026-05），二是长时域 agent 的首个跨域基准给出了令人清醒的数字——
科学实验设计类任务平均成功率仅 21.4%，且 43.3% 的失败源于 agent"提前放弃"。**
本地侧，ANRI-Aerospace 的 Research Object 已于今日完成修复并达到可复现状态
（64 个产物哈希在 Windows 与 LF checkout 下均一致），但仍**未提交**，
且第 4 层 Independent Review Gate 仍无独立人工审阅记录。

---

## 2. 上游进展

### 2.1 研究产物层（对应图中第 2 层）

**Ara: Agent-Native Research Artifacts（arXiv:2604.24658, 2026-05）— 本日最重要的对标工作。**
它把"论文"替换为 4 层 agent 可执行包：

| Ara 层 | 内容 | 与本项目对应物 |
|---|---|---|
| L1 科学逻辑 | claim graph + 推理 | `claims` + Claim–Evidence Graph |
| L2 可执行代码 | 可运行且规格完整 | `baseline_model.py` / `verify_baseline.py` |
| L3 探索图谱 | 试过什么、失败什么、为何放弃 | **缺失**（`git log` + 12 个对抗案例是原材料） |
| L4 证据落地 | 每条 claim → 原始输出 | `evidence_refs` + 64 个哈希注册产物 |

它把学术出版的损耗命名为**两种税**：*Storytelling Tax*（失败实验与放弃的分支被压成
线性叙事，对人类可忍，对复现 agent 是灾难）与 *Engineering Tax*（"用了合适的超参数"
这类对人类评审够用的表述，对 agent 是规格空洞，agent 根本无法执行）。
论文自报在 PaperBench 上问答准确率 **72.4% → 93.7%**，RE-Bench 上复现成功率
**57.4% → 64.4%**（以上为论文自报数字，未经我独立验证）。

**反直觉发现**：保留失败轨迹的效果**取决于 agent 能力**——当 agent 弱于原作者时，
失败轨迹加速进展；当 agent 强于原作者时，失败轨迹反而**限制**它，使其困在既有解法
的框里。

**开放问题（对本项目直接可操作）**：论文明确点名"**从 git log + 实验追踪自动编译出
探索图谱**"是最有价值的下一步，并说 Ara Compiler 只是第一次尝试、预计 90 天内出现
第二波。本项目的 `git log`（11 个提交）与 ANRI-RV-001 对抗集正是这一路径现成的原料。

生态工具三件：Live Research Manager（开发期捕获决策与死路）、Ara Compiler（把遗留
PDF/仓库翻译成 Ara）、Ara-native review（自动做客观检查，让人类只评审意义与品味）。
第三件与本项目第 4 层 Independent Review Gate 的定位一致。

相关：**Intern-Atlas**（捕捉*跨论文*的方法谱系）与 Ara（捕捉*论文内*探索图谱）被描述
为互补的"agent 原生研究知识栈"。
[论文](https://arxiv.org/abs/2604.24658) ·
[wiki 摘要](https://bayesiansapien.github.io/cere-bro/agentic-systems/2026-05-01-ara-agent-native-research-artifacts/)

- **Provenance, Timestamp Evidence, and Source-Chain Auditability**（Zenodo）讨论
  AI 辅助研究程序的来源链与时间戳证据审计——与本项目今日修复的
  "哈希冻结 + 台账交叉校验"直接相关。
  [链接](https://zenodo.org/records/21330680/files/SIT-16-provenance-timestamp-source-chain-v2.pdf)
- **Reimagining research papers as interactive and reliable AI agents**（Nature, 2026）
  把论文重做成可交互 agent，说明主流出版侧也在往"可执行研究产物"方向移动。
  [链接](https://www.nature.com/articles/s41586-026-11044-y)

### 2.2 通用科研 agent / 工具层（对应图中第 1 层的 agent 部分）

- **ClawsGO Science**（北京比特奇迹科技，36氪 2026-09-23）宣称把云服务器、预装科研
  环境、文献检索、代码执行、数据可视化、LaTeX 工作区封进单一 agent 界面，并具备
  **长时域执行（数小时、断点续跑）** 与 **任务图 + 多子 agent 协作** 两层工程能力，
  支持多模型路由，保留环境/命令/文件修改/检索动作的完整过程轨迹，**关键结论标注
  支撑来源**。
  这是与图中"人类 / ClawsGO / Codex / 实验设备"框最贴近的产品化进展。
  **须标注的不确定性**：该文为公司融资导向的报道，明确承认"付费用户规模、复购率、
  营收数据尚未公开"，长时域任务成功率与断点恢复表现也尚无公开指标。
  [36氪 英文版](https://eu.36kr.com/en/p/3995487329308552) ·
  [36氪 中文版](https://m.36kr.com/p/3995487329308552)
- **Google Co-Scientist**：多 agent 研究伙伴，持续迭代中。
  [链接](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/)
- **Google 学术工作流 agent**（配图与同行评审两个 agent）。
  [链接](https://research.google/blog/improving-the-academic-workflow-introducing-two-ai-agents-for-better-figures-and-peer-review/)
- **OpenAI 关于 agentic AI 与科学计算**的官方表态。
  [链接](https://openai.com/zh-Hant-HK/index/scientific-computing-agentic-ai/)

### 2.3 AI4S / AI4E 平台与政策层

- **晶泰科技 XtalPi Science**（2026-07-30）发布被描述为"AI4S 原生操作系统"的产品，
  主打从"模型假设"到"物理验证"的闭环。
  [链接](https://www.stdaily.com/web/gdxw/2026-07/30/content_556091.html)
- **上海"超级科研工厂"**（2026-07-09）宣称国内首个零人工介入的科研工厂。
  [链接](https://www.stdaily.com/web/gdxw/2026-07/09/content_544682.html)
- **全国首个 AI4E 千卡工科智算集群落地同济大学**（2026-06）——AI4E（AI for
  Engineering）开始有专用算力基础设施。
  [科学网](https://paper.sciencenet.cn/htmlnews/2026/6/567167.shtm) ·
  [证券时报](https://stcn.com/article/detail/3983529.html)
- **百度 AI4S 科学家计划**（2026-08-12）面向百位学者。
  [链接](https://www.stdaily.com/web/gdxw/2026-08/12/content_562839.html)
- 市场与政策：QY Research 估计全球 AI for Science 市场 2025 年约 45.38 亿美元，
  2032 年约 262.3 亿美元，CAGR ≈ 28.9%；国家数据局 2026 年 6 月《关于推进行业
  高质量数据集建设行动实施方案》首次在行业数据集层面部署科研领域高质量数据。

### 2.4 实验闭环层（对应图中第 1 层的"实验设备"部分）

- **SLAC SPIRE**（2026-10-08，DOE 资助，SLAC 牵头，联合 Stanford、UChicago、
  Argonne、Brookhaven、LBNL）：建设"自驱动实验室"平台，三个方向为**具身 SI 精密
  样品操作、X 射线/电子束自校正、实验期间实时数据分析**；SI agent 现场解读数据并
  实时调整实验，只把最有价值的结果推给研究者。明确目标是"可泛化的自主实验室
  工作流，可跨 DOE 设施迁移"。
  [链接](https://www6.slac.stanford.edu/news/2026-10-08-slac-leads-new-project-build-self-driving-laboratory-future)
- 相关：**From Isolation to Agency: Toward Fully Autonomous Laboratory Ecosystems**
  （IEEE）讨论实验室生态从孤立走向自主。
  [链接](https://xplorestaging.ieee.org/document/11511636)

### 2.5 评测与可靠性（决定"大规模使用"能否成立的关键证据）

- **AutoLab**（arXiv:2606.05080，2026-06）构建 36 个长时域闭环优化任务：
  | 模型 | 成功率 | 提前终止率 | 平均迭代轮次 |
  |---|---:|---:|---:|
  | claude-opus-4.6 | 47.2% | 22% | 8.3 |
  | claude-sonnet-4 | 38.9% | 31% | 6.7 |
  | gpt-4o | 27.8% | 44% | 5.2 |
  | gemini-2.0 | 22.2% | 50% | 4.8 |
  | qwen-max | 13.9% | 61% | 3.5 |
  | **平均** | **27.4%** | **43.3%** | 5.5 |

  分领域中**"科学实验设计"平均成功率仅 21.4%**（最优模型 42.9%）；结论指出
  "短任务强者 ≠ 长任务强者"，且**能正确处理反馈的 agent 成功率提升 2.3 倍**。
  **须标注的不确定性**：我读取的是二手解读文章，其标题写"68% 因提前放弃而失败"、
  正文写 43.3%，两处口径不一致；我在上表采用正文表格的 43.3%，并且样本量只有
  36 个任务、4 个领域，作者自己也承认泛化性待验证。**该数字应视为数量级参考，
  不是精确常数。**
  [解读文章](https://cloud.tencent.cn/developer/article/2684253?policyId=1003)
- **ClaroAI-Bench**：在真实生物医学论文上评测 agentic 科研可复现性。
  [链接](https://dev.europepmc.org/article/PPR/PPR1210202)
- **SciAgentGym**：多步科学工具使用的 agent 基准。
  [链接](https://xuanjing-huang.github.io/publication/sciagentgym-zh)
- **FrontierChallenge**：评测科学工作流完成度。
  [链接](https://arxiv-org.ezproxy.obspm.fr/html/2608.24979v2)
- **Co-Reviewer**：LLM 与人类在同行评审上的对齐研究，是第 4 层
  Independent Review Gate 能否自动化的直接相关证据。
  [链接](https://dl.acm.org/doi/10.1007/s11192-026-05557-6)

---

## 3. ANRI 五层体系对照

| 层级 | 图中模块 | 上游成熟度（今日） | 本项目状态（今日，取自 State.json） |
|---|---|---|---|
| L1 | 人类 / ClawsGO / Codex / 实验设备 | **快速成熟**：ClawsGO 已产品化（指标未公开）；Codex/Claude 类 agent 能力与长时域评测同步上升 | 实验设备侧仅有 `Experiment_Requests/CDFV-001-Ref-01S_Experiment_Request.md`，状态为"预沟通材料"，尚无实验室确认 |
| L2 | ANRI Research Object | **已有直接对标工作且已量化**（Ara，见 §2.1） | 已有 1 个对象 `RO-CDFV-001-Ref-01B`，schema v0.2，64 个哈希注册产物，校验器 PASS；对照 Ara 的 4 层：L1/L2/L4 已有对应物，**L3 探索图谱缺失** |
| L3 | Claim-Evidence Graph + Executable Validators | 评测基准开始出现（ClaroAI-Bench 等） | Claim-Evidence 图存在但只有 1 claim / 3 evidence；验证器已做到确定性输出、跨平台哈希一致、12 对抗案例 + 18 负例 + 13 门禁自测全通过 |
| L4 | Independent Review Gate | Co-Reviewer 等在研究自动化评审 | **最薄弱层**：`review.status = revision_requested`，但审阅方是 AI 只读会话，**无独立人工审阅记录** |
| L5 | Verified Research Package | 无现成对标 | 打包要素（对象+校验器+台账+评审记录+CI 门禁）已齐备，但只有 1 个对象，未证明可复制到第二个研究问题 |

---

## 4. 成功概率评估（口径 v1）

### 4.1 目标定义

"成功" = 完成图中五层并**大规模使用**。拆成两个可分别判定的门槛：

- **门槛 A（单用户闭环）**：本人在 ≥1 个真实研究问题上，稳定跑通
  L1→L5 全链，且 L5 产出可被第三方按文档复现。
- **门槛 B（大规模使用）**：≥3 个不同研究问题 / ≥2 个不同学科或团队 /
  ≥1 位非作者人员主动使用该体系产出并接受 L4 审查。

### 4.2 分解（每条为合取项，即全部都要成立）

| 组件 | 今日判定 | 依据 |
|---|---:|---|
| L1-agent（ClawsGO/Codex 侧可用且持续可用） | 0.80 | 产品已存在且公开可注册；长时域成功率约 20–47%，对"数小时无人值守"仍不足以完全托付 |
| L1-lab（Ref-01S 实验设备接入） | 0.35 | 仅到预沟通材料阶段，无实验室回复、无预算、无排期 |
| L2（对象标准可扩展到第 2 个研究问题） | 0.65 | 单例已跑通；Ara（§2.1）独立验证了"agent 原生研究产物"这一命题并给出量化收益，且其 4 层结构与本项目 3 层直接对应、缺口（探索图谱）可由现有 `git log` 补齐——命题风险下降；跨问题复用仍未验证 |
| L3（claim-evidence 图 + 验证器达到可被他人复核的严格度） | 0.70 | 验证器证据强（跨平台哈希一致、对抗与负例覆盖、门禁自测）；但 evidence 仍主要是内部文档，无外部基准对照 |
| L4（独立审查真实发生并留存） | 0.30 | 需要真实第三方花时间复核并接受"哈希级证据"审阅；当前 AI 会话不满足"独立"的强定义 |
| L5（打包成为习惯并跨项目复用） | 0.30 | 要素齐备但零复用案例；依赖 L4 先成立 |

**独立乘积**：0.80 × 0.35 × 0.65 × 0.70 × 0.30 × 0.30 ≈ **0.0115**
（即约 1.2%，仅用于检验量级，不作为最终值，因为各因子并非严格独立）

### 4.3 今日结论

| 口径 | 概率 | 时间窗 |
|---|---:|---|
| 门槛 A（单用户闭环） | **80%** | 12 个月内 |
| 门槛 B（大规模使用） | **约 7%（区间 7–12%）** | 24 个月内 |
| 完全建成五层 + 大规模使用 | **约 2%（区间 2–3%）** | 5 年内 |

上表取整数，因为底层因子本身就是判断而非测量，保留小数会造成虚假精度。
区间由 §4.4 的敏感度分析给出。

### 4.4 判断依据与不确定性（必须区分事实与判断）

**实际观察到的事实**：上述第 2 节所有链接与其正文内容；本地状态快照
`Research_Log/2026-10-11_ANRI_State.json` 中：`head.commit = abc9103…`（与本次
修复前相同，说明修复尚未 commit）、`worktree.pending_entries = 98`、
`line_endings.worktree_crlf = 0`、`research_object.artifact_count = 64`、
`review_gate.independent_human_reviews = 0`、`review_gate.status =
revision_requested`；`Experiment_Requests/CDFV-001-Ref-01S_Experiment_Request.md`
的"计划状态"节仍为 3 条预沟通条目；`Research_Log` 中此前只有 3 个历史文件；
8 项检查（RO 校验 0、clean baseline 0、A01/A02 各 1、负例 18 例 0、对抗 12 例 0、
门禁自测 13 场景 0、对象/台账漂移 0）退出码全部符合预期。

**基于事实的判断**：
1. 门槛 A 之所以给到 80% 而非更高，是因为 L4 的"独立性"与 L1-lab 的"设备"两项
   都不由本人单独控制，而 AutoLab 的 21.4% 科学实验设计成功率提示：即便全部
   工具就位，"无人值守跑出可信结论"仍会频繁失败，需要人工检查点兜底。
2. 门槛 B 之所以只有约 7%，核心不是技术，而是**采用率**：目前没有第二个使用者、
   第二个研究问题、第二个学科。所有技术层证据都无法替代"别人愿不愿意用"。
   Ara 的自报收益（PaperBench +21.3 个百分点）说明"agent 原生研究产物"这一
   命题本身有效，但那证明的是**格式的价值**，不是**本项目标准的采用**，二者不能混同。
3. **该 7% 中含大量主观不确定性**（尤其是 L4=0.30 与 L5=0.30 两个因子，本质是
   对协作与习惯的预测）。敏感度：
   - 若 L4 与 L5 各取 0.5 → 门槛 B 升到约 **12%**；
   - 若 L1-lab 在 24 个月内不发生（0.1）→ 降到约 **2%**；
   - 若 L2 回落至原值 0.55（认为 Ara 的映射不足以降低风险）→ 降到约 **6%**。
   **这是判断，不是测量。**

### 4.5 距上一次评估的变化（Δ）

无（本文件为基线）。

但**本文件在 2026-10-11 日内被修订过一次**，修订原因必须记录，以免与"跨日 Δ"混淆：

| 修订项 | 修订前 | 修订后 | 触发证据 |
|---|---:|---:|---|
| 因子 L2 | 0.55 | **0.65** | 精读 Ara（arXiv:2604.24658）：它独立验证了"agent 原生研究产物"命题并量化收益（自报 PaperBench 72.4%→93.7%），其 4 层与本项目 3 层直接对应；它点名的下一步（从 git log 自动编译探索图谱）正是本项目现成原料 |
| 门槛 B | 6% | **约 7%** | 同上，由 L2 变化经 §4.2 传递 |
| 新增工作项 | — | — | Ara 的 L3"探索图谱"被识别为本项目 L2 的明确缺口，进入 §5 |

**这不是跨日 Δ**：本文件仍标记为 2026-10-11 的基线，跨日 Δ 从下一份日报开始计算。
把日内修订单独列出，是为了让后续读者能区分"证据更新"与"日期推进"。

---

## 5. 高杠杆动作（按对概率的边际影响排序）

1. **把已 staged 的修复提交，并跑通第一个"改完再验"的完整周期。**
   L2/L3 的技术证据已经很强，但它们目前只存在于工作区；`git log -1` 仍是
   修复前的 commit，"可复现"对第三者来说尚不可见。
2. **给 L4 补一次真实独立审阅。** 从概率上看这是最大单点杠杆（0.30 是六个因子
   里最低的一个与 L5 并列）：找一位同事按
   `Reviews/RO-CDFV-001-Ref-01B_Review_Checklist.md` 复核一次并署名，
   比再加 10 个对抗案例更能提升体系可信度。
3. **推进 Ref-01S 实验室预沟通的下一步。** 这是 L1-lab 从 0.35 上升的唯一路径，
   且它是六因子中第二低。
4. **补齐 Ara 意义上的 L3"探索图谱"缺口。** 今天精读发现：本项目的对象已有
   Ara L1/L2/L4 的对应物，唯独缺"试过什么、失败什么、为何放弃"这一层，而
   `git log`（11 个提交）、ANRI-RV-001 的 12 个对抗案例、以及被删除的重复结果树
   （F10）都是现成原料。Ara 明确把"从 git log 自动编译探索图谱"列为最有价值的
   开放问题，并称 90 天内会出现第二波——这意味着**这是有时间窗的机会**。
   注意 Ara 的反直觉发现：失败轨迹对"弱于原作者的 agent"有帮助、对"强于原作者的
   agent"反而构成约束；因此自建的探索图谱应设计成可选择性注入，而不是全量灌入。
5. **启动第二个 Research Object**（不同研究问题、最好不同学科）。这是把 L2 从
   0.65 继续拉起来、并让 L5 有复用证据的唯一办法。
6. **精读 ClaroAI-Bench 与 Co-Reviewer**，判断本项目的对象标准与第 4 层审查
   是否需要向外部已有约定靠拢——自定标准的采用成本远高于顺应既有约定。

---

## 6. 观察清单（用于后续日报的触发条件）

触发条件以 **ID 形式声明在 `scripts/compare_snapshots.py` 的 `TRIGGERS` 列表**中，
由 `compare_snapshots.py` 自动求值，并由 `scripts/check_report_mechanism.py` 校验
"代码声明"与"本节叙述"是否一致。**本节与代码必须同步修改**，否则机制检查会失败。

| ID | 触发条件 | 阈值 | 状态 | 承诺效果 |
|---|---|---|---|---|
| T1 | 本地修复仍未 commit（head 仍为 `abc9103` 且 pending > 0） | 2026-10-14 | pending | L2 −0.05、L3 −0.05 |
| T2 | Ref-01S 仍无实验室回复 | 2026-10-25 | pending | L1-lab → 0.25 |
| T3 | 出现第二个 Research Object 且被他人复核 | — | not met | L2 → 0.75、L5 → 0.40 |
| T4 | ClawsGO 或同类产品公布长时域指标 | — | not met（人工） | 据实重估 L1-agent |
| T5 | 出现取代 AutoLab 的新长时域基准 | — | not met（人工） | 据实重估 L1-agent 与门槛 A |
| T6 | 出现"探索图谱自动编译"公开实现（Ara L3 缺口被外部补齐） | 2027-02-01 | pending（人工） | 改为集成，L2 +0.05 |
| T7 | 出现把"审查状态机/发布门禁"与哈希冻结产物绑定的公开发表 | 2027-04-01 | pending（人工） | C2c 被抢概率 → 0.70 |
| T8 | 出现同参数的跨域/HAUV 垂直出水静水压基线 | 2027-04-01 | pending（人工） | 视为 C1 已被抢占 |
| T9 | A59 式对抗验证协议被领域期刊/会议正式采纳 | 2027-10-01 | pending（人工） | C2a 正式判为已抢占 |
| T10 | P003 Stage 1 的 CDFV-001 列仍有未解决的 `Blocked` 单元格 | 2026-11-10 | pending（已读数：**4**） | 判定研究问题被框架工作挤占，**冻结一切框架开发** |
| T11 | 仍无独立人工评审（`independent_human_reviews = 0`） | 2027-01-09 | pending（已读数：**0**） | Principle 5 判为"未制度化"，L4 → 0.15 |

> **T7–T9** 来自同行进度评估
> `Research_Log/2026-10-11_Peer_Progress_and_Scoop_Risk.md`；
> **T10–T11** 来自项目层决策
> `Research_Planning/Decision_Log.md` 的 `D-ANRI-001`（项目定位与资源分配）。
> 该文给出一个与本文**方向相反但不矛盾**的结论：本项目的基础设施主张被同行抢先发布的
> 概率约 **90%**（Ara/ARA 协议 2026-05、A59 对抗验证协议 2026-08 均已公开），
> 而"体系建成 + 大规模使用"的成功概率仅约 2–3%。两者可以同时成立：
> 一个几乎必然被抢的主张，与一个几乎不可能建成的体系。
>
> 该文的可操作结论：**C2a（"研究产物应 agent 原生/哈希冻结"这一主张）应放弃新颖性诉求**，
> 改为引用 Ara/A59 并把本项目定位为该协议在工程领域的实例化；
> 真正还剩的空间是 C2c（门禁与审查状态机绑定）与 C3（领域内采纳）。
>
> **通用化路线**另见 `D-ANRI-002`：以 EEM 闭环次数为唯一度量，分级 G1–G4 且禁止跳级。

---

## 7. 来源

- ClawsGO Science：[36氪 英文](https://eu.36kr.com/en/p/3995487329308552) ·
  [36氪 中文](https://m.36kr.com/p/3995487329308552)
- Ara: Agent-Native Research Artifacts：
  [论文 arXiv:2604.24658](https://arxiv.org/abs/2604.24658) ·
  [wiki 摘要](https://bayesiansapien.github.io/cere-bro/agentic-systems/2026-05-01-ara-agent-native-research-artifacts/)
- AutoLab 解读：
  [腾讯云开发者社区](https://cloud.tencent.cn/developer/article/2684253?policyId=1003)
- SLAC SPIRE：
  [SLAC](https://www6.slac.stanford.edu/news/2026-10-08-slac-leads-new-project-build-self-driving-laboratory-future)
- Google Co-Scientist：
  [DeepMind](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/)
- Google 学术工作流 agent：
  [Research Blog](https://research.google/blog/improving-the-academic-workflow-introducing-two-ai-agents-for-better-figures-and-peer-review/)
- OpenAI agentic 科学计算：
  [OpenAI](https://openai.com/zh-Hant-HK/index/scientific-computing-agentic-ai/)
- XtalPi Science：
  [科技日报](https://www.stdaily.com/web/gdxw/2026-07/30/content_556091.html)
- 上海超级科研工厂：
  [科技日报](https://www.stdaily.com/web/gdxw/2026-07/09/content_544682.html)
- AI4E 千卡集群（同济）：
  [科学网](https://paper.sciencenet.cn/htmlnews/2026/6/567167.shtm) ·
  [证券时报](https://stcn.com/article/detail/3983529.html)
- 百度 AI4S 科学家计划：
  [科技日报](https://www.stdaily.com/web/gdxw/2026-08/12/content_562839.html)
- ClaroAI-Bench：
  [EuropePMC](https://dev.europepmc.org/article/PPR/PPR1210202)
- SciAgentGym：
  [链接](https://xuanjing-huang.github.io/publication/sciagentgym-zh)
- Co-Reviewer：
  [Scientometrics](https://dl.acm.org/doi/10.1007/s11192-026-05557-6)
- Provenance / source-chain auditability：
  [Zenodo](https://zenodo.org/records/21330680/files/SIT-16-provenance-timestamp-source-chain-v2.pdf)

---

## 8. 方法论声明

- 本日报的**事实部分**仅来自：(a) 上述公开链接的正文，(b) 本地仓库可执行的
  实测命令与文件内容。二者在文中已分别标注。
- 本日报的**概率部分全部是判断**，不来自任何测量。分解因子、乘积检验与敏感度
  分析的作用是让判断可被审阅和逐日对比，而不是让判断变成事实。
- 二手解读（AutoLab、ClawsGO）已显式标注不确定性；未公开指标的一律不作为
  确定性证据使用。
- 每个后续日报应保持同一格式，并在第 4.5 节给出 Δ，在第 6 节检查触发条件。
- **事实数字的口径**：第 3 节与第 4.4 节引用的仓库度量一律取自同日
  `Research_Log/<date>_ANRI_State.json`，由 `scripts/collect_state.py` 从文件与
  命令退出码生成，不允许手工转述。该快照的 `generated_utc` 是墙钟时间、不参与
  跨日比较，其余字段可逐日 diff。
- **模板**：`Research_Log/Daily_Template.md` 固定了本日报的章节编号与顺序。
- **配套文档**：`Research_Log/2026-10-11_Peer_Progress_and_Scoop_Risk.md` 评估
  "成果被同行抢先发布"的概率（`scoop-v1` 口径），与本日报结论方向相反但不矛盾，
  其新增的 T7–T9 触发条件已并入 §6。
- **机制自检**：`py -3 .\scripts\check_report_mechanism.py` 校验"代码中的 TRIGGERS"
  与"日报 §6 的叙述"是否一致，并检查快照可解析、章节编号完整、日报中被提到的触发 ID
  全部真实存在。本日报通过该检查。
- **快照版本**：本日报引用的快照 `2026-10-11_ANRI_State.json` 会被同日多次采集覆盖
  （最近一次 `pending_entries = 102`、8 项检查全通过）。同日追加的
  `Daily_Template.md`、`2026-10-11_ANRI_Daily.md`、`2026-10-11_ANRI_State.json`、
  `scripts/collect_state.py`、`scripts/compare_snapshots.py`、
  `scripts/new_daily_report.py` 会使 `pending_entries` 继续上升；这些都是日报机制
  自身的产物，**不改变第 4 节的任何因子判定**。
  跨日比较时以「同日快照 + 当日日报」成对读取为准。
- **范围声明**：日报文件本身是日志，**不纳入** Research Object 的 `artifacts`
  哈希清单；否则每写一次日志都会移动对象与台账的哈希。纳入哈希清单的是研究证据
  （模型、结果、校验器、schema、评审报告、台账）。
