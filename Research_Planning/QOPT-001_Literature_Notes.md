# QOPT-001 文献笔记：水下非声探测 / 量子光学路线

> **状态：模板 + 首轮种子清单。无任何数据，无任何结论。**
> **本文件不是文献综述。它是"读什么、怎么记、记什么"的规约。**
>
> **为什么先做这个**：`D-ANRI-012` §7 记录新方向为量子光学。
> 在该方向出现第一个可注册结果之前，唯一真实存在的东西是"读过哪些文献"。
> **故先建笔记本，不建对象、不建仓库。**

---

## 0. 这份文件与 `P003_Literature_First_Pass.md` 的关系

**同构**。那份文件在流体领域建立了"文献身份 → 它做了什么 → 与本问题的边界 →
可用的条目 → 方法论声明"的结构；本文件把它搬到量子光学。

**新增一节（§4 可复现性）**——这是 ANRI 的入口，也是本方向最缺的东西。

---

## 1. 检索策略（必须可复现）

**文献检索本身要可复现，否则它不构成证据。**

| 项 | 填写 |
|---|---|
| 数据库 | Scopus / Web of Science / IEEE Xplore / Optica / 知网 |
| 检索词（英文） | `quantum illumination` + `underwater`；`entangled` + `underwater` + `detection`；`optical` + `wake` + `submarine` |
| 检索词（中文） | `量子照明`、`水下非声探测`、`尾迹光学`、`纠缠光子 水下` |
| 检索日期 | （填） |
| 时间范围 | 2008 起（QI 提出的年份） |
| 纳入标准 | （填） |
| 排除标准 | （填） |

> **注意**：本方向大量工作不公开，故**公开文献的"稀疏"本身不等于"没人做过"**。
> 这一点必须写进任何综述的局限里。

---

## 2. 记录格式（每篇一条，逐项填）

**不要写成"某某等人研究了……"。那是摘要的复述，不是笔记。**

```markdown
### [编号] 作者, 标题, 期刊/会议, 年, doi

**类型**：理论 / 数值 / 实验 / 综述

**它做了什么**：（一句话。如果写不出一句话，说明还没读懂）

**它声称的优势**：
- 优势指标是什么？ ☐ 错误指数 error exponent  ☐ 信噪比 SNR  ☐ 探测距离  ☐ 其他
- 对谁的优势？**具体的经典基准是什么**？（见 §5 陷阱二）
- 量子增益的数值：____ dB / ____ 倍

**它的物理假设**：
- 损耗：____ dB/m 或等价
- 湍流模型：☐ 无 ☐ Nikishov ☐ 其他 ____
- 背景噪声水平：____
- 是否假设理想单光子源 / 探测器？ ☐ 是 ☐ 否

**与本问题的边界**：
- 水下还是水面？____
- 距离量级？____
- 与"水波-光波相互作用"的关系？近 / 远 / 无关

**★ 可复现性（ANRI 入口）**：
- ☐ 有公开代码  ☐ 有公开数据  ☐ 只有参数表  ☐ 什么都没有
- 若无可复现材料：**复现它最少需要什么？** ____
- 它的数值结果是否依赖未公开的调参？____

**结论 / 我的判断**：（一段，明确标注是判断）
```

**最后一项最容易被跳过，但它是本笔记的核心产出。**

---

## 3. 首轮种子清单

> ⚠️ **以下为 2026-10-20 一次联网检索的结果，只读了标题与来源页面。
> 未读正文，故每条的"它做了什么"全部待填。不得当作已读文献引用。**

| # | 文献 | 来源 | 与本方向的关系 |
|---|---|---|---|
| S1 | **Underwater Target detection with quantum illumination**（会议论文） | NSTL 国家科技图书文献中心 | **直接对应**——水下 + QI + 探测 |
| S2 | **Quantum illumination using polarization-entangled photon pairs for enhanced object detection**, *Optics Express* **32**(23): 40150 (2024) | opg.optica.org | 顶刊；偏振纠缠实现 |
| S3 | **Entangled Quantum Imaging in Nikishov Underwater Turbulence Environment** | IEEE | 含**湍流模型**（Nikishov）——物理假设最具体 |
| S4 | 海面对光学成像探测影响的研究（中文） | 《光学学报》系（知网 `JGHW202110009`） | 中文线；**水面**而非水下 |
| S5 | **Fluid lensing and applications to remote sensing of aquatic environments** | Stanford 学位论文（J. J. Alonso） | 光-水面相互作用，偏遥感 |

