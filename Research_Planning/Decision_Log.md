# D002-001 — Whether to include free-surface loading

> 本文件是 ANRI-CDFV 的决策记录（Decision Log）。文件顶部保留 D002-001 作为原有锚点，
> 其余为按编号追加的决策条目。
>
> **阅读顺序建议**：先读 `D-ANRI-001`（项目定位与资源分配）与 `D-ANRI-002`（通用化
> 路线），再读 `D002-001`（具体物理问题）。前者约束后者的优先级，不改变后者的内容。
>
> 条目编号规则：`D-<跟踪号>-<序号>` 为一组决策；`D-ANRI-00x` 为项目层决策，
> `D002-001` 为领域层决策。

## Evidence

- E002-001
- P002 Section 4.1.2
- Fig. 11–12
- `Paper_Notes/P002_Free_Surface_Hydrodynamics_HAUV_2022.md` Table 1（p.5）、§4.2、§4.3
- `Research_Planning/P003_Free_Surface_Loading.md` §7.5（Path B 量纲筛选，2026-10-12）
- `Models/CDFV-001/Ref-01B/results/summary.csv`：满浸没浮力 20.1510694 N

## Observation

The reported suction force increases between approximately
0.1 and 0.25 m/s and becomes approximately stable above 0.25 m/s
within the tested range. The reported maximum is about **10% of vehicle weight
≈ 1.99 N** for the 2.030 kg P002 cylinder.

**2026-10-12 补充（Path B 量级检验）**：该 1.99 N 的量级**无法由动压解释**
（0.5 m/s 以内至多 0.127 N，占 6.4%），**无法由表面张力解释**
（σ·πD = 0.0206 N，占 1.03%）；准静态凹陷需 31.9 mm（9.9% L）偏大。
量级自洽的解释是**空腔体积亏缺**：气腔使实际排水体积低于静水线暗示值，
需损失约 9.9% 总排水体积（= 满浸没浮力 20.151 N 的 9.9%）。
该假说同时解释饱和行为（几何机制而非动压机制）。**尚无反演证据。**

## Decision Candidate（2026-10-12 修订）

**原表述**：CDFV-001 transition analysis should compare a baseline model
against a model containing a **velocity-dependent** free-surface term.

**修订后**：自由液面贡献应按**无量纲判据**处理，而非按速度区间处理。
迁移的判据是三者是否可比：
`Froude 数区间 + 机体有效密度比 ρ_w/ρ_body,eff + 几何`。
若可比，则 `F_suction/W` 与尺度无关（空腔体积与排水体积同为 L³）；
若不可比，则 P002 的载荷量级不可迁移。

**修订理由**：动压解释已被量级判除，故"velocity-dependent"这一机理描述不成立。

## Status

**Needs CDFV experiment** — 附条件（记录日期 2026-10-12）

**为何不是 Accepted 或 Rejected**：两者都要求已知 CDFV-001 的机体有效密度
`ρ_body,eff = m_body / (πD²L/4)`，而该量在本仓库中不存在
（CDFV-001 几何与质量参数缺失，实测依据见
`Research_Planning/P003_Stage1_Sourcing_Checklist.md` §0）。
在缺少该量的情况下记 Accepted 或 Rejected 均属**用推测替代事实**，
违反 `P003_Free_Surface_Loading.md` §6 与 §11 的禁止条款。

## Next Action

1. **执行 B1（推荐）**：同一几何、两种尺度、**相同 Froude 数**下测 `F_suction/W`，
   直接检验"该比值与尺度无关"这一迁移所依赖的不变量。
   不需要先确认空腔机制，也不需要 Stage 1 的四个 CDFV 参数。
   - 比值一致 → D002-001 转为 **Accepted**（附无量纲适用条件）；
   - 比值不一致 → 转为 **Needs CDFV experiment（无条件）**。
2. 取得 CDFV-001 的机体有效密度（按 `P003_Stage1_Sourcing_Checklist.md` §3），
   用于最终的 material / immaterial 判定。
3. `KU003-001`（`P003_Free_Surface_Loading.md` §13）在 D002-001 转为 Accepted 时
   由 proposed 转为 active。

---
---

# D-ANRI-001 — 项目定位与资源分配：从"基础设施新颖性"转向"工程实例化"

## 元数据

- 决策 ID：`D-ANRI-001`
- 日期：2026-10-11
- 状态：**Accepted**
- 决策类型：项目层定位与资源分配
- 依据文档：
  - `Research_Log/2026-10-11_ANRI_Daily.md`（体系建成概率评估，口径 `v1`）
  - `Research_Log/2026-10-11_Peer_Progress_and_Scoop_Risk.md`（被抢先概率评估，口径 `scoop-v1`）
- 关联决策：`D-ANRI-002`（通用化路线，受本决策约束）

## 背景

同日两份独立评估给出**方向相反但不矛盾**的结论：

| 问题 | 结论 |
|---|---|
| 五层体系建成 + 大规模使用的概率 | 约 **2–3%**（5 年） |
| 基础设施主张被同行抢先发布的概率 | 约 **90%**（其中 C2a 主张已达 95%，即已发生） |

