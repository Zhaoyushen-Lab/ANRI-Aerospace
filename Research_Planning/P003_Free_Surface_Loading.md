# P003 — CDFV-001 Free-Surface Loading Assessment

## Metadata

- Research object: CDFV-001
- Parent question: AQ001
- Parent decision candidate: D002-001
- Primary evidence: P002, E002-001
- Status: Planned
- Type: Evidence-to-model transfer task
- Revision: v0.1

---

# 1. Research Question

Does the velocity-dependent free-surface loading reported in P002 remain significant for CDFV-001 water-exit conditions?

This is narrower than “optimize the transition.” The task first determines whether the effect must be represented in the CDFV-001 model and, if so, what minimum representation is justified.

# 2. Why This Task Exists

P002 reports that, in the tested cylindrical model:

- suction increases between approximately 0.1 and 0.25 m/s;
- suction is approximately unchanged above 0.25 m/s within the tested range;
- maximum suction is about 10% of vehicle weight;
- the result comes from a constrained experiment and a reported fit.

These results do not establish that the same loading applies to CDFV-001. P003 tests transferability rather than assuming it.

# 3. Parent Evidence and Decision

## 3.1 Parent Evidence

- Evidence ID: E002-001
- Source: P002 Section 4.1.2, Figures 11–12
- Type: time-resolved resultant-force data and suction-force fit
- Limitation: no raw time-series dataset has been recovered or digitized

## 3.2 Parent Decision Candidate

D002-001: CDFV-001 transition analysis should compare a baseline model with a model containing a velocity-dependent free-surface loading term.

Status: Candidate. P003 must provide evidence to accept, reject, or narrow this decision.

# 4. Scope

## Included

- Compare the P002 cylinder and CDFV-001 geometry and transition conditions.
- Determine whether CDFV-001 operates in a velocity regime where P002's effect could matter.
- Define the minimum state variables and loading term needed for a first model comparison.
- Define one validation criterion and the next measurement if analytical transfer is insufficient.

## Excluded

- Claiming that P002 validates CDFV-001.
- Building a full autonomous controller.
- Reconstructing all P002 raw data from plots without recording digitization uncertainty.
- Extrapolating the P002 fit beyond its tested conditions.
- Building an AI agent or a complete ROS platform.

# 5. Working Hypotheses

These are hypotheses to test, not conclusions.

- H1: Free-surface loading is material within at least part of the CDFV-001 operating envelope.
- H2: A first CDFV model can represent the effect as a stage- and velocity-dependent additional vertical load, with explicit validity limits.
- H3: The P002 cylindrical fit cannot be transferred numerically to CDFV-001 without a geometry or experiment correction.

# 6. Inputs Required

## From P002

- E002-001 evidence card.
- P002 Figures 11–12 and captions.
- Tested velocity range: 0.1–0.5 m/s.
- Transition-stage definitions and force notation.
- Model geometry and limitations.

## From CDFV-001

- water-exit velocity range;
- vehicle mass and weight reference;
- body diameter, length, and wetted geometry near the free surface;
- expected attitude during exit;
- current baseline force model;
- target force or stability tolerance;
- available sensor or simulation data.

If an input is unavailable, record “Blocked — source required.” Do not substitute P002 cylinder values.

# 7. Method

## Stage 1 — Regime and Transfer-Condition Comparison

> **2026-10-20 重构**。原表按**绝对量**对比 P002 与 CDFV-001（出水速度、质量、直径、
> 长度、姿态），因此 4 个单元格 `Blocked`——CDFV-001 的绝对几何与质量还不存在。
>
> 但这张表要回答的从来不是"CDFV-001 上的载荷有多大"，而是
> "**在什么条件下 P002 的量级结论可以迁移到 CDFV-001**"。
> 后者是**无量纲**问题，不需要 CDFV-001 的绝对数值。§7.5.5 已给出结构：
>
> ```
> F_suction / W  =  (ρ_w / ρ_body,eff) · G(geometry, Fr, immersion state)
> ```
>
> 所以每行的 "CDFV-001" 列现在写的是**迁移条件（必须满足什么）**，
> 而不是**被要求的数值（是多少）**。

