# ANRI / AI4S / AI4E 日报 — 2026-10-20

- 日期：2026-10-20
- 口径版本：`v1`
- 状态快照：`Research_Log/2026-10-20_ANRI_State.json`
- 上一份日报：见 §4.5（由 `compare_snapshots.py` 自动识别）

---

## 0. 机器生成部分（由脚本填充，请勿手改）

> 生成命令：
>
> ```powershell
> py -3 .\scripts\collect_state.py --out "Research_Log\2026-10-20_ANRI_State.json"
> py -3 .\scripts\compare_snapshots.py --markdown --date 2026-10-20
> ```

### Δ 2026-10-19 → 2026-10-20

| Field | Before | After |
|---|---|---|
| `head.commit` | `bcf213e6d05712ed6fd2d74eb834d145594bd24f` | `f799259a7092f3642d2ccb61c2a142e322a40132` |
| `worktree.pending_entries` | `40` | `3` |
| `worktree.staged` | `34` | `3` |
| `worktree.untracked` | `6` | `0` |
| `worktree.unpushed_commits` | `9` | `0` |
| `line_endings.files` | `165` | `180` |
| `research_object.sha256` | `df8052cf4c352f5b0e19a8709b02ac647124f1908275574acb71a049ecd0074d` | `561d587377168f84894309815a26a6c9e8737e89be7711f9887735a9c2f3fa6a` |
| `research_object.artifact_count` | `80` | `87` |
| `research_object.manifest_entries` | `79` | `86` |

### Trigger status

| ID | Threshold | Status | Observed | Promised effect |
|---|---|---|---|---|
| T1 | 2026-10-14 | **FIRED** | pending_entries=3 | L2 -0.05, L3 -0.05 |
| T2 | 2026-10-25 | **pending** | lab_engagement_lines=3 (no machine-readable response field exists) | L1-lab -> 0.25 |
| T3 | 2026-10-11 | **not met** | research_objects=1 independent_human_reviews=0 | L2 -> 0.65, L5 -> 0.40 |
| T4 | 2026-10-11 | **not met** | manual check; not machine-evaluable | re-estimate L1-agent from published numbers (manual) |
| T5 | 2026-10-11 | **not met** | manual check; not machine-evaluable | re-estimate L1-agent and threshold A (manual) |
| T6 | 2027-02-01 | **pending** | manual check; not machine-evaluable | L2 +0.05 and replace the build item with integration (manual) |
| T7 | 2027-04-01 | **pending** | manual check; not machine-evaluable | C2c scoop probability -> 0.70; drop the independent claim (manual) |
| T8 | 2027-04-01 | **pending** | manual check; not machine-evaluable | treat C1 as pre-empted; stop submitting it as a result (manual) |
| T9 | 2027-10-01 | **pending** | manual check; not machine-evaluable | freeze C2a as pre-empted in the peer-progress report (manual) |
| T10 | 2026-11-10 | **pending** | manual check; not machine-evaluable | none (retired); see T18 |
| T11 | 2027-01-09 | **pending** | independent_human_reviews = 0 | D-ANRI-001: mark Principle 5 as not institutionalised; L4 -> 0.15 |
| T12 | 2027-04-01 | **pending** | manual check; not machine-evaluable | C2c scoop probability -> 0.85; per D-ANRI-001 adopt their specification and drop the independent claim (manual) |
| T13 | 2026-10-19 | **not met** | unpushed_commits = 0 | L2 -0.03, L3 -0.03 |
| T14 | 2026-10-20 | **not met** | manual check; not machine-evaluable | L3 -0.05; declare the gate unable to pass in a real environment (manual) |
| T15 | 2026-10-20 | **not met** | manual check; not machine-evaluable | none (retired); see T17 |
| T16 | 2026-10-26 | **pending** | manual check; not machine-evaluable | L3 -0.03; declare the gate effective only off the default branch (manual) |
| T17 | 2026-10-27 | **pending** | manual check; not machine-evaluable | L3 -0.03; declare the gate usable but the results stranded off the default branch (manual) |
| T18 | 2026-12-31 | **pending** | manual check; not machine-evaluable | L4 -0.05; record that the project has produced a verification infrastructure for a vehicle that has never been specified (manual) |
| T19 | 2026-11-20 | **pending** | manual check; not machine-evaluable | L5 -0.05; record that the pivot from protocol to domain result was written and not executed (manual) |

