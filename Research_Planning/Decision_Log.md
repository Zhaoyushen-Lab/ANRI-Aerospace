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

## Observation

The reported suction force increases between approximately
0.1 and 0.25 m/s and becomes approximately stable above 0.25 m/s
within the tested range.

## Decision Candidate

CDFV-001 transition analysis should compare a baseline model
against a model containing a velocity-dependent free-surface term.

## Status

Candidate — not yet validated on CDFV-001.

## Next Action

Determine whether the CDFV-001 geometry and operating range justify
a dedicated free-surface loading test.

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
---

# 修订记录

| 日期 | 条目 | 变更 | 原因 |
|---|---|---|---|
| 2026-10-11 | `D-ANRI-001` | 新建 | 两份同日评估（体系建成概率 / 被抢先概率）给出方向相反的结论，需要一次定位与资源分配决策 |
| 2026-10-11 | `D-ANRI-002` | 新建 | 回答"专业化之后能否向通用化进军"，并设定 G1–G4 门槛以防跳级 |
| 2026-10-11 | `D-ANRI-001` | 更正 | 原报告称"人类锚点"为本项目缺口；复核发现 `ANRI_Principles_v0.1.md` Principle 5 早已记载该原则，准确表述为"已具备、未制度化" |