| Dimensionless group | Definition | P002 value | Transfer condition for CDFV-001 | Status |
|---|---|---|---|---|
| Froude number | `Fr_D = v / √(g·D)` | 0.106 @0.1 m/s; 0.266 @0.25 m/s; 0.532 @0.5 m/s; saturation at `≈0.27` | CDFV-001 must operate at `Fr_D ≳ 0.27` for the load to be material | Derived from P002 §4.1 |
| Effective density ratio | `ρ_w / ρ_body,eff`, with `ρ_body,eff = m / (πD²L/4)` | `ρ_body,eff = 988 kg/m³`; ratio = **1.012** | ratio within ±5% of 1.012, else `F_suction/W` rescales **linearly** with the ratio | Derived (Ref-01B `summary.csv`) |
| Slenderness | `L / D` | **3.589** | assume equal; otherwise a geometry correction is required (§7.5.5 implication 3) | Derived from P002 Table 1 |
| Immersion state at exit | `h_sub / L` | `0 → 1` over `1.5 L` of travel | the crossing sequence must match: start fully submerged, end fully emerged | `Ref-01B_Initial_Immersion_Decision.md` |
| Cavity-deficit ratio | `ΔV_cav / V_displaced` | **9.86e-2** (9.9%) | equality is the **untested hypothesis**, not a condition to impose | Hypothesis H4, §7.5.3 |

Completion condition: **every cell carries either a repository-derived value or an explicit
transfer condition.** This table no longer asks CDFV-001 for data it cannot supply, which is
why the four former `Blocked` cells resolve — **they were blocked by the framing, not by a
missing measurement.**

**What this reframing does NOT do**: it does not establish that CDFV-001 satisfies any of
these conditions. It states what would have to be true. CDFV-001's actual specification
remains owed, and is tracked separately (trigger `T18`).

## Stage 2 — Baseline Definition

Record the current CDFV baseline, including:

- frame and sign convention;
- gravity and buoyancy terms;
- hydrodynamic terms already included;
- transition-stage definition;
- velocity and attitude inputs;
- output used for the decision.

Do not introduce a new free-surface term before the baseline is recorded.

## Stage 3 — Minimum Model Comparison

Compare the baseline model with a baseline plus candidate free-surface term.

The candidate term must specify:

- velocity definition;
- active transition stage;
- force direction and frame;
- units or normalization;
- validity range;
- uncertainty or confidence statement;
- source and assumptions.

A symbolic term is acceptable initially. Copying P002 numerical coefficients is not acceptable unless geometry and normalization are justified.

## Stage 4 — Validation Choice

Choose one:

1. Analytical screening: show that the term is negligible or potentially material over the CDFV range.
2. Digitized comparison: reproduce the P002 curve with a recorded method and uncertainty.
3. New experiment or simulation: define a CDFV-specific measurement or simulation because transfer cannot be justified analytically.

---

# 7.5 Path B — 自由液面载荷量级的量纲筛选

- 执行日期：2026-10-12
- 依据：`Research_Planning/P003_Stage1_Sourcing_Checklist.md` §3.2 路径 B
- 选择的上位选项：**Stage 4 选项 1（解析筛选）**
- 输入状态：**未使用任何 CDFV-001 数值**（Stage 1 四个单元格仍为 Blocked）

## 7.5.1 为什么可以不用 CDFV 数值

待答问题不是"载荷的绝对大小是多少"，而是"**P002 报告的载荷量级在什么条件下会对
CDFV-001 构成不可忽略的载荷**"。后者是量纲问题，可以用符号与比例关系回答。

## 7.5.2 输入数据（全部来自仓库内文档）

| 量 | 值 | 来源 |
|---|---|---|
| P002 模型质量 m | 2.030 kg | `Paper_Notes/P002_Free_Surface_Hydrodynamics_HAUV_2022.md` Table 1（p.5） |
| 直径 D | 0.090 m | 同上 |
| 长度 L | 0.323 m | 同上 |
| 重量 W | m·g = 19.9075 N（g=9.80665 m/s²） | 本文件计算 |
| P002 报告的最大吸入力 | ≈ 10% W ≈ **1.99 N** | E002-001；P002 §4.1.2, Figs. 11–12 |
| 饱和点 | 约 0.25 m/s 以上近似不变 | E002-001 |
| 初始深度（加速度组 / 姿态组） | 0.1 m / 0.3 m | P002 §4.2 / §4.3 |
| 共振/振动阈值 | ≥0.2 m/s² 数据退化 | P002 §4.2 |

## 7.5.3 四种候选机制及其被判除的依据

对同一组观测（1.99 N，且在 0.25 m/s 以上饱和），逐一检验量级：

