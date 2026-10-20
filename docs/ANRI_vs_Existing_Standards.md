# ANRI 与既有标准的关系（骨架，含已核实与待填部分）

> **用途**：论文 related work 的基础，以及回答审稿人第一个问题
> "这跟已有工作有什么区别？"
>
> - 建立日期：2026-10-20
> - **状态：骨架。§2 已联网核实；§4 是本文档最重要的部分；§6 全部为空槽**
> - ⚠️ 撰写时网络刚刚恢复，**核实不完整**。凡标 `[待核实]` 者不得直接写入论文。

---

## 1. 为什么必须有这份文档

审稿人问的第一个问题不会是"你的方法好不好"，而是：

> **"这和 RO-Crate / PROV-O / 那个 IETF 草案有什么不同？"**

**答不上来 = 直接退稿。** 而本仓库此前对这些**一处都没有引用**（2026-10-20 实测：`RO-Crate` 0 处、
`ResearchObject.org` 0 处、`W3C PROV` 0 处、`FAIR` 0 处）。

---

## 2. 已核实：三个既有体系

### 2.1 RO-Crate（Research Object Crate）

| 项 | 已核实内容 |
|---|---|
| 当前版本 | **RO-Crate 1.3**（长期发布版）；1.2 为稳定版；社区正在做 RO-Crate 2（模块化） |
| 性质 | **打包与元数据规范**——用 JSON-LD 描述"一个研究对象包含什么" |
| 结构 | Root Data Entity / Data Entities / Contextual Entities / **Provenance** / Profiles / Workflows and scripts |
| 许可 | Apache 2.0 |
| 治理 | 社区（University of Technology Sydney、University of Manchester 等） |
| 来源 | <https://www.researchobject.org/ro-crate/specification.html> |

**关键判断**：RO-Crate 规定**如何描述与打包**，**不规定如何验证**。
它没有校验器、没有通过/失败判据、没有 review 状态机。

> **这可能是 ANRI 最干净的差异点**：RO-Crate 管"装"，ANRI 管"判"。
> **但此判断需确认**——RO-Crate 是否有配套验证工具，`[待核实]`。

### 2.2 W3C PROV（PROV-DM / PROV-O）

| 项 | 已核实内容 |
|---|---|
| 性质 | **溯源本体**（W3C Recommendation 系列） |
| 作用 | 描述"谁在何时用什么产生了什么" |
| 来源 | <https://www.w3.org/TR/prov-o/>、<https://www.w3.org/TR/prov-dm/> |

**关键判断**：PROV 是**描述语言**，不是**验证机制**。
它能让溯源可交换，但不判断结果对不对。

**ANRI 目前的问题是**：自己的 `provenance` 字段是**自创结构**，未对齐 PROV。
这是一个**可修**的弱点，也是一个**可写的贡献点**（对齐后即可与既有工具互操作）。

### 2.3 FAIR 原则

| 项 | 已核实内容 |
|---|---|
| 性质 | **数据管理原则**（Findable, Accessible, Interoperable, Reusable） |
| 不是 | 不是工具，不是规范，不含验证 |
| 原始出处 | Wilkinson et al., *Scientific Data*, 2016, doi:10.1038/sdata.2016.18 |

**关键判断**：FAIR 与 ANRI **不重叠**。FAIR 管"能不能被找到和复用"，不管"结果对不对"。

---

## 3. ⚠️ 最重要的发现：一份 IETF 草案已经覆盖了 ANRI 的核心概念框架

### 3.1 事实（已核实）

**`draft-watts-research-artifact-provenance-00`**
"Research Artifact Provenance and Corrigible Scientific State"
D. Watts（独立研究者），**2026-10-08 发布**，Informational，2027-04-11 过期。
来源：<https://www.ietf.org/archive/id/draft-watts-research-artifact-provenance-00.html>

**其摘要原文**：

> "This document describes a protocol-neutral pattern for content-addressed research
> artifacts, append-only evidence history, explicit epistemic classes, and corrigible
> active scientific state. **It separates byte integrity from numerical correctness,
> empirical adequacy, mechanism identification, and release authority.**"

### 3.2 逐条对照：它已经说了 ANRI 说过的话

| 概念 | Watts 草案 | ANRI 现状 |
|---|---|---|
| 内容寻址产物 + 加密摘要 | ✅ §2 | ✅ 95 个哈希注册产物 |
| **区分字节完整性与数值正确性** | ✅ **摘要直述** | ✅ 失效报告的核心论点 |
| 追加式历史 | ✅ §4 | ✅ `Decision_Log` 修订记录 |
| 显式认知类别（ESTABLISHED / DERIVED / CONJECTURE…） | ✅ §3 | ⚠️ 有 review status，未形式化 |
| 结论可被推翻/撤回，但历史不可改 | ✅ §4 | ✅ 触发器"原地退役"即此原则 |
| 矛盾证据并存，不得静默平均 | ✅ §5 | ⚠️ 未显式处理 |
| 复现记录需含代码/环境摘要、容差 | ✅ §6 | ✅ `verification.json` 含容差 |
| "通过复现只说明通过了所声明的测试" | ✅ §6 | ✅ **覆盖矩阵正是这句话的量化** |
| 发布是治理行为，独立于科学地位 | ✅ §7 | ⚠️ 有 review gate，未区分 |
| 威胁模型含摘要替换、溯源伪造 | ✅ §8 | ⚠️ 仅有哈希，无伪造模型 |