### Snapshot trend

| Date | head | pending | artifacts | independent human reviews | checks ok |
|---|---|---:|---:|---:|---|
| 2026-10-11 | `abc9103` | 105 | 65 | 0 | True |
| 2026-10-12 | `1705724` | 16 | 69 | 0 | True |
| 2026-10-13 | `e3edde0` | 7 | 71 | 0 | True |
| 2026-10-19 | `bcf213e` | 40 | 80 | 0 | True |
| 2026-10-20 | `f799259` | 3 | 87 | 0 | True |

### EEM 闭环（D-ANRI-002 通用化度量）

- 定义：Knowledge -> Design -> Simulation -> Evaluation -> Knowledge Update (Knowledge_Base/CDFV_Knowledge_Map.md section 5)
- **loops_closed = 2**（G1 satisfied）

| 环节 | 是否成立 |
|---|---|
| knowledge | ✅ |
| design | ✅ |
| simulation | ✅ |
| evaluation | ✅ |
| knowledge_update | ✅ |

- KU id：`KU003-001, KU004-001`
- 已决议 decision：2 条；未决议：0 条
- 说明：loops_closed counts definitions of a knowledge update that also carry a verdict in Decision_Log.md. G2 additionally requires the loops to come from DIFFERENT research questions, which the 'loops' list makes auditable.

---

## 1. 一句话摘要

**上游出现了本项目最该关注的一类进展：谷歌让 AI 智能体在真实湿实验室里跑通了
"设计分子—安排实验—读结果—改方案"的闭环**（VERID 框架），且该系统**自己抓到过一次
假阳性并修正**。同日 Fabarta 升级 AI4S 平台、中科院材料所发布双模型协作智能体。
**仓库侧**：网络恢复，`fix/gate-and-brief` 已推送（`e4d46db`）；P004 Stage 2 完成，
新增 6 个加速度工况，**`m·a` 在 1 m/s² 时达 2.030 N = P003 吸入力的 102%**；
期间发现并修复**两个度量缺陷**（`unpushed` 口径、历史快照被覆盖）。

---

## 2. 上游进展

### 2.1 研究产物层（对应 L2）

本日无新增可直接核实的 L2 层（研究对象/证据对象标准化）进展。

### 2.2 通用科研 agent / 工具层（对应 L1-agent）

**`[仅有报道]` 谷歌 VERID 框架：AI 智能体自主完成湿实验室闭环测试**
（科技日报 2026-10-19，新华网 2026-10-20 转载）

关键事实（据报道正文）：

- 团队让智能系统在**液体处理机器人**上完成"设计分子—安排实验—读取结果—
  调整下一轮方案"的闭环；
- 框架名为 **VERID**，基于开源机器人控制框架，为工作台建立**持续更新的数字孪生**，
  记录机械臂位置、孔内液量、试剂种类、枪头库存等状态；
- **发指令前先校验**：确认无撞针、空吸、容器不匹配等问题后才下发；
- 运行时**视频与动作日志保留**，供研究人员回溯；
- **一次肌红蛋白筛选中的自我纠错**：系统一度认为找到更好的分子，
  加入对照后发现并未真正识别目标，随后**调整设计规则**，下一轮即改善。

**证据强度说明**：本条为**媒体报道**，非论文、非产品发布。
文中明确"目前这仍是科研原型，不是成熟产品"，且"科研人员仍需审核序列、
核对方案、监督机器人运行"。

**同文提及的竞品动向**（均为报道口径，未独立核实）：
OpenAI 推出面向生命科学的实验规划工具；Anthropic 让模型参与新型酶系统线索发现，
但仍由科学家动手验证。

### 2.3 AI4S / AI4E 平台与政策层

**`[仅有报道]` Fabarta 升级 AI4S 平台，提出 RSI 引擎打通"材料发现—数字中试—量产"**
（TMCnet 转 prnewswire，2026-10-19）。未取得技术细节，指标未公开，仅作记录。