被抢先不是推测：以下工作已公开发表，覆盖了本项目"验证装置"层（C2）的核心主张：

- **A59 对抗验证协议**（Zenodo, 2026-08-25）：预注册 + 密码学哈希冻结规则、
  冻结基准零损失回归门禁、**执行者/验证者分离 + 强制暂停点**、
  **人类领域专家锚点（任何 AI 在环者不得评分该测量）**、errata-forward。
  由**单人**研究程序完成。
- **Ara / ARA 协议**（arXiv:2604.24658, 2026-05）：四层 agent 原生研究产物
  （科学逻辑 / 可执行代码 / 探索图谱 / 证据落地）+ 三件生态工具，并给出量化收益。
- **MIRROR 本地证据包**（Zenodo 20463358）、**Barba《可复现性即上下文工程》**
  （arXiv:2609.11728, 2026-09-10）、**ClaroAI-Bench**（bioRxiv 2026-05-12）。

关键判断：继续以"提出一种新的研究产物协议"为诉求，是在一个**已被占据且进入
生态化竞争**的位置上作业。

## 决策

**1. 放弃基础设施新颖性诉求（C2a）。**
不再把"研究产物应 agent 原生 / 哈希冻结"作为本项目的贡献主张。
改为直接引用 Ara 与 A59 作为既有工作，本项目定位为该协议在**跨域飞行器工程领域**
的**首个实例化**，并公开该流程在工程场景下的失效模式。

调整后的主张表述：

> 用哈希验证的 agentic 流程回答"跨域飞行器出水自由液面载荷能否从 P002 迁移"，
> 并公开该流程在工程物理场景下的失效模式与人工锚点需求。

**2. 项目主指标从"体系完备度"改为"研究问题闭合度"。**
主指标为 `D002-001` 是否被判定为 **Accepted / Rejected / Needs CDFV experiment**，
而非验证器层数或覆盖面。体系仅为达成该指标的手段。

**3. 冻结验证框架的扩张。**
在 P003 的 Stage 1 参数表填满之前，不再新增对抗案例、负例、门禁场景或校验器分支。
理由：现有装置（12 对抗 + 18 负例 + 13 门禁自测 + CI 状态门禁 + 机制自检）**已超过
当前单一研究对象的需要**；继续扩张即违反 `P003_Free_Surface_Loading.md` §4 明确排除的
"Building an AI agent or a complete ROS platform"。

**4. 建立"卫生设施 ≠ 研究产出"的汇报纪律。**
快照采集、快照比较、日报生成、机制自检等属卫生设施（infrastructure hygiene），
其作用是让结果可信，**不作为成果汇报**。

**5. 采用 A59 的人类锚点规则为流程约束。**
"不得让任何 AI 在环者给自己的输出评分，且每条关键链条中至少一项测量保留给
完全不在 AI 环内的人类。" 该规则与 `docs/ANRI_Principles_v0.1.md` **Principle 5**
一致，差别在于**必须由系统强制**而非口头承诺。

> 更正记录：`2026-10-11_Peer_Progress_and_Scoop_Risk.md` §2.1 曾将"人类锚点"列为
> 本项目缺口。经复核 `docs/ANRI_Principles_v0.1.md`，**Principle 5 早已记载该原则**
> （"Human expertise remains part of the loop"）。准确表述是：
> **原则已具备（2026 年前），但未制度化（`independent_human_reviews = 0`）。**

## 依据（事实，全部可在仓库内复核）

- `git log -1` = `abc9103`；修复工作已 staged 但未 commit（`pending_entries = 104`）。
- `Research_Objects/RO-CDFV-001-Ref-01B.json`：1 个对象、1 个 claim、3 个 evidence、
  64 个哈希注册产物、`review.status = revision_requested`、
  `independent_human_reviews = 0`。
- `Research_Planning/P003_Free_Surface_Loading.md` Stage 1 对比表中，
  CDFV-001 侧四个参数（出水速度 / 质量重量基准 / 主体几何 / 过渡姿态）
  **全部为 "Blocked — source required"**。
- `Knowledge_Base/CDFV_Knowledge_Map.md` §5 EEM 回环
  （Knowledge → Design → Simulation → Evaluation → Knowledge Update）**从未闭合过一次**。

## 影响（概率，判断而非测量）

| 贡献 | 被抢先概率 | 处理方式 |
|---|---:|---|
| C1 领域静水压基线 | 78% / 12 个月 | 尽快提交以锁定优先权，作为体系的载荷使用 |
| C2a "产物应 agent 原生/哈希冻结"主张 | 95%（已发生） | **放弃主张**，改为引用 Ara/A59 |
| C2b 对抗+负例+CI 门禁装置组合 | 72% / 12 个月 | 不主张新颖性，作为实现细节 |
| C2c 门禁与审查状态机绑定 | 45% / 12 个月 | 保留为唯一窄主张，但不独立成篇 |
| C3 五层体系 + 大规模使用 | 20% / 24 个月 | 真正的护城河，资源应转向采纳 |

以上数字均取自 `2026-10-11_Peer_Progress_and_Scoop_Risk.md` 的 `scoop-v1` 口径，
**应视为下界**（检索存在固有盲区：审稿中稿件、未公开预印本、非英文文献）。