| # | 机制 | 力的量纲尺度 | 数值 | 与 1.99 N 的关系 |
|---|---|---|---|---|
| H1 | 表面张力 | σ·πD | **0.0206 N** | **仅 1.03%** → 判除 |
| H2 | 准静态水面凹陷（hydrostatic） | ρ_w·g·A·Δh | 需 Δh = **31.9 mm**（=9.9% L） | 量级偏大，**强假设，判为不可信** |
| H3 | 惯性/动压（drag 或驻点） | ½ρv²A | 0.032 N @0.25 m/s；**0.127 N @0.5 m/s** | 至多为 1.99 N 的 **6.4%** → 判除 |
| H4 | **空腔体积亏缺** | ρ_w·g·ΔV_cav | 只需 ΔV_cav = 2.03e-4 m³ = **9.9% 总排水体积** | **量级自洽** |

补充：静水压基线的满浸没浮力为 `ρ·g·V = 20.151 N`（见
`Models/CDFV-001/Ref-01B/results/summary.csv`），故 1.99 N 相当于**满浸没浮力的 9.9%**。
该基准是"可提取上限"的正确量级——没有它，1.99 N 无从解释。

## 7.5.4 结论：空腔体积亏缺假说（cavity-volume deficit hypothesis）

**ANRI 推断（非 P002 作者结论）**：1.99 N 既不能由 1.0 m/s 以下速度的动压解释，
也不能由表面张力解释；唯一量级自洽的解释是**水自物体表面分离形成气腔，使实际排水体积
小于静水线所暗示的体积**，从而损失浮力。该假说同时解释饱和行为：空腔一旦贯通并稳定，
力即不再随速度变化——这是**几何机制而非动压机制**的特征。

**与 P002 原文的边界**：P002 未提供 0.1–0.5 m/s 工况下的空腔形态量化
（`Paper_Notes` §9 仅有 Figs. 9–10 自由液面图像，未含空腔尺寸）。
故本假说**由本文件提出，尚无反演证据**。

## 7.5.5 标度律（对 CDFV 迁移的含义）

空腔体积与排水体积**同为 L³ 量级**，其比值无量纲：

```
F_suction / W  =  (ρ_w / ρ_body,eff) · G(geometry, Fr, immersion state)
                 ↑ 与尺度 L 无关
```

严格相似条件下该比值**在尺度变换下不变**。几何与密度比相同时，比值仅是 Froude 数的函数。

由此得到三条可检验含义：

1. **表面张力不会在放大时增强**（判除 H1 使这一点更确定）：小尺度水槽实验不会因表面
   张力而高估该效应的**相对**重要性。
2. **该比值随"机体有效密度" ρ_body,eff = m_body/(πD²L/4) 反向变化**。P002 圆柱体的
   有效密度为 988 kg/m³（2.030 kg / 2.0548e-3 m³）。**CDFV-001 的总质量与总排水体积
   均未知**，故无法给出该比值。
3. **若 Froude 数显著不同**（P002 的 Fr_D = v/√(gD)：0.106 @0.1 m/s，0.266 @0.25 m/s，
   0.532 @0.5 m/s；饱和出现在 Fr_D ≈ 0.27），则需重新取值。

## 7.5.6 三态结论

> **unresolved（含条件性陈述）**

- **material 的条件**：CDFV-001 的机体有效密度与几何与 P002 相当，且工作在
  Fr_D ≳ 0.27 的空腔稳定区。
- **immaterial 的条件**：CDFV-001 的机体有效密度远低于 988 kg/m³
  （同等浮力由更大体积提供，使该比值按 ρ_w/ρ_body 缩小），或工作在空腔尚未贯通的区间。
- **当前判定**：**无法在两者间选择**，因为 CDFV-001 的有效密度、几何与 Froude 区间
  **全部未知**。
  **2026-10-20 补充**：Stage 1 已重构为无量纲迁移条件（见 §7 的 Stage 1），
  故"未知"现在以**条件形式**列出，而不再是 4 个 `Blocked` 单元格。
  三态结论**不变**——仍是 `unresolved`——但理由的形式变了：
  从前是"缺 CDFV 数据所以无法判断"，现在是"**迁移条件已列出，尚未验证任何一条**"。
- 关键限定（必须随结论传递）：P002 报告的"吸入力"是**从合力 Z 中提取并拟合的残差**
  （`Paper_Notes` §5、§14 明确要求区分"测量的合力 Z"与"孤立的吸入分量"）。
  本结论因此是**关于合力中自由液面贡献部分的推断**，不是对独立分量的测量结论。