**`[仅有报道]` 中科院材料领域轻量化双模型协作智能体**（中科院网信工作网，
2026-10-14）。站点正文访问受限（HTTP 418），**仅记录标题与日期，不引用内容**。

### 2.4 实验闭环层（对应 L1-lab）

**本日最重要的上游判断：L1-lab 层首次出现"工业级团队 + 真实湿实验室闭环"的公开案例。**

这改变了本项目对 L1-lab 的评估基础。此前本项目把 L1-lab 视为
"need to apply for lab access"（`Ref-01S` 仍为预沟通材料），
而现在**同一层已有人用机器人 + 数字孪生 + 人工监督跑通了闭环**。

**但需注意两点**（判断）：
1. 该案例是**生物化学湿实验室**，与本项目的**水动力拖曳水槽**在物理上不可直接迁移；
2. 报道强调"科研人员仍需监督"，与本项目 `docs/ANRI_Principles_v0.1.md`
   Principle 5（人类留在环内）一致，**不构成对本项目原则的否证**。

### 2.5 评测与可靠性

**一个对本项目有直接方法学价值的细节**：报道提到谷歌系统
"一度认为找到了更好的分子，加入对照后发现并没有真正识别目标"。

这是**负例/对照组检出假阳性**的实例，与本项目
`verify_negative_cases.py`（18 例）与 `Benchmarks/ANRI-RV-001`（12 例对抗）
所做的是同一件事——**用对照暴露"看起来通过但实际错"的结果**。

**上游以工程实践印证了本项目的负例策略，这是本日唯一的方法学层面的正向信号。**

---

## 3. ANRI 五层体系对照

| 层级 | 图中模块 | 上游成熟度（今日） | 本项目状态（今日，取自 State.json） |
|---|---|---|---|
| L1 | 人类 / ClawsGO / Codex / 实验设备 | **显著上升**：谷歌 VERID 在真实湿实验室跑通闭环；Fabarta、中科院材料智能体同日发布 | Ref-01S 仍为预沟通材料，无实验室回复；同学可投入，专家需申请 |
| L2 | ANRI Research Object | 无新增 | 1 个对象、schema v0.2、**87** 个哈希注册产物 |
| L3 | Claim-Evidence Graph + Executable Validators | 无新增（VERID 的数字孪生与日志属相邻但不同之物） | 校验链在独立环境 CI 绿；**默认分支门禁已建成**（4 条规则） |
| L4 | Independent Review Gate | 无新增 | `independent_human_reviews = 0`；门禁强制但无外部评审 |
| L5 | Verified Research Package | 无新增 | EEM **`loops_closed = 2`**（P003 + P004 各闭环一次） |

---

## 4. 成功概率评估（口径 v1）

### 4.1 目标定义

- **门槛 A（单用户闭环）**：本人在 ≥1 个真实研究问题上稳定跑通 L1→L5，
  且 L5 产出可被第三方按文档复现。
- **门槛 B（大规模使用）**：≥3 个不同研究问题 / ≥2 个不同学科或团队 /
  ≥1 位非作者人员主动使用并接受 L4 审查。

### 4.2 分解

| 组件 | 今日判定 | 依据（可追溯到 §2 或 §3） |
|---|---:|---|
| L1-agent | 0.82 | 无变化。VERID 是实验执行层，非通用 agent 能力提升 |
| L1-lab | **0.38**（↓0.04） | **双向下调**：外部证明该层可被工业级团队实现（说明技术上可行），但也说明本项目在该层的相对位置更靠后——`Ref-01S` 仍无回复，而他人已跑通闭环 |
| L2 | 0.65 | 80 → 87（新增 7 个注册产物，见附录 A） |
| L3 | **0.73**（↑0.01） | 门禁建成 + CI 绿；但 `fix/gate-and-brief` 尚未合并入 `main`（领先 9 commit），默认分支内容仍非最新 |
| L4 | 0.30 | 无变化。仍 0 次外部评审 |
| L5 | **0.32** | `loops_closed = 2` 未变（P004 Stage 2 是深化，不是新闭环） |

