# P002 数据可得性核实（针对候选 B 与 C）

> **本文档回答一个具体问题**：`P002_WaterAir_Transition_Dynamics_2022.pdf` 里，
> 是否存在可用于候选 B（出水/入水冲击）与候选 C（流分离）的**定量数据**？
>
> - 日期：2026-10-19
> - 上游：`Research_Planning/P004_Candidate_Comparison.md` §6 明确标注
>   "未逐一打开 PDF 核实"——本文档补上这一步
> - 方法：`pdfplumber` 提取全文（15 页、48736 字符），关键词定位 + 图像清单
> - 结论：**B 不可行（数据不存在）；C 半可行（只有定性描述 + 可数字化的照片）**

---

## 1. 核实方法（可复现）

```powershell
# 库装在隔离目录，不污染系统 Python
python -m pip install --target $env:TEMP\pdflibs pdfplumber pypdf
$env:PYTHONPATH = "$env:TEMP\pdflibs"
# 提取全文并对关键词做上下文定位
```

- 页数：**15**（与 `Paper_Notes/P002_Free_Surface_Hydrodynamics_HAUV_2022.md` 的记录一致）
- 全文：**48,736 字符**
- 图像：见 §4

---

## 2. 候选 B（冲击 / water impact）—— **不可行**

### 2.1 关键词命中

| 词 | 命中次数 |
|---|---:|
| `impact` | 6 |
| `slamming` | **0** |
| `entry force` | **0** |
| `water entry` | 6 |
| `peak force` | **0** |

### 2.2 命中的 `impact` 全部不是冲击载荷

逐条核对 6 处 `impact` 的上下文，**没有一处报告冲击力峰值**：

| # | 实际含义 |
|---|---|
| 1 | `less than 0.5 m/s ... has an impact on the hydrodynamic forces` — 泛指"有影响" |
| 2 | `serious impact on HAUV` — 泛指 |
| 3 | `reducing the impact of platform vibration` — **平台减振**，不是水动力冲击 |
| 4 | `other hydrodynamic moment would have a greater impact on the resultant moment` — 泛指 |
| 5–6 | **参考文献标题**（Huang et al. 2018 关于弹体入水空腔；Dong et al. 2019 关于楔形体入水） |

### 2.3 论文明确说"入水"不是主要对象

原文（`water entry` 命中 1–4）：

> "The results of water entry experiments are shown in Fig. 13. In practical application,
> the water entry process of HAUV can be adjusted to a **relatively low speed
> (less than 0.5 m/s)** ... Therefore, the water entry process is relatively **less
> challenging** than that of the water exit process."

> "At low speed (less than 0.5 m/s), the water entry and exit processes of cylindrical
> HAUV can be approximately **simplified into opposite processes**."

**判断**：论文的入水实验只有 Fig. 13 一组，且其自身结论是"低速下入水可与出水
视为相反过程"——即**论文否认入水提供了独立的新信息**。
因此候选 B 在 P002 中没有数据基础，且论文的立场与该候选的前提相反。

### 2.4 全文没有力峰值表

| 搜索 | 命中 |
|---|---:|
| `maximum force` | **0** |
| `max(imum) value` | 3（全部指**吸入力**的最大值 ≈10% 重力） |
| `magnitude of` | **0** |

**结论：B 不可行。** 若要做 B，必须重新实验，而不是"从 P002 取数"。

---

## 3. 候选 C（流分离）—— **半可行，但只有定性**

### 3.1 关键词命中

| 词 | 命中次数 | 说明 |
|---|---:|---|
| `separat` | 4 | 见下 |
| `cavity` | **1** | **仅出现在参考文献标题里** |
| `cavitation` | **0** | — |
| `ventilat` | **0** | — |
| `air pocket` | **0** | 与 P003 的"空腔体积亏缺"假说最相关的词，**零命中** |
| `free surface` | 49 | 但多为一般性讨论 |

### 3.2 四处 `separat` 的实际含义

