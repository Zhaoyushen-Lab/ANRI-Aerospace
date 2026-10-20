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

## 4. 论文的新颖性还能站在哪里（我的判断）

| 候选贡献 | 是否可能新颖 | 依据 |
|---|---|---|
| **① 基于实现的失效分类法（7 类 26 条）** | **可能新颖** | 未检索到同类"对验证工具自身的失效分类"；`[待核实]` |
| **② 覆盖矩阵：量化门禁看不见什么（13/26）** | **可能新颖** | Watts §6 说了"通过只说明通过了所声明的测试"，但**没有量化**；`[待核实]` |
| **③ "修复只在测试环境成立"（F7 类）** | **可能新颖** | 未检索到；`[待核实]` |
| ④ 区分完整性与正确性 | ❌ **已被覆盖** | Watts 2026-10-08 |
| ⑤ 内容寻址 + 追加历史 | ❌ 已被覆盖 | Watts、RO-Crate、PROV |
| ⑥ 复现记录需含容差 | ❌ 已被覆盖 | Watts §6 |

**若 ①②③ 都站得住，论文仍然成立**，但标题和引言必须重写：
从"我们发现了一个区别"改为"**我们测量了一个已被提出的原则在实践中失效的方式**"。

---

## 5. 其他已发现的相邻工作（`[待核实]`，仅有标题与片段）

| 工作 | 为什么相关 |
|---|---|
| *The logic of computational reproductions: Formal definitions of outcomes, errors, and their epistemic function* | **形式化定义了复现的"结果"与"错误"**——与失效分类法直接相邻，**必须读全文** |
| *A conceptual framework for computational reproductions* | 同上 |
| **ReproScore**: Separating Readiness from Outcome in Research Software Reproducibility Assessment | 区分"就绪度"与"结果"——与 ANRI 的 review 状态机相邻 |
| **MIRROR**: Local Evidence Bundles for Reproducible Research Software Review | 本地证据包——与 ANRI 的产物打包相邻 |
| **Modelstamp**（论文片段提到"rejected the tested artifact modifications and authentication violations covered by its stated guarantee"） | 有安全保证的产物验证系统——**威胁模型比 ANRI 完整** |
| arXiv 2607.27556（片段："most systems implement multiple Function and Evidence dimensions, yet the majority remain at V3"） | 像是一份**成熟度调查**，可能已有系统对比表 |
| arXiv 2603.06394（片段："Table 3 summarizes 20 representative systems"） | **20 个系统的对比表**——必须逐一比对 |

**这批全部需要读全文。仅凭标题与片段不足以判断重叠度。**

---

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