**结论：ANRI 的"概念框架"部分，基本已被这份草案在 12 天前公开覆盖。**

### 3.3 这对我原定论文主张的影响

我在 `Paper_Outline_FailureModes.md` §5.1 把"**哈希冻结保证完整性，不保证正确性**"
列为论文第三项贡献，并写了标题候选
*"Hash-frozen is not verified"*。

> **该主张不能再作为新颖性声明。** 必须改为引用 Watts 草案，
> 然后把论文定位为**对这套原则的一次实现与失效测量**。

**这实际上让论文更稳，不是更弱**：
"有人提出了原则，我们实现了它，并测量了它在哪里断" —— 这是**有力的实证贡献**，
而"我们提出了一个原则"在有人先说过之后反而是弱点。

---

## 4. 论文的新颖性还能站在哪里（2026-10-20 联网核实后修订）

> **§5 的三篇论文全文摘要已读。结论：新颖性比我原先估计的更窄，但有一处站得住。**

|候选贡献|状态|依据|
|---|---|---|
|① "通过测试"不等于"正确"这一**观察**|❌ **已被三处独立报告**|见 §5.2、§5.3、§5.4|
|② **量化**门禁看不见什么（13/26 覆盖矩阵）|⚠️ **形式相近者已存在**|ReproScore 在 423 个仓库上量化了 readiness–outcome 差距（§5.3）|
|③ "修复只在测试环境成立"（F7 类）|**可能仍新颖**|三篇均未涉及**跨环境可移植性**这一具体机制|
|④ 区分完整性与正确性|❌ 已被覆盖|Watts 2026-10-08（§3）|
|⑤ 内容寻址 + 追加历史|❌ 已被覆盖|Watts、RO-Crate、PROV|
|⑥ 复现记录需含容差|❌ 已被覆盖|Watts §6|

**核心判断**：ANRI 的**观察**（测试通过≠正确）已不是新鲜事。
**真正可能还空着的，是"跨环境失效"这一类**——但要立住它，样本只有 2 条（F7、G-1），**太薄**。

---

## 5. 已核实的相邻工作（逐篇读过摘要）

### 5.1 Watts, IETF draft-00（2026-10-08）

见 §3。**概念框架已被覆盖。**

### 5.2 Bai et al., *When Passing Tests Hides Vulnerabilities*（arXiv:2609.10548，2026-06-25）

**这是方法上最接近 ANRI 的一篇。**

摘要核实要点：

- 研究对象：LLM 代码修复代理的**静默失效**（通过了语法与功能验证，但仍保留或引入安全漏洞）
- 规模：**1,030 条有效执行轨迹**，7 个代理框架，2 个安全数据集
- 编码方法：**三轮定性编码 + 人工核验**，确认 **170 条静默失效**
- 分类：**3 个主类 + 10 个细粒度编码**（Omission 48.2% / Introduction 30.6% / Inadequacy 21.2%）
- 关键结论(iii)：**"Current test-passing evaluation and LLM-based reviewer roles were
  insufficient to expose or intercept these failures"**

| 与 ANRI 的对比 | ANRI | Bai et al. |
|---|---|---|
| 分析单元 | **检查器自身的盲区** | **被检查者的失效** |
| 样本 | 26 条缺陷，1 个项目 | 170 条，1,030 轨迹 |
| 编码程序 | **无** | **三轮定性编码 + 人工核验** |
| 评分者间信度 | **无** | 有（编码迭代）|

**威胁**：它已经说了"通过测试不等于正确"，**而且方法远比 ANRI 严谨**。

**机会**：它的分析单元是**代理的缺陷**，不是**检查器的盲区**。ANRI 的 7 类里
A 类（检查式子里写进假设）、C 类（度量在测别的东西）讨论的是**检查器自己**，
这一层它没有做。

### 5.3 Samuel et al., *ReproScore*（arXiv:2605.13275，2026-05-13）

摘要核实要点：

- 命名了一个现象：**"the readiness–outcome conflation"**——把"仓库里有什么"当作"能不能跑"的代理
- 两层框架：readiness (RRS) 与 outcome (ROS)
- **RRS 含 26 个子指标，5 个类别**
- 在 **423 个 GitHub 仓库**上评估，跨 5 种失效模式
- 关键结论：**"RRS exhibits near-zero binary success correlation, empirically quantifying
  the readiness–outcome gap at repository scale"**