## 7.5.7 需要的下一次测量（Stage 4 选项 3）

按代价排序，推荐 **B1**：

**B1 — Froude 相似性直接检验（推荐）**
同一几何、两种尺度（例如 λ=0.5 与 λ=1.0），在**相同 Fr_D** 下测 F_suction/W。
- 若该比值在两种尺度下一致 → 无量纲关系成立，CDFV 可在满足同样无量纲条件时被预测；
- 若不一致 → 必须做 CDFV 专用实验。
- 优点：**不需要确认空腔机制**，直接检验迁移所依赖的那个不变量。

**B2 — 空腔体积亏缺的直接反演**
侧视成像测 ΔV_cav(t) 与合力时间历程，检验 `F_suction ≈ ρ_w g ΔV_cav(t)`。
- 优点：可证伪本文件的假说；
- 缺点：需要自由液面成像与同步，成本更高。

**B0（不作为推荐）** — 仅做数字化比对（Stage 4 选项 2）：复现 P002 曲线只能校验读取
方法，**不能回答迁移问题**，因为迁移的困难在几何与密度比，不在曲线读取。

## 7.5.8 第五个候选机制：附加质量梯度（2026-10-20 补充）

> **本节追加于 §7.5.3 之后，不修改 §7.5.3 的"四种"表述。**
> §7.5.3 是 2026-10-12 的记录；本节是读到新文献后的补充。

### 来源

**陈宇翔（2012）博士论文《物体穿过自由表面的多相流体动力学问题研究》**，
哈尔滨工程大学，§4.1.3，式 (4-36) 与 (4-37)：

```
F = −½ V² ∂m₃₃/∂Z + m₃₃ dV/dt          (4-36)
恒速时：  F = −½ V² ∂m₃₃/∂Z            (4-37)
出水系数：C_e = F / (½ ρ V² D)          (4-38)
```

**物理含义**：物体接近自由面时，物体与其镜像体的距离变化，**使附加质量系数本身随位置变化**，
该项在**恒速**出水时也存在（不需要加速度）。

**原文对量级的表述**（p.78）：
> 「当水平圆柱运动至接近自由表面（−1 < Vt/R < 0）时 m₃₃ 快速增加。」

### 为什么此前未列入 §7.5.3

**因为 2026-10-12 写 §7.5.3 时本文件不知道这个机制。** 不是判除了，是没考虑。

### ⚠️ 更正：一条此前用过的、不成立的排除论证

2026-10-20 曾以量纲理由排除本机制，**该论证不成立**，理由两条：

| 原论证 | 为什么不成立 |
|---|---|
| 该项 ∝ V²，与 P002 观测的"饱和"矛盾 | **陈宇翔的 `C_e`–`Vt/R` 曲线在两个不同速度下几乎重合（图 4.2 / 4.3），这恰恰证实 V² 标度成立**。而"饱和"来自 P002 数据在加速度 > 0.2 m/s² 时退化，**是数据限制，不是物理规律** |
| 与已判除的 H3 同标度，故同命运 | **H3 是动压（½ρv²A），本机制是附加质量梯度。同标度 ≠ 同机制** |

**结论**：`∂m₃₃/∂Z` **不能被量纲论证排除。只有实验数据能排除它。**

### 当前状态

| 项 | 状态 |
|---|---|
| 是否为候选机制 | **是** |
| 能否被排除 | **否**（量纲论证无效） |
| 能否被支持 | **否**（缺 `∂m₃₃/∂Z` 的数值） |
| 需要的量 | 本项目几何（竖直圆柱、平头）的 `∂m₃₃/∂Z` |

**注**：陈宇翔给的是**算法**（Morino 面元法 + 镜像体），**不是列表值**。
故取得该量需要自行实现面元法，或改用其他势流求解器。

## 7.5.9 B1 判据的双模型问题（解释预案；**判据不变**）

### 判据不变

**B1 的判据 `R = (F/W)_λ=0.5 ÷ (F/W)_λ=1.0`，通过区间 `1 ± 0.20`，已预注册，
不因本节修改。**

### 问题

在陈宇翔的模型下，`C_e` 对 `Vt/R` 是**普适**的（两个速度曲线重合）。
若该普适性对竖直圆柱也成立，则 **R = 1 是该模型的必然推论**。

**所以 `R ≈ 1` 不再能单独区分 H4 与 H5。**