**据我记忆、待核实的奠基性文献** —— **已于 2026-10-20 核实，见 §3A。**

---

## 3A. 奠基文献核实结果（2026-10-20）

**核实方法与依据**：查 Science DOI 页、ADS 记录、并下载该综述全文（14 页）
核对其参考文献表。**PDF 已存 `Paper_Library/QOPT_QI_QuantumRadar_Overview_2023.pdf`。**

### 3A.1 ★ 先记这一篇：它是整个领域最好的入口

> **Karsa A., Fletcher A., Spedalieri G., Pirandola S.**
> ***Quantum Illumination and Quantum Radar: A Brief Overview***.
> **arXiv:2310.06049**（综述，14 页，已精读）

**为什么先读它**：它把 QI 的历史、协议、经典基准、实验进展、以及**所有批评**
都梳理了一遍，并给出了全部奠基文献的规范引用。

### 3A.1b ★★ 已核实到底的引文（可直接引用）

**以下引自该综述的参考文献表，页码与 DOI 均已核对：**

| # | 完整引用 |
|---|---|
| **F1** | **S. Lloyd, "Enhanced sensitivity of photodetection via quantum illumination," *Science* 321, 1463 (2008). doi:10.1126/science.1160627** |
| **F2** | **S.-H. Tan, B. I. Erkmen, V. Giovannetti, S. Guha, S. Lloyd, L. Maccone, S. Pirandola, J. H. Shapiro, "Quantum illumination with Gaussian states," *Phys. Rev. Lett.* 101, 253601 (2008).** |
| **F4** | **J. H. Shapiro and S. Lloyd, "Quantum illumination versus coherent-state target detection," *New J. Phys.* 11, 063045 (2009). doi:10.1088/1367-2630/11/6/063045** |
| **F3** | **J. H. Shapiro, "The quantum illumination story," *IEEE Aerosp. Electron. Syst. Mag.* 35(4), 8–20 (2020). doi:10.1109/MAES.2019.2957870** |
| **F5** | Sacchi M. F., "Entanglement can enhance the distinguishability of entanglement-breaking channels," *Phys. Rev. A* 72, 014305 (2005). — **QI 的前身** |
| **F6** | Audenaert et al., "Discriminating states: the quantum Chernoff bound," *Phys. Rev. Lett.* 98, 160501 (2007). — **QCB 工具** |

> **✅ 上一版标"未确认"的两条现已全部确认：Lloyd 页码确为 1463；F4 确为 Shapiro & Lloyd, NJP 11, 063045 (2009)。**

---

## 3B. 综述精读：四道硬约束与一个关键结论

> **本节的每个数字都摘自综述正文，不是推断。**

### 3B.1 ★ 结论段原文（最重要，直接决定方向判断）

> "Despite many advances in QI, **the possibility of a quantum radar still seems to be far in the future.**"
>
> "Type-3 designs, based on entanglement distribution (like QI), appear to be **too fragile to loss**
> to be implemented in a practical microwave scenario."
>
> "it is **extremely unlikely** to foresee any near-term development of a **long-range** quantum radar."
>
> "currently there is **low chance of potential military use** of QI-based technology."
>
> **但**："applications of QI appear to be **feasible for short-range detection of fixed or
> slowly-moving objects.**"
>
> 举例：**"quantum-enhanced scanning of metallic objects in a surveillance scenario"**；
> 以及低光子数的**生物医学**场景。

**即：长程不行，短程可以。**

### 3B.2 四道硬约束（每一条都能否掉一个方案）

| # | 约束 | 具体数字 |
|---|---|---|
| **①** | **Idler 存储效率** | `η_I ≥ 1/4` 才有任何量子优势；**`η_I ≥ 1/2` 才能胜过成对 LOCC 测量**。存储手段：光纤延时线，或量子存储器（**"still a technology very much in its infancy"**） |
| **②** | **接收机只能拿到一半** | 最优联合测量实验上极难。实用接收机（OPA、相位共轭）只实现 **3 dB**，而理论上是 6 dB |
| **③** | **光源** | 需要**高时间带宽积的最大纠缠模对**。微波段靠约瑟夫森参量放大器，但"这些信号极微弱，放大到室温会严重破坏量子特性" |
| **④** | **测距** | QI 只解决"有/无"，**测距是另一个问题**，综述单列讨论 |

