# P003 文献缺口：第一次实际检索的结果

> **本文档记录 2026-10-20 一次实际文献检索的发现。**
> 起因：`D-ANRI-008` §4 指出 P003 的全部证据基础只有 P002 一篇。
>
> **结论：那篇论文不是我们要的，但它的参考文献列表里有我们要的——包括一条指向哈工程自己。**

---

## 1. 找到的论文（已下载入库）

**Zhang Xing-yu, Lyu Xu-jian, Fan Xu-dong (2022)**
*Numerical Study on the Vertical Water Exit of A Cylinder with Cavity*
China Ocean Engineering, **36(5): 734–742**
doi:10.1007/s13344-022-0065-0
南京理工大学 能源与动力工程学院

存于 `Paper_Library/P003_Water_Exit_Cylinder_Cavity_2022.pdf`

### 1.1 它做了什么

- **CFD（VOF + 重叠网格）**，不是实验
- 对象：**高速圆柱**（30–70 m/s 量级）穿越水气界面的出水过程
- 主要结论：**出水时空泡溃灭会在圆柱上造成强烈压力脉动**；
  当圆柱被超空泡包裹出水时，壁面压力分布较均匀、阻力变化平缓，运动稳定性较好

### 1.2 ⚠️ 它与本项目不是同一个区制

| | 本项目（P002 基准） | Zhang 2022 |
|---|---|---|
| 速度 | **0.1–0.5 m/s** | **30–70 m/s** |
| `Fr_D` | **0.106 / 0.266 / 0.532** | 约 3–7（量级差 10 倍以上） |
| 流动 | 无空化、重力主导 | **超空泡区**、惯性主导 |
| 方法 | 实验 | 数值 |

**所以它不能直接回答 P003 的问题，但它证明了两件事**：
1. 这个方向有活跃的、正在发表的研究；
2. **它的引言与参考文献，是一份现成的必读清单。**

---

## 2. 从它的参考文献里筛出的必读项

> **以下条目均引自 Zhang 2022 的参考文献列表，我未读原文。**
> 筛选依据只有标题——**这是本条最重要的限制**。

### 2.1 ★ 最相关的四条（低速 / 浮力主导 / 密度效应）

| # | 文献 | 为什么最相关 |
|---|---|---|
| **1** | **Truscott, Epps, Munns (2016). *Water exit dynamics of buoyant spheres*. Physical Review Fluids 1(7), 074501** | **浮力主导的出水**——与本项目低速区制最接近 |
| **2** | **Takamure & Uchiyama (2020). *Effect of density of a sphere launched vertically in water on the water-surface behavior and sphere motion in air*. Physics of Fluids 32(11), 113313** | **直接研究密度影响**——正是 Stage 1 的第一条迁移条件 |
| **3** | **Hao et al. (2019). *Numerical analysis of water exit for a sphere with constant velocity using the lattice Boltzmann method*. Applied Ocean Research 84, 163–178** | **恒速出水**——B1 的工况形态 |
| **4** | **Korobkin (2013). *A linearized model of water exit*. Journal of Fluids and Structures** | **出水的理论模型**——若已有标准形式，本项目自定的自由液面项须对齐 |

### 2.2 ★★ 一条指向哈工程自己的

> **Chen, Y.X. (2012). *Research on Multiphase Hydrodynamics Problems of the Free Surface
> Penetration of Bodies*. Ph.D. Thesis, Harbin Engineering University, Harbin, 139. (in Chinese)**

**哈尔滨工程大学的博士论文，主题是"物体穿越自由液面的多相水动力学"。**

**这可能是今天最重要的发现**：
- 它说明**哈工程自己有人做过这个方向**；
- 一条博士论文意味着**一个课题组、一位导师**；
- **而今天下午你要选导师。**

**建议：立刻查这篇论文的导师是谁。** 这比问任何一位教授"有哪些经典文献"更直接——
因为答案就在本校。

### 2.3 其他可引用项

| 文献 | 类型 |
|---|---|
| Tassin, Piro, Korobkin, Maki, Cooker (2013). *Two-dimensional water entry and exit of a body whose shape varies in time*. JFS 40, 317–336 | 出入水理论 |
| Shi, Hu, Zhou (2014). *Experimental and theoretical analysis of water exit of a supercavity*. Acta Aerodynamica Sinica 32(4), 544–550 | 实验+理论 |
| Liu et al. (2014). *Experimental study on vertical water exit of an axisymmetric body under ventilated cavitation* | 实验 |
| Chen, K.X. (2015). *Measurement research of underwater vehicles of the out-of-water load*. Journal of Sichuan Ordnance 36(11) | **出水载荷测量** |
| Li, Lu, Fu (2007). *Numerical simulation on vertical water exit of axis-symmetric slender body* | 数值 |

---

## 3. 对本项目的三条含义

### 3.1 P003 的"空腔体积亏缺假说"（H4）可能不是新发现

本项目在 §7.5 独立推导出 H4：`F_suction ≈ ρ_w g ΔV_cav`。

**而 Zhang 2022 的核心结论是"空泡溃灭造成压力脉动"**——
机制相近。**必须读 Truscott (2016) 与 Korobkin (2013) 才能判断 H4 是否已被提出。**

**若已被提出**：P003 的贡献须从"提出机制"改为"在 G2 的第二个问题上验证该机制"。
**若未被提出**：H4 是真实的独立贡献，且有了文献对照。

### 3.2 基线的 `L-EXCLUDED-PHYSICS` 可能站不住

P003 的基线**排除了自由液面项**。而 Korobkin (2013) 提供的是**出水的线性化模型**。

**若文献中已有标准形式**，本项目自定一个（并排除掉）会被直接质疑。

### 3.3 今天的检索改变了"问教授什么"

原本打算问：**"有哪些必读文献？"**

**现在应该问得更具体**：

> "我查到 Chen Y.X. 2012 那篇哈工程的博士论文，
> 以及 Truscott 2016 和 Korobkin 2013。
> **这几篇里，哪几篇是必须读的？还有没有我漏掉的？**"

**问具体的人比问开放问题更容易得到有用的回答**，而且显示你已经做过工作。

---

## 4. 方法论声明

- **事实部分**：Zhang 2022 的标题、期刊、卷期页、DOI、摘要与结论，
  引自下载到的 PDF 正文；其参考文献条目**逐条抄自该 PDF 的 References 节**。
- **判断部分**：§2.1 的四条筛选、§3 的三条含义、§2.2 的"立刻查导师是谁"，
  **均为基于标题的判断，未读原文**。
- **明确未做**：**未阅读任何一篇被引文献的正文**；未核实这些文献是否真的
  涉及"低速垂直出水吸力"这一具体问题；未查 Chen Y.X. 2012 的导师。
- **使用限制**：§2 的清单**不得直接作为 related work 使用**。
  它是"该读什么"的候选表，不是"这些文献说了什么"的结论。