### 解释预案（结果出来时按此写，不得事后改）

| B1 结果 | 能说什么 | **不能**说什么 |
|---|---|---|
| `R ≈ 1`（通过） | 「无量纲关系在尺度变换下成立」——**这正是 §1 研究问题所问的** | ❌ 不能据此支持 H4 空腔体积亏缺 |
| `R ≠ 1`（不通过） | 「无量纲关系不成立，CDFV 需专用实验」 | ❌ 同时否定 H4 与 H5，不能只说否定了 H4 |

### 为什么这不削弱 B1

**§1 的研究问题是**：

> "Does the velocity-dependent free-surface loading reported in P002 remain significant for
> CDFV-001 water-exit conditions?"

**这是迁移性问题，不是机制问题。** B1 直接回答它，无论机制是 H4 还是 H5。

**所以：B1 的价值不变，但它的结论范围必须限定在迁移性，不能延伸到机制。**

### 区分机制需要 B2

| 假说 | 预测 |
|---|---|
| **H4** 空腔体积亏缺 | `F_suction ∝ ρ_w g ΔV_cav` —— 力与**排水体积亏缺**成正比 |
| **H5** 附加质量梯度 | `F ∝ ½ V² ∂m₃₃/∂Z` —— 力与**V²** 成正比 |

**两者对速度的依赖不同（H4 在空腔稳定后不随 V 变化；H5 恒为 V²）。**
**所以 B2（侧视成像 + 同步合力）可以区分它们。**

## 7.5.10 第六个候选机制：被带出的水膜（2026-10-20 补充）

> **本节追加，不改动 §7.5.3 的"四种"，也不改动 §7.5.8/§7.5.9。**

### 来源

**蔡军辉、何友声、叶取源（1990）.《平头圆柱体垂直出水粘性流动的数值模拟》.
水动力学研究与进展（A辑）, 1990 年第 2 期.**（知网 `SDLJ199002012`）

**该文摘要提到计算了**：

> 「柱体表面压力及**粘附在柱体上并被带出水面的流体体积**」

**即：物体出水时会带走一层附着水，这层水有重量。**

### 物理图像

| 假说 | 向下净力的来源 |
|---|---|
| **H4** 空腔体积亏缺 | 排水体积 < 几何体积——**该有水的地方是空气** |
| **H6** 被带出的水膜 | 附着在物体上的额外质量——**多带了水** |

### ⚠️ 量级简并：H4 与 H6 在数值上不可分

```
1.99 N ÷ 9.80665 = 0.203 kg 水 = 2.03e-4 m³
§7.5.3 算得 H4 需要 ΔV_cav      = 2.03e-4 m³
```

> **同一个体积。**
> **两者都要求「约 9.9% 总排水体积的水不在它该在的位置」。**
> **所以仅凭力的量级，无法区分 H4 与 H6。**

### 但两者可区分

| | H4 空腔亏缺 | H6 水膜带出 |
|---|---|---|
| 那 9.9% 的空间里是什么 | **空气** | 不适用（多出的是水） |
| 对速度的依赖 | 空腔稳定后**不随 V 变化**（这曾是"饱和"的来源） | 水膜厚度随 V 变，**通常随 V 增厚** |
| 观测手段 | 侧视成像看空腔 | **出水后称重 / 收集被带出的水** |

**H6 的证据要求显著低于 H4**：不需要高速成像，**一台天平即可**。

### ⚠️ 一条禁止混淆的说明

**§7.5.3 的 `2.03e-4 m³` 是"该假说所需"的量级，不是该文计算出的结果。**
该文摘要**未给出该体积的数值**。
**不得在论文中写成"蔡军辉等算出 2.03e-4 m³"。**

### 新增推荐测量：B3（比 B2 便宜得多）

**B3 — 出水后称重（区分 H4 与 H6）**

| 项 | 内容 |
|---|---|
| 做法 | 物体出水瞬间/之后**称其质量**，或收集溅出与被带出的水并称重 |
| H6 成立 | 测得**额外水质量 ≈ 0.203 kg**（对 P002 尺度）；且该质量随出水速度增大 |
| H4 成立 | 无额外水质量；力仍存在 → 只能是排水体积亏缺 |
| 代价 | **极低**（天平 + 容器），远低于 B2 的高速成像 |
| 局限 | 若水膜在称重前已流失，会**假阴性**；故需称重或收集尽快完成 |