**独立乘积**：0.82 × 0.38 × 0.65 × 0.73 × 0.30 × 0.32 ≈ **0.0142**（约 1.4%）

### 4.3 今日结论

| 口径 | 概率 | 与上一份相比 |
|---|---:|---|
| 门槛 A（12 个月） | **85%** | 无变化 |
| 门槛 B（24 个月） | **约 6%（区间 6–10%）** | 无变化 |
| 完全建成 + 大规模使用（5 年） | **约 1.5%（区间 1.5–2.5%）** | 无变化 |
| EEM 通用化成功（12 个月内 G2） | **约 30%（区间 25–35%）** | ↑5 |

### 4.4 判断依据与不确定性

**实际观察到的事实**：

- 系统日期 **2026-10-20 16:04**，距上一份日报 1 天。
- 网络恢复：`git ls-remote` 4.4 s 成功；`git push` 7.1 s 成功。
- **5 个本地分支全部与远端同步**（逐个 `git ls-remote` 核对）。
- `fix/gate-and-brief` = `e4d46db`，领先 `origin/main` **9 个 commit**。
- 仓库：`pending = 1`（仅 `2026-10-20_ANRI_State.json` 本身未跟踪）；
  `unpushed = 0`（修正 refspec 后）。
- `artifacts` = **80**（P004 Stage 2 新增 6 个加速度工况）。
- `loops_closed` = **2**（P004 Stage 2 未新增闭环，是对已有闭环的深化）。
- 上游：谷歌 VERID 报道（2026-10-19/20）；Fabarta 2026-10-19；
  中科院材料智能体 2026-10-14（正文不可达）。

**基于事实的判断**：

1. **`L1-lab` 下调的理由必须说清**：这不是"外部变差"，而是
   "外部证明了该层可被实现"→ 本项目的相对位置因此更落后。
   同一个事实既提高了技术可行性判断，也降低了我方相对优势。
   我选择**对称处理**：只看技术可行性会高估，只看相对位置会低估，
   净效果取小幅下调（−0.04）。
2. **`T13` 的解除是度量修正的结果，不是新事实**。今天的
   `unpushed = 0` 与昨天的 `9` 都是"正确读数"——因为**口径变了**。
   详见 §4.5 的显式披露。
3. **EEM 通用化上调 5 个百分点的依据**：P004 的 Stage 1 + Stage 2
   连续两次复用同一闭环结构（三态判据、量级筛选、RO schema 未改），
   且第二次还**在不改 schema 的前提下扩展了验证器**（加速度断言）。
   这说明框架的可扩展性比昨日判断的更强。

**主观不确定性（敏感度）**：
- 若 `fix/gate-and-brief` 在 10-27 前合并入 `main` → L3 升至 0.80，
  门槛 A 升至约 87%。
- 若 `T10` 的 4 个 Blocked 在 11-10 前减少到 ≤2 → 门槛 A 约 88%，
  EEM 通用化约 38%。
- 若清室复现或盲测在 11-13 前给出明确结果（无论通过与否）→
  L2 或门槛 B 会有 3–5 个百分点的移动，**方向取决于结果**。
- 若谷歌 VERID 在 6 个月内转为产品并被高校实验室采用 →
  L1-lab 再降 0.05，5 年概率降至约 1.2%。

### 4.5 距上一次评估的变化（Δ）

**机器快照 Δ（6 个字段）**：

| 字段 | 10-19 | 10-20 |
|---|---|---|
| `head.commit` | `bcf213e` | `e4d46db` |
| `worktree.pending_entries` | 40 | 1 |
| `worktree.staged` | 34 | 0 |
| `worktree.untracked` | 6 | 1 |
| `worktree.unpushed_commits` | 9 | **0** |
| `line_endings.files` | 165 | 171 |