## 执行顺序（按杠杆排序，不按难度）

1. **填满 P003 Stage 1 的四个 CDFV 参数**（每个要么有来源，要么显式 Blocked）。
   这是唯一完全受本项目控制、且解锁全部后续工作的动作。
2. 提交已 staged 的 104 项修复（`head` 仍为 `abc9103`，"可复现"对第三方尚不可见）。
3. 完成一次**真实独立人工评审**并署名（落实决策 5）。
4. 提交 C1 计算基线锁定优先权，表述按决策 1 重新定位。

## 可测的判定条件

| 条件 | 阈值 | 未达成的后果 |
|---|---|---|
| P003 Stage 1 四个参数填满 | 30 天内（至 2026-11-10） | 判定研究问题被基础设施工作挤占，**暂停一切框架开发** |
| `independent_human_reviews ≥ 1` | 90 天内（至 2027-01-09） | Principle 5 判定为"未制度化"，`L4` 下调至 0.15 |

以上两条已作为触发条件 `T10`、`T11` 登记于
`scripts/compare_snapshots.py` 的 `TRIGGERS` 列表，并由
`scripts/check_report_mechanism.py` 校验"代码声明"与"日报 §6 叙述"一致。

## 风险与控制

| 风险 | 控制 |
|---|---|
| 基础设施完美主义挤占研究时间 | 决策 3（冻结扩张）+ 条件 T10 |
| 在同一日内反复修订文档以制造进展感 | 决策 4；跨日 Δ 与"日内修订"在日报中分开记录 |
| 自定标准导致后续无法与 Ara/A59 互操作 | 决策 1 改为采用既有约定，迁移成本不随领域数增长 |
| 过度承诺（把体系说成已建成） | 主张表述按决策 1 收紧；`review.status` 保持在 `revision_requested` 直至新评审 |

## 下一步

按"执行顺序"第 1 项推进 P003 Stage 1；同时把本决策的约束反映到
`Research_Planning/Active_Questions.md` 的 AQ001 里程碑中。

## 复核日期

2026-11-10（与 T10 同步），或 P003 Stage 1 完成时，以先到者为准。

---
---

# D-ANRI-002 — 通用化路线：EEM 闭环挣得式推进

## 元数据

- 决策 ID：`D-ANRI-002`
- 日期：2026-10-11
- 状态：**Accepted**
- 决策类型：长期路线与门槛设定
- 上游决策：`D-ANRI-001`（本决策受其约束，且**不得先于其执行**）
- 依据文档：`docs/ANRI_Evolution_Path.md`、`Knowledge_Base/CDFV_Knowledge_Map.md` §5、
  `Research_Log/2026-10-11_Peer_Progress_and_Scoop_Risk.md`

## 背景

`docs/ANRI_Evolution_Path.md` 已记载通用化路线图：

```
ANRI v0.1  AI-assisted Engineering Workflow
   ↓
ANRI v1.0  Agentic Engineering System
   ↓
ANRI v2.0  AI Creates Engineering Platform
   ↓
ANRI v3.0  Cross-domain AI Research Infrastructure
```

`Knowledge_Base/CDFV_Knowledge_Map.md` §5 的 EEM
（Knowledge → Design → Simulation → Evaluation → **Knowledge Update**）是领域无关的，
即**通用化的真正载体**。其研究问题是："工程知识如何累积？设计经验如何可复用？
AI 如何加速工程演化？"

## 问题的答案：可以，但顺序不可颠倒

### 三种"通用化"含义，命运完全不同

| 含义 | 内容 | 现状判定 |
|---|---|---|
| **技术通用化** | 哈希冻结、对抗验证、负例、CI 门禁搬到其他领域 | **已经通用，且不需要本项目发明**——Ara/A59 已公开。可直接引用采用。 |
| **领域通用化** | AQ001 的结论迁移到其他跨域平台 | **声称可以，证据为零**。`P003` §5 H3 假设已指出："P002 圆柱拟合不能在未做几何或实验修正的情况下数值迁移到 CDFV-001"。 |
| **设计推理通用化（EEM）** | 跨问题、跨平台的决策与知识更新累积 | **无人在此位置**，但只能由前两者的实际积累长出。 |

关键技术区分：**Ara 的探索图谱是"单篇论文内"的；A59 是"单一领域"的；本项目的
AQ001→AQ002→AQ003 依赖链是"跨问题累积"的。** 三者不冲突，本项目的位置在第三层。

### 一个真实的不对称优势，与随之而来的风险

**优势**：跨域飞行器的核心难题（AQ001：气水过渡期间物理特性如何变化）**本身就是
一个"跨物理域迁移"问题**。专业化过程所练的正是通用化所需的能力——判断一个域内的
结论在什么边界外失效。

**风险**：迁移性结论的典型形态是"某些结构可迁移、系数不可迁移"（本项目的 H3 正是
此形态）。这类结果真实且有用，但**通用性弱**——它给出的是边界条件，不是普适规律。
不得把"边界条件结论"包装为"通用规律"。

## 决策