### 3B.3 我此前给的"四个区制条件"已被证实

**综述给出 Gaussian QI 的对比式（Eq. 15 与 Eq. 17）**：

```
QI：      P_err ≤ ½ exp(−M κ N_S / N_B)
相干态：   P_err ≤ ½ exp(−M κ N_S / 4 N_B)
                              ↑ 比值 4 = 6 dB，且"被证明是理论上最大的"
```

**成立条件（综述明确列出）**：`N_S ≪ 1`、`M ≫ 1`、`κ ≪ 1`、**`N_B ≫ 1`**。

> **✅ 我上一版写的四个条件，与综述一致。**

### 3B.4 对水下应用的含义（判断）

**综述虽然主要谈微波量子雷达，但它的结论对水下的启发很直接：**

| 综述的话 | 水下对应 |
|---|---|
| "short-range detection of **fixed or slowly-moving** objects" | **水雷、静止目标、缓慢的 UUV** |
| "quantum-enhanced **scanning** of metallic objects" | 金属目标扫描（水雷就是金属壳体） |
| 长程不可行 | **不适用于反潜** |

> **所以：水下 QI 的可行定位是"短程、静止或慢速、金属目标"。**
> **这恰好覆盖水雷与港口防御，不覆盖潜艇搜索。**
>
> **这与我在会话中给出的"窄场景补充手段"判断一致，且有综述原文支持。**

### 3B.5 一个必须记的批评线索

**综述明确指出**：早期在**低背景噪声**区制下，经典相干态**追平** QI（引 F4）。
**6 dB 优势只在 `N_B ≫ 1`（强背景噪声）时出现。**

> **但水下光学是低背景噪声环境**（没有太阳直射、没有室温热噪声主导）。
>
> **⚠️ 这是本方向最大的技术疑问：水下到底落在 `N_B ≫ 1` 还是 `N_B ≪ 1`？**
> **如果在后者，6 dB 优势不出现，整个水下 QI 方案的价值要重新论证。**
>
> **这一条必须在读任何"水下 QI"论文时第一个查。**


**读它一篇，等于拿到一份带注释的文献地图。**

### 3A.2 三条奠基文献的核实状态

| # | 文献 | 状态 |
|---|---|---|
| **F1** | **Lloyd S., *Enhanced Sensitivity of Photodetection via Quantum Illumination*** | **标题与期刊已确认**（Science, DOI `10.1126/science.1160627`；同卷有报道文章 Science **321**(5895): 1433a）。**卷 321 已确认；页码 1463 未直接确认** |
| **F2** | **Tan S.-H., Erkmen B. I., Giovannetti V., Guha S., Lloyd S., Maccone L., Pirandola S., Shapiro J. H., *Quantum Illumination with Gaussian States*** | **已确认**：**Phys. Rev. Lett. 101, 253601 (2008)**（ADS bibcode `2008PhRvL.101y3601T`） |
| **F3** | **Shapiro J. H., *The Quantum Illumination Story*** | **已确认**：**IEEE Aerospace and Electronic Systems Magazine, 2020**（ADS bibcode `2020IAESM..35d...8S`，卷 35，期 4） |

### 3A.3 ⚠️ 我漏了一条更关键的

**F3 只是 2020 年的综述性回顾。真正建立"经典基准"的是更早的一篇：**

| # | 文献 | 作用 |
|---|---|---|
| **F4** | **Shapiro J. H., 2009**（综述中记为 `shapiro2009quantum`） | **建立了相干态经典基准**，并证明：在**低背景噪声**区制下，经典相干态的表现**追平** Lloyd 的 QI，**当时找不到量子优势** |

**⚠️ F4 的准确出处我尚未确认**（作者、卷期、是否是 PRA 或其他刊）。
**在确认之前不得引用。**

**为什么 F4 重要**：**它是"量子优势是相对于什么"这个问题的原始答案。**
**不读 F4，会以为 QI 一提出就赢了——实际上它先输过一阵。**