| 因子 | 变化 | 触发证据 |
|---|---|---|
| L1-agent | 0.82 → 0.82 | VERID 属实验执行层，非通用 agent 能力 |
| **L1-lab** | **0.42 → 0.38** | 谷歌 VERID 在真实湿实验室跑通闭环（§2.4） |
| L2 | 0.65 → 0.65 | 80 → 87 产物；对象结构未变 |
| **L3** | **0.72 → 0.73** | 门禁建成 + 全部本地门禁通过（小幅，因 fix 分支未合并） |
| L4 | 0.30 → 0.30 | 无外部评审 |
| L5 | 0.32 → 0.32 | `loops_closed = 2` 未变 |
| **EEM 通用化** | **25% → 30%** | P004 两次复用同一闭环且扩展了验证器（§4.4 判断 3） |

**结论：一个因子上调、一个下调、四个不变；门槛 A/B/5 年全部持平；
EEM 通用化上调 5 个百分点。**

---

### 4.6 本日发现的两个度量缺陷（必须披露）

**缺陷一：`unpushed_commits` 口径错误，且报出过假警报。**

本地 git 的 `remote.origin.fetch` 原为
`+refs/heads/main:refs/remotes/origin/main`——**只跟踪 `main`**。
因此 `git rev-list --count --branches --not --remotes` 把**所有其它分支的提交**
都算作"未推送"，即使它们已在远端。

实测：修正 refspec 前 `--remotes` 下计数为 **10**；修正后为 **0**。
**两个读数都是"正确执行"，但含义完全不同。**

- 今天的正确读数：**`unpushed = 0`**（所有分支均已推送）
- 历史的 10-19 读数 `9`：在**旧口径**下正确，但当时**并非真的没推**
  （`fix/gate-and-brief` 的 `062ce86` 当时已在远端）

**已修**：refspec 改为 `+refs/heads/*:refs/remotes/origin/*`。
**新的语义边界**：`unpushed` 现在测的是"是否推到了某个远端"，
**不测**"是否合并到 `main`"。后者需要独立指标，见 `T17`。

**缺陷二：我在采集时覆盖了历史快照。**

重算 Δ 时，我对 `2026-10-19_ANRI_State.json` 重新跑了 `collect_state.py`，
**把历史值覆盖成了当前值**（`pending_entries` 40→1 等）。

**已从 `git show HEAD:...` 完整恢复**，并核对：`as_of_date=2026-10-19`、
`head.commit=bcf213e`、`pending_entries=40`、`unpushed=9`。

**教训**：快照是**历史事实**，只能新增不能重算。
`collect_state.py --date <过去日期>` 会写入**当前**状态而标上过去日期，
这是一个**危险的默认行为**——它让"重新采集"看起来像是在补记录。

**建议**：给 `collect_state.py` 加一个保护——若目标文件已存在且日期不是今天，
默认拒绝覆盖，需显式 `--force`。**本次未实现**（属代码改动，需单独验证）。

---

## 5. 高杠杆动作（按边际影响排序，≤5 条）

1. **合并 `fix/gate-and-brief` 入 `main`（9 个 commit，CI 已绿）。**
   这是当前唯一阻塞在门禁外的东西。合并后 `main` 才含 P004、
   `D-ANRI-004`、门禁修复与 80 个产物。
2. **给 `collect_state.py` 加历史快照保护**（见 §4.6 建议）。
   这是今天暴露的最危险默认行为——它能无声地毁掉跨日可比性。
3. **把 `unpushed` 与"未合并到 main"拆成两个指标**（新增 `T17`）。
   现在混在一起，导致今天的读数需要额外解释才能看懂。
4. **推进清室复现与盲测**（任务书与盲测脚本均已就绪，等舍友）。
5. **P004 Stage 3**：核实 `C_a`（回查附加质量标准表）。
   目前 `C_a = 0.1–1.0` 是**我的判断，不是引用**，这个缺口不补，
   P004 的结论始终带"未核实"标签。

---

## 6. 观察清单（触发条件检查）