**1. 通用化必须"挣得"，不得"设计"。**
禁止以自定标准做通用化的起点。理由：框架先行位置已被 Ara/A59 占据并进入生态化竞争，
且以新格式要求他人采纳的起点，是"无业绩记录的新标准"。

**2. 通用层不重新设计，直接采用既有标准。**
产物结构采用 Ara/ARA 协议，验证规则采用 A59（含"不得让 AI 在环者给自己的输出评分"
与人类锚点要求）。本项目的贡献限定为三样：**工程实例、失效报告、累积记录**。
此定位把本项目从"竞争者"变为"采用者"——这是弱方唯一可持续的站位。

**3. 以 EEM 闭环作为通用化的唯一度量。**
通用化程度 = **EEM 环闭合并通过验收的次数**，不是框架完备度、不是代码行数、
不是文档数量。

**4. 分级门槛 G1–G4，逐级以"上一级产出物"为输入。**
禁止跳级；禁止以"计划"充当下一级的输入。

| 阶段 | 内容 | 概率（判断） | 时间窗 | 进入条件 |
|---|---|---:|---|---|
| **G1** | 在 CDFV-001 上闭合 EEM 一次（产出 `KU003-001` + `D002-001` 判定） | **65%** | 6 个月 | `D-ANRI-001` 执行顺序第 1 项完成 |
| **G2** | 同一领域内第二个问题复用同一流程 | **30%** | 12 个月 | G1 产出物存在 |
| **G3** | 第二个物理域（热 / 结构等）复用 | **12%** | 36 个月 | G2 通过 |
| **G4** | 第三条依赖链自发进入（他人开始使用） | **5%** | 60 个月 | G3 通过 |

概率为判断而非测量；逐级衰减，且**G1 是唯一完全受本项目控制的一步**。

## EEM 闭环的验收标准（G1 判据）

沿用 `P003_Free_Surface_Loading.md` §9 已定义的验收条件，并明确其作为 EEM 首次闭合的
判定：

1. 结果落入 **material / immaterial-within-range / unresolved** 三者之一（必须显式声明）；
2. `Research_Planning/Decision_Log.md` 中 `D002-001` 被更新为
   **Accepted / Rejected / Needs CDFV experiment**；
3. 产出 `KU003-001` 知识更新条目（含 Before / After / Evidence / Validity range /
   Open limitation）；
4. 每个结论可追溯到来源文件、章节/图表、几何与工况、坐标系与单位、
   实测/数字化/计算/推断状态。

**不通过的情形**：仅得出"P002 表明这很重要"。`P003` §9 已明确排除该结论形态。

## 依据（事实）

- `Knowledge_Base/CDFV_Knowledge_Map.md` §5 已写出 EEM 回环与研究问题（领域无关）。
- `docs/ANRI_Evolution_Path.md` 已写出 v0.1→v3.0 通用化路线。
- `P003_Free_Surface_Loading.md` §9/§10/§13 已定义验收标准、预期产出与知识更新模板。
- **该环从未闭合过一次**：`Research_Objects/` 仅有 1 个对象，
  `Research_Planning/Decision_Log.md` 中 `D002-001` 仍为 `Candidate`，
  `KU003-001` 不存在。
- `docs/ANRI_Principles_v0.1.md` Principle 4（"Knowledge must be cumulative"）
  与本决策目标一致，同样处于"已记载、未制度化"状态。

## 风险与控制

| 风险 | 控制 |
|---|---|
| 在 G1 未闭合时讨论 G3/G4，注意力从阻塞点转移 | 本决策的第 4 条门槛 + `D-ANRI-001` 条件 T10 |
| 把迁移结论包装成普适规律 | 第 2 条定位 + H3 的显式限定；结果必须声明 validity range |
| 自定通用标准导致跨领域迁移成本累积 | 第 2 条：采用 Ara/A59 既有约定 |
| 用"框架更完备"冒充"通用化进展" | 第 3 条：度量仅取 EEM 闭合次数 |

## 下一步

本决策**不产生任何立即动作**。其作用是：在 G1 完成前，任何"通用化 / 平台化 /
体系化"提案都应先对照本决策第 4 条门槛，判定其属于哪一级、以及该级的进入条件
是否已满足。

## 复核日期

G1 闭合时，或 2027-04-11（6 个月），以先到者为准。

---

# D-ANRI-003 — 人力约束与 EEM 规模化的真实瓶颈

- **日期**：2026-10-13
- **状态**：**Accepted**
- **触发**：`D-ANRI-002` 的规模化路线在讨论"EEM 如何大规模实现"时缺少人力前提

## 已核实的事实（用户 2026-10-13 提供）

- **可用人力**：同项目同学（可直接投入）
- **不可直接获得**：业内人士 / 实验室专业人员——**需要单独申请**（机构级流程）
- 同学在该领域的专业水平：**未确认**（用户未说明，本决策不假设）

## 本决策的核心区分

人力必须按**用途**分成两类，二者的难度差一个数量级，且互相**不可替代**：