| # | 上下文 | 是否有量化 |
|---|---|---|
| 1 | `Stewart et al. (2020) tested the water-air trans-media motion ... separately` | 否（文献综述用词） |
| 2 | `(4) separation from the free surface (air stage)` | 否（**阶段定义**） |
| 3 | 自由液面与圆柱**完全分离**后，上部水被推向**尖峰状态**、形成**尖峰层**、水锥在重力下运动 | **定性描述，无参数** |
| 4 | `other hydrodynamic forces ... varying ranges will be different` | 否（泛论） |

**关键**：只有第 3 处是本研究自己的结果，且是**纯定性**的——
描述了"水锥/尖峰层"的形貌，**没有给出分离角、分离位置、空腔长度、临界速度**。

### 3.3 与 P003 假说的关系（重要）

P003 §7.5.4 提出的**空腔体积亏缺假说**，其关键概念是"气腔使实际排水体积低于
静水线暗示值"。本次核实发现：

- `cavity` 在 P002 全文**只出现 1 次，且在参考文献里**
- `air pocket` **零命中**

**判断**：P002 **没有研究气腔**。它研究的是**吸入力**（suction）
与**自由液面形貌**。因此：

> P003 的 H4（空腔体积亏缺）假说**不是 P002 内容的延伸**，
> 而是我们**自己提出的新机制**。P002 不提供任何支持或反驳它的数据。

这个发现**加强了 P003 §7.5.5 的谨慎表述**（"本假说由本文件提出，尚无反演证据"），
同时说明**候选 C 无法"从 P002 取数"来检验该假说**——要做 C 必须自己产生数据。

---

## 4. 图像可得性（决定"数字化"这条路是否成立）

`pdfplumber` 报告的嵌入图像：

| 页 | 图像数 | 尺寸 |
|---|---:|---|
| 7 | 1 | 1730×2722 |
| 8 | 1 | 1732×2722 |
| 9 | 2 | 1032×771, 1421×850 |
| 10 | 2 | 1033×777, 1836×1816 |
| 11 | 3 | 1032×697, 1032×698, 1422×943 |
| 12 | 1 | 1762×2722 |
| 13 | 3 | 1033×695, 1033×692, 1033×651 |

**`Fig. 9`（不同速度下自由液面变化）与 `Fig. 10`（水下视角）位于第 9–10 页**，
图像约 **1030×700 到 1400×850**——分辨率足以做**定性判别**（是否出现分离、
分离位置大致在哪），但**不足以做定量数字化**（无法可靠读出空腔长度等）。

**`Fig. 11`/`Fig. 12`（力曲线与吸入力拟合）图像约 1030×700**——
`Paper_Notes` 已记录它们"可读取但受绘图与测量约定限制"。

---

## 5. 对三个候选的修正评级

| 候选 | 原评级（未核实） | **核实后** | 依据 |
|---|---|---|---|
| **A 附加质量** | 无风险 | ✅ **仍然是唯一零外部依赖** | 不依赖 P002 数据，只需几何与已发表物理 |
| **B 冲击** | 中风险（需数据） | ❌ **不可行** | P002 无冲击力峰值；论文自认入水=出水的反向过程 |
| **C 流分离** | 高风险（可能需图像） | ⚠️ **只有定性** | 分离仅有形貌描述；气腔零命中；照片分辨率仅够定性 |

### 结论

> **B 应当从候选中删除**——不是"风险高"，而是**它的数据基础不存在**。
>
> **C 保留但降级**：它无法检验 P003 的 H4 假说（P002 没有气腔数据），
> 只能重新产生数据。
>
> **A 成为唯一"用现有材料就能闭环"的候选。**

---

## 6. 本文档的边界

- **事实部分**：关键词计数、上下文引文、图像尺寸，全部由 `pdfplumber` 从 PDF
  直接提取，可复现。引文已标注是否为参考文献标题。
- **判断部分**：§5 的评级、以及"分辨率足以定性、不足以定量"这一评估，
  **是判断**。我未实际打开图像目视确认内容——只读了尺寸与所在页。
- **未做**：未尝试实际数字化任何曲线；未核对 `Paper_Notes` 与 PDF 全文是否
  完全一致（只抽查了 suction ≈10% 重力这一处，一致）。
- **一个可能的偏差**：`pdfplumber` 的文本提取可能漏掉图内文字（如坐标轴标签）。
  若要做严格的数字化评估，需要**目视查看第 9–10 页的图像**。