### 3A.4 ★ 必须记录的技术前提（这条改变了"6 dB"的分量）

**综述明确给出**：Gaussian QI 的 **4 倍（= 6 dB）优势**是在以下**四个条件同时成立**时：

| 条件 | 含义 |
|---|---|
| `N_S ≪ 1` | **信号极弱**（每模光子数远小于 1） |
| `M = T·W ≫ 1` | **时间带宽积极大** |
| `κ ≪ 1` | **目标反射率极低** |
| **`N_B ≫ 1`** | **背景热噪声极强** |

**原文表述（据综述）**：QI 的错误指数是 `exp(−M κ N_S / N_B)`，
相干态基准是 `exp(−M κ N_S / 4 N_B)`，**比值为 4**，
且**"此 6 dB 优势被证明是理论上最大的"**。

> **关键含义：6 dB 优势只存在于"强噪声、弱信号、低反射率、大时间带宽积"这个区制。**
> **在低噪声区制下，经典相干态追平 QI（Shapiro 2009）。**

**这对水下应用意味着什么**：**必须查清水下光学的 `N_B`（背景噪声）落在哪个区制。**
**如果水下背景噪声不够强，6 dB 优势不出现——这是判断任何"水下 QI"论文价值的第一道筛子。**

---

## 4. 读之前必须先懂的三个概念

**不搞清这三个，读这些论文会误判它们的价值。**

### 4.1 量子照明（QI）到底做什么

**不是"提高信号强度"。**
它用纠缠光子对：一个（idler）留在本地，一个（signal）去探目标。
**通过联合测量判断"目标在不在"。**

**关键**：它解决的是**在强噪声强损耗下、用极低光子数判"有/无"**这件事。

### 4.2 "6 dB 优势"指的是什么

**指错误概率随模式数衰减的速率（error exponent）上的优势，不是信噪比上的优势。**

**这两者常被混为一谈**，而混谈会让一篇论文看起来比它实际强得多。

**每篇论文必须记清：它的优势指标是哪一个。**

### 4.3 经典基准（classical benchmark）

**量子优势永远是"相对于某个经典方案"的优势。**

**如果那个经典方案选得弱，量子优势就大——但那不说明问题。**

**这是本方向最主要的争议来源。**

---

## 5. 这个领域特有的四个陷阱

| # | 陷阱 | 怎么识别 |
|---|---|---|
| **一** | **过度宣称**："量子 + 某应用"的组合在基金与媒体里被大量使用，兑现比例不高 | 看它有没有给出**具体的、可比的**经典方案 |
| **二** | **优势指标偷换**：把 error exponent 的优势说成探测性能优势 | 见 §4.2。**每篇都查这一条** |
| **三** | **湍流/损耗模型的现实性**：Nikishov 谱是模型，不是实测海水 | 记清它假设了什么，别把模型的结论当成海的结论 |
| **四** | **理想器件假设**：假设理想单光子源与零暗计数 | 看它有没有讨论非理想器件下的退化 |

**第 二 条是本方向最需要警惕的，因为它是纯技术性的、不易被察觉。**

---

## 6. 本笔记对 ANRI 的意义

**数值量子光学恰好是复现性最差的领域之一**——protocol、参数、测量方案常不可复现。

**而 §2 的"可复现性"一栏，就是这个方向上的第一个缺口探针。**

**如果读完 10 篇之后发现 10 篇都不可复现，那就是一个真实、可发表、且很 ANRI 的发现。**

> **这条不构成承诺。它只是说明：为什么这份笔记的格式值得先定下来。**

---

## 7. 方法论声明

- **事实部分**：§3 的 S1–S5 来自 2026-10-20 的联网检索结果（标题与来源），
  §4 的三个概念定义、§5 的四个陷阱，为领域通用知识。
- **判断部分**：§2 的记录格式、§5 的陷阱排序、§6 的意义陈述，**均为判断**。
- **未核实**：
  - **S1–S5 一篇正文都没读**，只看到标题；
  - **F1–F3 完全未核实**，据记忆列出，作者/卷期/年份可能有误；
  - 本方向的公开文献是否真的稀疏，未做检索量统计。
- **禁止**：本文件**不得**作为 related work 使用。它是待填的表格。