| 用途 | 谁能做 | 获取难度 | 可否并行 | 对应的层 |
|---|---|---|---|---|
| **生产性人力**（建模、验证器、基准、文档、复现脚本） | 同学可胜任 | 低 | ✅ 可并行 | L1–L3、L5 |
| **判断性人力**（语义级评审、量纲/物理合理性挑战、反例构造） | 需要领域专业能力 | **高（需申请）** | ❌ 近乎串行 | **L4** |

**结论：项目的瓶颈不是生产性人力，而是判断性人力。**

依据：本仓库 `independent_human_reviews = 0`、`loops_closed = 1`，而 2026-10-11 至 10-13
的实质工作显示，时间主要消耗在"让验证站得住"（验证器、负例、对抗用例、门禁、CI），
而非知识获取或建模本身。生产性工作**可以**分给同学；L4 不能。

## 决策

1. **对同学**：按生产性人力使用，优先做"已定义、可验收、不依赖领域判断"的任务；
   任务书必须自带验收判据（本仓库已有形态：负例套件、对抗用例、门禁自测）。
2. **对业内人士 / 实验室**：**只在 L4 任务上使用申请得来的机会**，
   不得用于问"项目好不好"这类问题。
   申请时必须附**一个具体、可执行、专家能回答的验证任务**；
   本仓库现成的候选是 `Research_Planning/P003_B1_Preregistration.md`
   （它不需要先理解 ANRI，即可被领域专家评审其相似性与判据）。
3. **同学可先充当 P2 级评审**（同项目、同水平）：可查笔误、单位、逻辑跳跃、
   命名不一致、README 与代码不符等机械与常识层问题。
   **但 P2 不能替代 L4**：独立性不足（同项目、同知识基础），且缺少领域判断能力。
4. **不得**把"同学看过了"记为 `independent_human_reviews ≥ 1`。
   该计数器只统计**不在本项目内**的评审者（`D-ANRI-001` 决策 5 已要求真人
   且不在 AI 环内；本决策补充：也不在本项目内）。

## 立即执行的实验：清室复现（clean-room replication）

用同学做一次**零培训测试**，同时验证两件事：

| 目的 | 判据 |
|---|---|
| 文档是否自足 | 只给 `docs/ANRI_Principles_v0.1.md`、`schema/research_object.schema.json`、`scripts/`、`P003_B1_Preregistration.md`，**不做口头解释**，同学能否产出一个通过 `validate_research_object.py` 的对象 |
| 是否可复制 | 上述过程中，人类介入次数与类型（判断？还是纯机械？） |

**成功判据**：能在**不需用户解释**的情况下跑通校验器。
- 若成功 → 获得"可复制"的**实测**证据，这是 `D-ANRI-002` G2 的前置；
- 若失败 → 得到一份**具体的文档缺口清单**，这本身就是 G1 产出的合法延伸。

## 对概率的修正

**维持门槛 A = 82%（本日修正后为 84%），但下调 L1-agent 0.80 → 0.78。**
理由：同学是可用的生产性人力，但**同为新手**，近期产出速度与质量方差都会上升。
两者近似抵消，故总体仅上调 2 个百分点（见当日日报 §4）。

**不得**因为"有人了"而上调 `L4` 或门槛 B：本次信息没有改变
"无外部判断性人力"这一事实。

## 复核日期

清室复现实验有结果时，或 2026-11-13（1 个月），以先到者为准。

---

# D-ANRI-004 — 默认分支门禁建成，以及冷启动暴露的两个缺陷

- **日期**：2026-10-19
- **状态**：**Accepted**
- **触发**：`main` 首次具备**强制**门禁；随后冷启动验证暴露两处"只在有 `.git`
  的工作副本里成立"的缺陷

## 一、事实（全部由仓库与本会话命令实测）

### 1.1 门禁建成

`main` 上的规则集（ruleset id `25410404`）现有四条生效规则：

| 规则 | 作用 | 实测方式 |
|---|---|---|
| `deletion` | 禁止删除 `main` | `GET /rules/branches/main` 返回该 type |
| `non_fast_forward` | 禁止强推 | 同上 |
| `pull_request` | 强制走 PR（approvals = 0） | 同上 |
| `required_status_checks` | 必须 `validate` 绿（strict = true） | 同上，`check: validate` |

**建成的证据**：一次直推 `main` 被 GitHub 明确拦下并打印

```
remote: Bypassed rule violations for refs/heads/main:
remote: - Changes must be made through a pull request.
```

即**规则在拦人，只是因为 admin 在 bypass list 才放行**。

### 1.2 CI 首次在默认分支通过

`main` 的 `6754cfe`（PR #1 合并提交）触发 `push` 事件，
`ANRI validation` 12 步**全部 success**。这是本仓库历史上第一次默认分支通过门禁。

### 1.3 冷启动暴露缺陷 A：产物里写进了随检出位置变化的路径

用 `git archive` 导出 tag `v0.2-gate-live`（**无 `.git`**）后运行门禁：

| 检查 | 结果 |
|---|---|
| RO validator | exit 0 |
| clean baseline | exit 0 |
| negative cases | exit 0 |
| report mechanism | exit 0 |
| **drift check** | **exit 1** |

根因（实测差异）：