**这是 ANRI 覆盖矩阵的"大规模版本"**：两者都在量化"检查项通过"与"实际正确"的差距。
差别只在对象（研究软件仓库 vs 单个研究对象的产物门禁）与规模（423 vs 1）。

**威胁**：如果 ANRI 的核心贡献表述为"我们量化了门禁的盲区"，**这篇已经做了，而且规模大三个数量级。**

### 5.4 Kohrt, Melinscak, McElreath, Schönbrodt（Zenodo 10.5281/zenodo.14007038，v2 2024-10-29）

- 来源：DFG META-REP (SPP 2317)，LMU München / Wien / MPI-EVA
- 主题：**复现的结果、错误及其认知功能的正式定义**
- 关键词含 **"honest errors"**、**"reproduction success"**、**"formal model"**

**威胁**：它给了"错误"的正式定义。ANRI 的失效分类若与之冲突会被质疑。
**必须先读全文再写 related work** —— 本条**仍未读全文**，只读了元数据。

### 5.5 已核查但判定**不构成威胁**

| 工作 | 为什么不是威胁 |
|---|---|
| Strickland et al.（arXiv:2603.06394，2026-03-06）*Talk Freely, Execute Strictly* | 研究对象是 **LLM 编排的 schema 门控**（execution determinism vs conversational flexibility），评审 20 个系统。**与验证器失效无关** |
| CODECHECK（codecheck.org.uk） | 人工代码检查工作流，是**流程倡议**，非失效分析 |
| arXiv:1609.00331 | "验证器本身也需要被信任"——**这是同一问题的早期表述，应引用** |

---

## 5.6 由这批文献得出的一个不舒服的结论

**ANRI 的方法学严谨度低于它所在领域的现有水准。**

| 维度 | 该领域 | ANRI |
|---|---|---|
| 样本 | 170 / 1,030 / 423 | **26 / 1** |
| 编码程序 | 三轮定性编码 + 人工核验 | **无** |
| 评分者间信度 | 有 | **无** |
| 复现性 | 数据集公开 | 产物哈希冻结（**这一项 ANRI 更强**）|

**因此：ANRI 不能靠"方法更严谨"取胜，只能靠"对象不同"取胜。**
若对象差异（检查器自身的盲区、跨环境失效）不足以支撑一篇论文，
**那么诚实的结论是：这个题目已经被更好的团队做过了。**

**该判断必须在动笔前接受或否证，不能绕过。**
## 6. 空槽：必须由你填的部分

> **以下每一项都必须读原文后填写。不得凭标题推断。**

- [ ] **§2.1** RO-Crate 是否有配套验证/校验工具？若有，与 ANRI 的差异是什么？
- [ ] **§2.2** ANRI 的 `provenance` 结构能否映射到 PROV-DM？映射成本多大？
- [ ] **§5** *The logic of computational reproductions* 全文：它的"错误"分类与 ANRI 的 7 类是否重叠？
- [ ] **§5** arXiv 2603.06394 的 20 系统对比表：其中是否已有"验证器失效分析"？
- [ ] **§5** arXiv 2607.27556 的成熟度框架（V1–V?）：ANRI 落在哪一级？
- [ ] **§5** Modelstamp 的威胁模型：ANRI 缺哪些？
- [ ] **§4** ①②③ 三项的一次系统检索（关键词：verification failure taxonomy /
      reproducibility tool evaluation / silent failure of automated checks）
- [ ] **§2.3** FAIR 是否已有"FAIR 与可验证性关系"的既有讨论？

---

## 7. 对投稿策略的影响（判断）

| 影响 | 说明 |
|---|---|
| **不能投"提出框架"类 venue** | 框架已被 Watts 覆盖 |
| **应投"实证/评估"类 venue** | F1000Research、eScience、JORS 这类接受 case study |
| **必须主动引用 Watts** | 否则审稿人会认为你没做检索，这比重叠更致命 |
| **时间压力真实存在** | Watts 草案 2026-10-08 发布，若他继续推进到 RFC，框架层面的话语权将完全归他 |
| **但 ANRI 的位置不差** | "实现 + 测量失效"这条路上，目前没看到有人公开做 |

**一句话**：
> 你原本想以"提出者"身份进入，但那个位置已经有人占了 12 天。
> **"第一个认真测量这套原则在实践中怎么坏掉的人"这个位置仍然空着**——
> 而且它比"提出者"更难被抢，因为它需要真的做出来并记录失败。

---

## 8. 方法论声明

- **已核实部分**：RO-Crate 版本与结构、PROV 的性质、FAIR 的出处、
  Watts 草案的全文与日期——均来自上述 URL 的正文，2026-10-20 取。
- **判断部分**：§4 的新颖性排名、§7 的投稿策略，**均为判断**，且**基于不完整的检索**。
- **明确未做**：未读 §5 中任何一篇的全文；未做系统性文献检索
  （仅三次关键词搜索）；未核实地引用格式与 DOI。
- **使用限制**：**本文件不得直接作为 related work 使用。**
  它是待填骨架；把它当文献综述引用会产出错误陈述。