| ID | 触发条件 | 阈值 | 状态（2026-10-20） |
|---|---|---|---|
| **T1** | 工作区仍有未提交内容 | 2026-10-14 | **🔴 已触发**（`pending_entries = 1`）。但该 1 项是 **本日报的状态文件本身**，属产生产物的副作用 |
| T2 | Ref-01S 仍无实验室回复 | 2026-10-25 | 未触发（pending） |
| T3 | 出现第二个 Research Object 且被他人复核 | — | 未触发（`research_objects = 1`，人工评审 0） |
| T4 | ClawsGO 或同类公布长时域指标 | — | 未触发（仍无指标公布） |
| T5 | 出现取代 AutoLab 的新长时域基准 | — | 未触发（人工） |
| T6 | 出现"探索图谱自动编译"公开实现 | 2027-02-01 | 未触发（人工） |
| T7 | 出现把审查状态机/发布门禁绑定哈希冻结产物的公开发表 | 2027-04-01 | 未触发。**VERID 的数字孪生 + 日志回溯属相邻但不同之物**：它保留过程记录，但未见哈希冻结与审查状态门禁 |
| T8 | 出现同参数的跨域/HAUV 垂直出水静水压基线 | 2027-04-01 | 未触发（人工） |
| T9 | A59 式对抗验证协议被领域期刊/会议正式采纳 | 2027-10-01 | 未触发（人工） |
| T10 | P003 Stage 1 仍有未解决 `Blocked` 单元格 | 2026-11-10 | **⚠️ 当日下午原地退役**：Stage 1 已重构为「无量纲组 + 迁移条件」，计数器由 4 归零。**但这不是「填上了值」，是「换了问法」** —— 义务由新增的 `T18` 承担，见下方说明 |
| T11 | 仍无独立人工评审 | 2027-01-09 | 未触发（读数 **0**） |
| T12 | 磐石或同类机构级平台公开其溯源规范且含哈希冻结或审查状态门禁 | 2027-04-01 | 未触发（人工） |
| **T13** | 本地提交仍未推送 | 2026-10-19 | **✅ 已解除**（`unpushed = 0`）。**但解除原因含口径修正**，见 §4.6 |
| T14 | 远端 CI 最近一次运行仍为 `failure` | 2026-10-20 | **未触发**（近几次运行均为 success） |
| T15 | `main` 与 `feat` 的文件数差仍 >50 | 2026-10-20 | **未触发**：`main` 与 `fix/gate-and-brief` 的差异是 9 个 commit，文件数差已不适用。**该触发条件的定义已过时**，应在 `main` 合并后重述 |
| T16 | 默认分支与「最近一次 CI 全绿所在分支」不一致 | 2026-10-26 | **✅ 已解除**（2026-10-20 合并后，`main` = `a09fda0`，CI 在 `main` 上 `push` 事件 success）。**不退役**：这是可复发条件 |
| **T17**（新增） | 长期分支领先 `main` 的 commit 数 ≥5 且持续 3 天以上 | 2026-10-27 | **✅ 已解除**（合并后 `origin/main..HEAD = 0`）。**不退役**：这是可复发条件，下次开长分支时会再次适用 |
| **T18**（新增） | CDFV-001 仍无独立规格（质量、几何、速度包线、姿态包线） | 2026-12-31 | **🔴 条件当前成立**。迄今所有数值都是 P002 圆柱按 scale 1.0 复用（`CDFV-001-Ref-01B`），而配置文档 §12 自己写着 not claimed to be the final CDFV-001 geometry |
| **T19**（新增） | P003 与 P004 仍均 `unresolved`，且未启动任何新实验或仿真 | 2026-11-20 | **🔴 条件当前成立**（两个问题均 `unresolved`；B1 尚未开始）。**这是 `D-ANRI-007` 的防回退判据**：写下「放下框架优先权」很容易，真正做到不容易 |

### 新增触发条件说明
**T10 退役与 T18 的关系（本日最需要说明的一条）。**
`T10` 的原判据是「数 P003 Stage 1 表里有几个 `Blocked`」。
Stage 1 重构后该计数归零，**`T10` 会静默解除** ——
而它本来要防的正是「用机制上的变化掩盖实质未推进」。
所以 `T10` 被**原地退役**（保留原文与原因），
它近似的那项义务由 `T18` 显式承担：
**CDFV-001 从来没有过自己的规格**。

**这是同一类处理方式的第二次**：`T15` 的前提失效时也是原地退役而非删除，
因为历次日报与决策记录都引用了它。
**计数器可以归零，义务不能。**