```diff
- 源仓库: "results_directory": "Models/CDFV-001/Ref-01B/results"
- 导出树: "results_directory": "AppData/Local/Temp/anri-cleancheck/Models/CDFV-001/Ref-01B/results"
```

`verify_baseline.py` 的 `repository_root()` 靠**向上查找 `.git`** 定位仓库根。
导出树无 `.git` 时它退化为模型目录，于是结果目录"看起来"在根之上，
`relative_to` 算出带 `../` 的路径并写入 `verification.json`——
**而该文件是哈希注册产物**。

**推论（判断）**：修复前，本仓库**只能在保留 `.git` 的工作副本里通过校验**。
任何拿到导出树（tag 的 zip、`git archive`、镜像）的人都会看到哈希不符。

**修复**：`to_posix_relative` 把"逃出仓库根的相对路径"视为无法表达，
退化为稳定目录名。验证：同一导出树上 `drift exit=0`、`RO validator exit=0`。

### 1.4 冷启动暴露缺陷 B：完整克隆在本机网络下失败

| 方式 | 耗时 | 结果 |
|---|---|---|
| `git clone --depth 1 --branch <tag>` | **795 s** | ❌ `early EOF` / `unexpected disconnect` |
| `git clone --filter=blob:none --no-checkout` | **4.0 s** | ✅ 成功 |

体积分布（`git ls-tree -r -l HEAD` 实测）：

| 目录 | 体积 | 占比 |
|---|---:|---:|
| `Paper_Library`（2 个 PDF） | 32.92 MB | **62.8%** |
| `Benchmarks`（46 个哈希冻结产物） | 17.50 MB | 33.4% |
| 其余全部 | ~2% | ~3% |

**`Paper_Library` 中的 PDF 不在 RO 注册清单内**（注册数 0），
而 `Benchmarks` 的 46 个产物全部冻结、不可删。

### 1.5 处置：离线 bundle

已生成并验证 `git bundle create --all`，30.2 MB，`git bundle verify` 报
"The bundle records a complete history."。恢复不依赖网络。

## 二、决策

1. **阈值 A 的门槛含义改变**：从"有校验脚本"变为"默认分支强制执行校验"。
   这是 L4 第一次具备**强制力**，而不是仅有工具。日报口径应据此更新，但
   **不得据此上调 L4 或门槛 B**——`independent_human_reviews` 仍为 0，
   门禁的强制力约束的是"提交路径"，不是"判断性人力"。
2. **`admin bypass` 必须显式披露**。准确表述：
   > `main` 受规则集保护，强制经由 PR 且禁止删除与强推；
   > 仓库管理员保留可审计的 bypass 权限。
   **禁止**对外声称"绝对不可绕过"或"证据不可篡改"。
3. **冷启动必须成为常规检查**，且**必须在无 `.git` 的导出树上做**。
   CI 永远抓不到缺陷 A 这类问题，因为 `actions/checkout` 总是提供 `.git`。
4. **`Paper_Library` 的 PDF 建议移出版本控制**，但**本次未执行**——
   属于用户决策（涉及"仓库是否能独立分发论文"），不擅自处置。
5. **每次重要节点后生成一次离线 bundle**，作为"机器故障"这一具体风险的直接对策。

## 三、本决策不改变的事

- **不改变** `D-ANRI-001` 的定位判断（放弃基础设施新颖性）。
- **不改变** `D-ANRI-002` 的 G1–G4 门槛。`loops_closed` 仍为 **1**。
- **不改变**门槛 A/B 的数值口径。本次是过程改进，不是研究进展。
- **不声称**上游因本次工作而改变评价。Sakana 等同类工作已公开，
  这是 `D-ANRI-001` 既有判断的强化，不是新发现。

## 四、遗留缺陷（已知未修）

1. **`main` 分支的旧 `.gitattributes` 遗留**：`* text=auto eol=lf` 与
   `*.csv text eol=lf` 会把 CRLF 内容的注册产物判定为 modified，
   **即使字节完全相同**。这在本会话中真实阻塞过一次 fast-forward 合并，
   当时用 `.git/info/attributes` 临时 `-text` 绕过（未提交、未推送）。
   `feat` 上的 `* -text` 已修复该规则，但**旧规则仍留在 `main` 的历史里**。
2. **`required_approving_review_count = 0`**：当前强制走 PR，但不要求第二人签字。
   这与"仅作者一人"的人力现实相符，但**不等于拥有了独立评审**。
3. **`Paper_Library` 体积问题未处置**（见决策 4）。

## 复核日期

2026-10-26（一周），或首次出现"默认分支 CI 红"、或清室复现结果返回时，以先到者为准。

---

# D002-002 — 是否需要在 CDFV-001 过渡模型中包含附加质量

> **这是 P004（`D-ANRI-002` G2 的第二个研究问题）的决策条目。**
> 与 `D002-001` 同属领域层决策，编号同族。

- **日期**：2026-10-19
- **状态**：**Needs CDFV acceleration profile**（附条件）
- **上游**：`Research_Planning/P004_Added_Mass_Screening.md` §5、§6
- **知识更新**：`KU004-001`（active）

## Evidence