**B3 与 B1 不冲突**：B1 检验迁移性，B3 检验机制。**可同一批实验同时做。**

### 当前机制表（截至本节）

| 假说 | 状态 |
|---|---|
| H1 表面张力 | **判除**（1.03%） |
| H2 准静态水面凹陷 | **判为不可信**（需 Δh = 31.9 mm = 9.9% L） |
| H3 动压 | **判除**（≤6.4%） |
| H4 空腔体积亏缺 | **量级自洽**，但无独立证据 |
| H5 附加质量梯度 | **未定**——不能被量纲排除，也无法支持 |
| **H6 被带出的水膜** | **未定**——与 H4 量级简并，但可用 B3 区分 |

# 8. Provenance Rules

Every P003 result must identify:

- source file or experiment ID;
- section, figure, table, or dataset;
- geometry and operating condition;
- frame and unit;
- measured, digitized, calculated, or inferred status;
- assumptions and uncertainty;
- relation to E002-001 and D002-001.

Minimum observation record:

Observation ID:
Source:
Condition:
Quantity and unit:
Method:
Observation:
Uncertainty / limitation:
Implication for D002-001:

# 9. Acceptance Criteria

P003 is complete only when:

- CDFV-001 velocity and geometry inputs are sourced, or stated as an explicit
  **transfer condition** in the dimensionless Stage 1 table;
- the current baseline model is documented;
- the candidate free-surface term has frame, units, stage, and validity limits;
- at least one comparison is reproducible from recorded inputs;
- the result states material, immaterial-within-range, or unresolved;
- D002-001 is updated to Accepted, Rejected, or Needs CDFV experiment;
- a subsequent task is created if the result is unresolved.

P003 is not complete if it only says “P002 suggests this is important.”

# 10. Expected Outputs

1. This P003 task file with a progress log.
2. An update to Research_Planning/Decision_Log.md.
3. One provenance-linked comparison table or figure.
4. One CDFV-001 Knowledge Update.
5. A new experiment or modeling task if the result remains unresolved.

# 11. Risks and Controls

| Risk | Control |
|---|---|
| Copying P002 fit directly to CDFV | Require geometry and normalization check |
| Confusing resultant Z with isolated suction | Keep resultant/component labels separate |
| Treating 0.25 m/s as universal | State it is a P002 tested-range observation |
| Hidden coordinate mismatch | Record frame, origin, sign, and moment reference |
| Overfitting digitized plots | Record digitization method and uncertainty |
| Expanding into full ROS software | Keep P003 bounded to one transfer task |

# 12. Decision Update

**Decision ID:** D002-001（原"Decision Candidate"）
**Update date:** 2026-10-12
**Recorded by:** P003 Path B screening

## Outcome

**Needs CDFV experiment** — 附条件（记录日期 2026-10-12）。

**已同步**：本条目已写入 `Research_Planning/Decision_Log.md` 顶部
`D002-001` 条目（状态与 Next Action 均已更新），该文件为哈希注册产物。

## Evidence reviewed

- E002-001（P002 §4.1.2, Figs. 11–12）：吸入力随速度增长、0.25 m/s 以上饱和、最大 ≈10% 车重
- `Paper_Notes/P002_Free_Surface_Hydrodynamics_HAUV_2022.md` Table 1（p.5）与 §4.2/§4.3 的工况条件
- `Paper_Notes/P002_Free_Surface_Hydrodynamics_HAUV_2022.md` §5、§14：合力 Z 与孤立分量的区分要求
- `Models/CDFV-001/Ref-01B/results/summary.csv`：满浸没浮力 20.1510694 N
- 本文件 §7.5.3 的量级检验（四种候选机制的数值判除）

## Result

1.99 N 的载荷量级**无法由 1.0 m/s 以内的动压解释**（至多 6.4%），
**无法由表面张力解释**（1.03%），准静态凹陷所需 31.9 mm 偏大。
量级自洽的解释是**空腔体积亏缺**（需损失约 9.9% 总排水体积）。
三态结论为 **unresolved（含条件性陈述）**。判据从"速度范围是否重叠"改为
"**Froude 区间 + 机体有效密度比 + 几何**是否可比"。

## Reason

1. P002 的载荷量级在机理上**不属于本项目原假设的"速度相关附加力"**形态
   （动压解释被量级判除），因此 D002-001 原表述"velocity-dependent free-surface
   loading term"的**机理描述需要修正**。