**T17 是对今天发现的度量缺陷的直接补丁。**
原 `T13` 把"未推送"与"未合并"混为一谈，修正 refspec 后 `T13` 自动解除，
但"成果不在默认分支"这个问题**依然存在**（9 个 commit 领先）。
T17 把这个真正的问题独立出来，并设了 3 天持续门槛，避免因单日波动误报。

**T15 需重述**：其原定义依据"`main` 与 `feat` 的文件数差 >50"，
但当前相关分支已变为 `fix/gate-and-brief`，且差异是 commit 而非文件。
**我不擅自改其定义**——留待 `main` 合并后一并重述，本日只标注"定义已过时"。

---

## 7. 来源

**上游（本日新增）**

- 谷歌 VERID / AI 智能体自主湿实验室闭环：科技日报 2026-10-19，
  新华网 2026-10-20 转载
  <http://www.xinhuanet.com/liangzi/20261020/fa4588c40b55449a909cfc62da2b335e/c.html>
- Fabarta AI4S 平台升级（2026-10-19）<https://www.tmcnet.com/usubmit/2026/10/19/10465327.htm>
- 中科院材料领域轻量化双模型协作智能体（2026-10-14，
  **正文访问受限 HTTP 418，仅记录标题**）
  <https://ecas.cas.cn/xxkw/kbcd/201115_150054/ml/xxhcxyyyal/202610/t20261014_5122221.html>
- 中国农科院"绿洲"智能体（**正文访问受限 HTTP 418，未采用**）
  <https://www.caas.cn/xwzx/kyhd/28164b3f0e7f4996a5749892288670bc.htm>

**仓库实测（本地命令）**

- `git ls-remote --heads origin` 耗时 4.4 s，exit 0
- `git push origin fix/gate-and-brief`：`74cdb84..e4d46db`，7.1 s，exit 0
- 5 个分支逐个核对：local == remote（全部 synced）
- `git rev-list --count origin/main..fix/gate-and-brief` = **9**
- 修正 refspec 前后：`--branches --not --remotes` = 10 → **0**
- `git status --porcelain`：1 项（`2026-10-20_ANRI_State.json`）
- `collect_state.py --date 2026-10-20`：`checks_all_ok = True`，`artifacts = 80`，
  `loops_closed = 2`
- `compare_snapshots.py --date 2026-10-20`：changed fields 6，triggers fired `['T1']`

---

## 8. 方法论声明

- **事实部分**仅来自：(a) 本地可执行命令与文件内容，(b) 上述公开链接的**正文**。
  二者在 §4.4 分列。访问受限的链接（HTTP 418）**只记录标题，不引用内容**。
- **概率部分全部是判断**，不来自测量。4.2 的因子与独立乘积仅用于检验量级与逐日对比。
- **本日披露两处自身失误**（§4.6）：`unpushed` 口径错误导致假警报；
  以及我覆盖了 10-19 的历史快照（已从 git 完整恢复并核对）。
  **两处均未以"读数变化"掩盖**——`T13` 的解除被明确标注为"含口径修正"。
- **一处口径判断**：`L1-lab` 因外部进展而**下调**。这个方向可能反直觉，
  理由已在 §4.4 判断 1 说明：外部可行性提高 ≠ 我方相对位置提高。
- **未做的事**：未尝试修复 `collect_state.py` 的历史快照覆写风险（只提出建议）；
  未重述 `T15` 的定义（留待 `main` 合并后）；未核实 Fabarta 与中科院两则的技术细节。
- **模板**：`Research_Log/Daily_Template.md`；**机制自检**：
  `py -3 .\scripts\check_report_mechanism.py`。
- **范围声明**：日报本身是日志，不纳入 Research Object 的 `artifacts` 哈希清单。

---

## 附录 A. 当日下午补充交付（本报告首次生成之后）

本报告 §0–§8 写于上午。之后又完成了四项交付，**`artifacts` 由 80 增至 87**。
本附录补记，不修改上文，以保留"当时怎么判断的"。

### A.1 四项交付