- `Models/CDFV-001/Ref-01B/README.md` L76：`drag is omitted, and added mass is omitted`
- `Models/CDFV-001/Ref-01B/baseline_model.py` L4–L10、L99、L118–119
- `Models/CDFV-001/Ref-01B/results/Ref-01B-B-*.csv`：加速度列实测统计
- `Research_Planning/CDFV-001_Reference_Configuration.md`：D/L/m/ρ/g
- `Paper_Notes/P002_...md` §4.2：加速度实测区间 0.07–0.15 m/s²
- `Research_Planning/P004_Added_Mass_Screening.md` §5.2–§5.3

## Observation

Ref-01B 的三个速度工况（4846 / 1940 / 971 行）的 `acceleration_m_s2`
**各只有一种取值：0.0**。源码自述为 prescribed-motion、constant upward velocity。

附加质量力 ∝ 加速度，故其在 Ref-01B 中**恒为零**。

## 关键推论

**基线"排除附加质量"这一选择，是零加速度的副产品，而不是量级论证的结果。**
这两件事在过去被视为同一件事，本次筛选把它们区分开了。

## Decision Candidate

**原表述（隐含）**：CDFV-001 过渡模型可以像 Ref-01B 一样省略附加质量。

**修订后**：**是否包含附加质量，取决于过渡过程的加速度区间**，
而不是取决于"Ref-01B 省略了它"。判据是：

```
a_break-even = F_threshold / (C_a · ρ_w · scale)
```

- 若过渡峰值加速度 **≲ 0.15 m/s²**（P002 实测区间）→ 可省略
  （ΔF ≤ 4.3% 体重，面控制模型 C_a=1.0）
- 若 **≳ 1–3.5 m/s²** → 不可省略（ΔF 与吸入力同级）
- 两者之间 → **需要具体计算，不能靠经验判断**

## Status

**Needs CDFV acceleration profile** — 附条件（记录日期 2026-10-19）

**为何不是 Accepted 或 Rejected**：两者都要求已知 CDFV-001 的过渡加速度剖面，
而该量**不存在**（与 `D002-001` 的 CDFV 几何缺口同类）。

### 内部工作完成状态（2026-10-20 更新）

**本决策项内部可做的工作已全部完成。** 清单：

| 步骤 | 状态 | 产出 |
|---|---|---|
| Stage 1 量纲筛选 | ✅ 完成 | `P004_Added_Mass_Screening.md` §5 |
| `C_a` 的物理依据 | ✅ 完成（推导，非引用） | `P004_Added_Mass_Coefficient.md` |
| 加速体积尺度裁决 | ✅ 完成 | `A-P004-002` 已定为端面尺度 |
| 细长体适用性检验 | ✅ 完成 | `P004_Slender_Body_Applicability.md` |
| Stage 2 非零加速度基线 | ✅ 完成 | 6 个新工况，9 工况全 PASS |
| 三态结论 | ✅ `unresolved`（含条件） | 见 `P004_Added_Mass_Screening.md` §6 |
| 知识更新 | ✅ `KU004-001`（active） | `P004_Added_Mass_Screening.md` §10 |

**当前判据（两法夹逼后的最终值）**：

```
m_a  = 0.130 – 0.243 kg     （椭球下界 … 圆盘上界，比值 1.87）
a_be = 8.19 – 15.28 m/s²    （0.84 – 1.56 g）
```

**剩余的唯一外部未知量是 CDFV-001 的过渡加速度剖面。**
在此之前继续投入内部工作**不会有新结论**，只会重复已有推导。

### 仍需外部输入的三个子问题

1. **CDFV-001 加速度剖面**（决定性）：决定 material / immaterial 的最终归属；
2. **真实平端圆柱的 `m_a` 数值解或文献表**：本日检索工具全部失效，
   现有值是两渐近的夹逼而非该几何的解；
3. **锐边分离的定量影响**：若分离使 `m_a` 超过圆盘值，
   则 `0.243 kg` 是下限而非上界，`a_be` 会低于 0.84 g。

**这三项都不是本项目内部能解决的，且第 1 项与 `T10` 属同一类外部缺口。**

## Reason

1. 在唯一有实测支撑的加速度区间内（0.07–0.15 m/s²），ΔF 最多为吸入力的
   **4.3%**，支持"可忽略"。
2. 但该区间是**实验约束的产物**（P002 为避开 ≥0.2 m/s² 的平台振动），
   **不是 CDFV-001 的自然下限**。
3. 快速出水或抛放可达**亚 g 到 g**，即 P002 区间的 65–140 倍；
   在那个区间 ΔF 会与吸入力同级甚至更大。
4. 因此"可忽略"是**区间内成立、区间外不成立**的结论，必须条件化表述。

## New assumptions

- **A-P004-001**（2026-10-20 修订）：**`m_a ≈ 0.243 kg`**（势流圆盘首阶解
  `(8/3)ρR³`，`m_a/m_body = 0.120`）；端面归一化下 `C_a = 0.424`，
  体积归一化下 `C_a = 0.118`。**待文献核实**——检索工具本日全部失效，
  未能取得标准表。详见 `Research_Planning/P004_Added_Mass_Coefficient.md`。