2. 迁移的困难**不在曲线读取，而在无量纲条件**（Fr、有效密度比、几何），
   故 Stage 4 选项 2（数字化比对）被排除为无效路径。
3. **为何不直接记为 Accepted/Rejected**：两者都要求已知 CDFV-001 的机体有效密度，
   而该量只能以**迁移条件**形式陈述，尚未被验证任何一条（2026-10-20 起
   Stage 1 为无量纲条件表，不再是 `Blocked` 单元格）。在条件未被验证时
   记 Accepted 或
   Rejected 都属于**用推测替代事实**，违反本文件 §6 与 §11 的禁止条款。

## New assumptions

- A-P003-001：空腔体积亏缺是 P002 1.99 N 载荷的主导机制（**未经反演验证**）。
- A-P003-002：`F_suction/W` 在几何与密度比相同的严格相似条件下与尺度无关。

## Next task

1. **B1（推荐）**：同几何、两种尺度、相同 Fr_D 下测 `F_suction/W`，
   直接检验 A-P003-002（详见 §7.5.7）。
2. ~~将本条目同步写入 `Research_Planning/Decision_Log.md`~~ — **已于 2026-10-12 完成**。
3. 若 B1 通过：把 D002-001 转为 **Accepted**（附无量纲适用条件）。
   若 B1 不通过：转为 **Needs CDFV experiment**（无条件）。
4. KU003-001 在 D002-001 被接受时由 proposed 转为 active。

# 13. Knowledge Update

Knowledge Update ID: KU003-001

**Status: proposed**（需 D002-001 被接受后转为 active）

## Before

在本次筛选之前，项目对"自由液面载荷"的知识状态是：P002 报告了一个随速度变化的吸入力，
最大值约为车重的 10%，并在 0.25 m/s 以上近似不变（来源 E002-001）。
**该载荷的物理机制未在本项目内被辨识**；`CDFV-001_Reference_Configuration.md` 仅记录
"Free-surface term: Excluded from baseline"，未给出量级论证。
CDFV 的适用性记为"未验证"（P002 note §3 Evidence Status）。

## After

1. **机制层面（新增）**：在 P002 的 1.99 N 量级上，表面张力只占 **1.03%**、
   0.5 m/s 以内的动压至多占 **6.4%**，而准静态凹陷需 31.9 mm（9.9% L，偏大）。
   量级自洽的解释是**空腔体积亏缺**：气腔使实际排水体积低于静水线暗示值，
   损失量约为总排水体积的 **9.9%**（= 满浸没浮力 20.151 N 的 9.9%）。
   该假说同时解释饱和行为（几何机制而非动压机制）。**本假说由本文件提出，尚无反演证据。**
2. **标度层面（新增）**：空腔体积与排水体积同为 L³，其比值无量纲——
   严格相似下 `F_suction/W` **与尺度无关**，仅是 (几何, Fr, 有效密度比) 的函数。
   由此可判除"小尺度水槽会因表面张力高估该效应"这一常见顾虑。
3. **判据层面（新增）**：迁移所需的判据不是"速度范围是否重叠"，而是
   **Froude 数区间 + 机体有效密度比 + 几何**三者是否可比。
   P002 的 Fr_D = 0.106 / 0.266 / 0.532（@0.1 / 0.25 / 0.5 m/s），饱和出现在 Fr_D ≈ 0.27。
4. **结论层面**：P003 的结果为 **unresolved（含条件性陈述）**，
   并已转化为一条可执行的验前假设（见 §7.5.7 B1）。

## Evidence

- E002-001（P002 §4.1.2, Figs. 11–12）：最大吸入力 ≈10% 车重；0.25 m/s 以上饱和。
- `Paper_Notes/P002_Free_Surface_Hydrodynamics_HAUV_2022.md` Table 1（p.5）：
  m = 2.030 kg，D = 0.090 m，L = 0.323 m。
- 同 note §5 与 §14：要求区分"测量的合力 Z"与"孤立的吸入分量"。
- `Models/CDFV-001/Ref-01B/results/summary.csv`：满浸没浮力 20.1510694 N（本仓库计算）。
- 本文件 §7.5.3 的量级检验表（四种候选机制的数值判除）。

## Validity range

- 适用条件：受限运动、直立圆柱、Fr_D ≲ 0.53、加速度 < 0.2 m/s²（P002 在 ≥0.2 m/s² 数据退化）。
- **不适用**：自主过渡、非圆柱几何、带臂构型（P002 的带臂比较仅限于 0.1 m/s）。
- 本知识更新**不包含任何 CDFV-001 的数值结论**。