| # | 交付 | 位置 | 解决什么 |
|---|---|---|---|
| 1 | **失效模式报告** | `Reviews/ANRI_Failure_Mode_Report_v0.1.md` | `D-ANRI-001` 承诺但从未交付的产出。17 条按"检测为何失效"分类 |
| 2 | **冷启动 CI** | `.github/workflows/anri-validation.yml` 的 `cold-start` job | 五层检测全部在有 `.git` 的树里运行；此 job 在导出树上重复验证 |
| 3 | **覆盖矩阵** | `Reviews/Ref-01B_Verifier_Coverage_Matrix.md` + `Benchmarks/ANRI-RV-001/coverage_probe.py` | 逐列扰动测出 13/26 个扰动对门禁不可见 |
| 4 | **敏感性分析** | `Research_Planning/P004_Sensitivity_Analysis.md` + `scripts/p004_sensitivity.py` | 检验 P004 的两条结论对输入错误的稳健性 |

### A.2 四项交付各自推翻了一个我的判断

这是本附录值得单独写的原因——**四项里有三项直接更正了我先前的说法**。

| 交付 | 我原先的判断 | 实测结果 |
|---|---|---|
| 失效模式报告 | `F7 machine-specific paths` 已修复 | **只在有 `.git` 的工作副本里成立**；导出树失败 |
| 冷启动 CI | `..` 检查已足够 | **不够**：家目录存在 `.git` 时根定位到用户主目录，路径不含 `..`，检查失效 |
| 覆盖矩阵 | 生成器 bug 会产出"完全验证通过"的错误物理 | **不会**：`buoyancy_unit_sanity` 在 1e-6 相对容差上钉死浮力量级 |
| 敏感性分析 | Stage 2 的"102%"需要撤回 | **不需要**：原文已明确写的是"机体惯性"；需要改的是 §12.5 的推理 |

**结论：本项目的四层检测（校验器/负例/对抗/自检）加上我的人工复核，
在一天内被同一批新工具否证了四次。**

### A.3 敏感性分析的关键结论（对概率评估的影响）

P004 的两条判断稳健性差异极大：

| 判断 | 余量 | 翻转所需输入误差 |
|---|---:|---|
| C1：P002 区间（≤0.15 m/s²）内附加质量可忽略 | **55–102 倍** | 输入错 ~55 倍 |
| C2：~1 g 时与吸入力同级 | **坐在边界上** | **输入错 ~1.7 倍，或直径错 19%** |

**这意味着 `L5` 的 0.32 不应因 P004 的完成而上调**——它完成的是"流程走通"，
而研究结论本身只有 C1 一条能被坚定主张。

**故 §4.2 的 `L5 = 0.32` 维持不变。本日不作概率调整。**

### A.4b 合并完成（当日晚间）

PR #2 已合入 `main`（`a09fda0`，28 个提交，快进，无 merge commit）。
GitHub 记录 `merged: True`。`main` 上 CI 的 `push` 事件 success。

**合并方式**：本地快进 + 推送 `main`，行使管理员 bypass。
原因与代价见 `Research_Planning/Decision_Log.md` 的 `D-ANRI-005`。
该条记录随本次合并一同进入 `main`。

**副作用**：`T16`、`T17` 两个触发器解除（条件满足）。
**二者均不退役**——它们描述的是可复发条件。

### A.4 一项对 `T10` 的升级建议

`D002-002` 的解除条件原为"取得 CDFV 加速度剖面"。
敏感性分析显示**还需要 CDFV-001 的实际直径**：`a_be` 与 `D` 的三次方成反比，
**直径错 19% 就足以翻转 C2**。

建议把 `T10`（CDFV 四个参数）中的"主体几何"从"影响 material 判定"
升级为"**决定 P004 结论能否被引用**"。

### A.5 本附录的局限

- 四项交付**均未经外部复核**（`independent_human_reviews = 0`）；
- §A.2 的"三项推翻了我的判断"是**我的自评**，
  外部读者可能对"是否算推翻"有不同判断；
- 冷启动 CI 已在 PR 上验证通过（run `39401365718`），
  但**尚未随 `main` 合并**，故 `main` 上还没有这道门禁。