- **A-P004-002**（2026-10-20 已裁决）：轴向附加质量 ∝ `R³`，**应使用端面尺度**；
  `A·L` 归一化只是同一物理量的另一种写法，不是另一个模型。

## Next Action

1. **Stage 2（最便宜）**：给 `simulate_case()` 增加恒定加速度运动学
   （`row_for_state()` 的力平衡层**已支持** `m·a`，见 L99/L118–119），
   跑 a = 0.1 与 1.0 m/s² 两个工况，产生可检验的非零加速度基线。
   **注意**：新增 `results/*.csv` 是哈希注册产物，须连带重新生成 RO 与 manifest。
2. ~~**核实 `C_a`**：回查附加质量标准表~~ — **2026-10-20 部分完成**。
   已从经典势流理论给出 `m_a ≈ 0.243 kg`（`P004_Added_Mass_Coefficient.md`），
   盈亏平衡加速度由 3.5–34.8 收窄为 **8.19 m/s²（0.84 g）**。
   **仍未取得可引用的标准表**（检索工具当日全部失效），故 A-P004-001
   标记为"推导值，待引用核实"，而非"引用值"。
3. **取得 CDFV-001 的加速度剖面**（与 `T10` 同一类外部缺口）。
4. 若 Stage 2 显示 ΔF 在 a=1.0 时确实与吸入力同级，
   则 `D002-002` 转为 **Accepted**（附加质量必须保留）。

## 复核日期

Stage 2 完成后，或 2026-11-19（1 个月），以先到者为准。

---
---

# 修订记录

| 日期 | 条目 | 变更 | 原因 |
|---|---|---|---|
| 2026-10-11 | `D-ANRI-001` | 新建 | 两份同日评估（体系建成概率 / 被抢先概率）给出方向相反的结论，需要一次定位与资源分配决策 |
| 2026-10-11 | `D-ANRI-002` | 新建 | 回答"专业化之后能否向通用化进军"，并设定 G1–G4 门槛以防跳级 |
| 2026-10-11 | `D-ANRI-001` | 更正 | 原报告称"人类锚点"为本项目缺口；复核发现 `ANRI_Principles_v0.1.md` Principle 5 早已记载该原则，准确表述为"已具备、未制度化" |
| 2026-10-12 | `D002-001` | **状态更新**：`Candidate` → `Needs CDFV experiment`（附条件） | P003 Path B 量纲筛选完成：1.99 N 无法由动压（≤6.4%）或表面张力（1.03%）解释，空腔体积亏缺假说量级自洽；因 CDFV 机体有效密度未知而无法记 Accepted/Rejected |
| 2026-10-12 | `D002-001` | **Decision Candidate 修订**：删除"velocity-dependent"机理描述，改为无量纲判据（Fr + 有效密度比 + 几何） | 动压解释已被量级判除，原机理表述不成立 |
| 2026-10-12 | `D002-001` | **Next Action 具体化**：改为可执行的 B1（同几何两尺度、同 Fr_D 测 `F_suction/W`） | Path B 结论要求把"是否需要专用实验"转化为可检验的判据，而非继续讨论 |
| 2026-10-13 | `D-ANRI-003` | 新建 | 用户提供人力约束：同学可直接投入，业内人士/实验室需单独申请。据此把人力区分为"生产性"与"判断性"，并指出瓶颈在后者（L4） |
| 2026-10-19 | `D-ANRI-004` | 新建 | `main` 首次具备强制门禁（四条规则）；冷启动暴露产物路径随检出位置变化、以及完整克隆在本机网络下失败两个缺陷 |
| 2026-10-19 | `D002-002` | 新建 | P004（G2 第二个研究问题）Stage 1 完成：发现 Ref-01B 加速度恒为 0，故"省略附加质量"是匀速的副产品而非量级论证；状态记为 Needs CDFV acceleration profile（附条件） |

> **EEM 闭环记录**：2026-10-12 的 `D002-001` 更新构成 `Knowledge → Design → Simulation →
> Evaluation → Knowledge Update` 环在本仓库的**第一次闭合尝试**。
> 对照 `D-ANRI-002` 的 G1 判据：
>
> | G1 判据 | 状态 |
> |---|---|
> | 结果落入 material / immaterial-within-range / unresolved 之一 | ✅ `unresolved`（附条件），见 `P003` §7.5.6 |
> | `D002-001` 更新为 Accepted / Rejected / Needs CDFV experiment | ✅ 本条（Needs CDFV experiment，附条件） |
> | 产出 `KU003-001` | ✅ 已起草（status: proposed），见 `P003` §13 |
> | 结论可溯源到文件 / 章节 / 工况 / 坐标与单位 | ✅ 见 `P003` §7.5.2 与 §8 |
>
> **判定：G1 判据全部满足。** 但须注意其质量边界——结论是 `unresolved` 而非
> material/immaterial，即**环闭合了，但环内的物理问题尚未解决**。
> 按 `D-ANRI-002` §4，这意味着 G2（同域第二个问题复用）的进入条件已具备，
> 而 G3（跨域）仍不得启动。