## Open limitation

1. 空腔体积亏缺假说**未被反演验证**；P002 未提供 0.1–0.5 m/s 工况的空腔形态量化。
2. P002 报告的"吸入力"是**合力 Z 的拟合残差**，不是孤立分量；本结论继承该限定。
3. CDFV-001 的机体有效密度、几何与 Froude 区间**全部未知**，故 material/immaterial
   无法判定。
4. 数字化比对路径（Stage 4 选项 2）**不能回答迁移问题**，只能校验曲线读取；
   已在本文件 §7.5.7 的 B0 中说明。

# 14. Progress Log

| Date | Action | Result | Commit |
|---|---|---|---|
| 2026-09-26 | Created P003 from D002-001 | Scope defined; CDFV inputs not yet filled | To record |
| 2026-10-12 | Built Stage 1 sourcing checklist; confirmed CDFV-001 parameters do not exist in-repo | Four parameters remain Blocked; three forward paths identified | To record |
| 2026-10-12 | Executed Path B (dimensional screening, Stage 4 option 1) | **unresolved** with conditional statement; cavity-volume deficit hypothesis proposed; KU003-001 drafted | To record |
| 2026-10-12 | Recorded D002-001 in `Decision_Log.md` and regenerated the object hashes | `D002-001` **Candidate → Needs CDFV experiment** (conditional); Decision Candidate revised to a dimensionless criterion; **EEM G1 criteria satisfied** | To record |

# 15. ROS Handoff

ResearchObject:
  plan: P003
  parent_paper: P002
  parent_evidence: E002-001
  parent_decision: D002-001
  target: CDFV-001
  question: transferability of velocity-dependent free-surface loading
  status: bounded_result_recorded
  stage4_choice: option 1 (analytical screening)
  result: unresolved (conditional)
  decision_update: D002-001 -> Needs CDFV experiment (conditional), recorded 2026-10-12
  knowledge_update: KU003-001 (proposed)
  required_output: bounded model comparison or CDFV experiment specification
  next_measurement: B1 (same geometry, two scales, matched Froude number)
  completion_gate: satisfied 2026-10-12; further resolution requires B1 or CDFV effective density

# 16. Current Action

## 16.1 Completed (2026-10-12)

**Path B（量纲筛选）已执行**，结论见 §7.5；D002-001 更新见 §12；KU003-001 见 §13。
Stage 4 已选择**选项 1（解析筛选）**，并由此导出选项 3 的必要性（§7.5.7 B1）。

## 16.2 Still open

**2026-10-20 起，Stage 1 不再是 `Blocked` 单元格表。** 它已重构为
**无量纲组 + 迁移条件**（见 §7 的 Stage 1）：每一行给出
「CDFV-001 必须满足什么」，而不是「CDFV-001 的值是多少」。

**仍然开放的（性质变了，不是消失了）**：

1. **没有任何一条迁移条件被验证过** —— Fr、有效密度比、`L/D`、浸没序列
   这四条全是「CDFV-001 若满足则可迁移」的**条件**，不是已知事实；
2. **CDFV-001 仍无独立规格** —— 原表要求它，新表不要求它，
   但 `Ref-01S` 的制造与触发条件 `T18` 仍然要求它；
3. **`ΔV_cav/V` 的等式仍是假说**（H4），未经实验检验。

**关键限定**：重构解除了「研究问题被缺数据卡住」这一状态，
**但没有推进任何物理结论**。三态结论仍为 `unresolved`。
因为 CDFV-001 的几何、质量与速度包线在本仓库中不存在
（实测依据：`Research_Planning/P003_Stage1_Sourcing_Checklist.md` §0）。

**两条路并行，互不阻塞**：

1. **不需要 CDFV 数值的**：执行 §7.5.7 的 B1（Froude 相似性直接检验）。
   这是把结论从 unresolved 推向 Accepted 或 Needs-experiment 的**唯一途径**，
   且不依赖 Stage 1 的四个单元格。
2. **需要 CDFV 数值的**：按 `P003_Stage1_Sourcing_Checklist.md` §3 取得四个参数。
   它不再是回答迁移问题的**前置条件**，而只影响 material/immaterial 的**最终判定**。

**约束（不变）**：在来源确认前不得填入任何 CDFV 数值，不得用 P002 圆柱值替代，
不得在基线记录之前引入自由液面项。
