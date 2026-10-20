# Ref-01B 校验器的覆盖矩阵：哪些错误对门禁不可见

> **本文档回答一个负例套件答不了的问题**：
> "是否存在一种错误，能通过全部门禁？"
>
> - 日期：2026-10-20
> - 工具：`Benchmarks/ANRI-RV-001/coverage_probe.py`
> - 方法：逐列扰动干净基线，记录校验器是否检出
> - 结果：**26 次扰动中 13 次未被检出**

---

## 1. 为什么负例套件答不了这个问题

18 例负例 + 12 例对抗用例测的是"**已知故障是否被抓**"。
它们的覆盖面由"有人想到的故障类型"决定，因此**无法发现没人想到的盲区**。

本探针反转问题：**遍历每一列**，看校验器是否约束它。
一列如果能被随意改动而门禁不变色，那它就是盲区。

---

## 2. 方法与自检

```
对每一列 c，两种扰动：
  row : 仅中间一行加 step
  all : 每一行都加 step

step = delta × max|该列|      （加性，按列自身量级缩放）
```

**先跑对照组**：未修改的文件必须 PASS，否则度量无效。
对照组结果：`exit=0 failed=[]` ✅

### 探针自身的两个错误（已修正并记录）

**错误一：用乘法扰动**

初版用 `值 × (1 + delta)`。但基线里有两列**恒为 0**：

| 列 | 基线取值 |
|---|---|
| `acceleration_m_s2` | 全部 0.0 |
| `free_surface_force_N` | 全部 0.0 |

`0 × 1.01 = 0`——**扰动等于没做**，探针因此报告了两个不存在的盲区。

**错误二：中点的值可能接近 0**

`z_center_m` 在时间中点**穿越 0**（`-0.75L → +0.75L`）。
对中点那一行做 1% 乘法扰动，同样是 `≈0 × 1.01 ≈ 0`。

**这就是为什么改为按列最大值缩放的加性扰动**：

```python
scale = max(abs(v) for v in values)
step  = delta * scale
new   = old + step
```

**教训**：一个测量覆盖率的工具，本身必须先被检验。
若不做对照组、不检查"扰动是否真的改变了值"，它会输出一张**看起来很有说服力但错误**的矩阵。

---

## 3. 覆盖矩阵（`delta = 1%`）

图例：`YES` = 校验器抓到；`NO` = 未抓到。

| 列 | row | all | 抓它的 check |
|---|:---:|:---:|---|
| `time_s` | YES | **NO** | `monotonic_time`（仅 row） |
| `z_center_m` | YES | **NO** | `monotonic_position`（仅 row） |
| `velocity_m_s` | YES | **NO** | `monotonic_speed`（仅 row） |
| `acceleration_m_s2` | YES | YES | `force_balance` |
| `submerged_length_m` | **NO** | **NO** | *无* |
| `immersion_fraction` | **NO** | **NO** | *无* |
| `submerged_volume_m3` | **NO** | **NO** | *无* |
| `buoyancy_N` | YES | YES | `force_balance` / `buoyancy_range` / `buoyancy_unit_sanity` |
| `weight_N` | YES | YES | `force_balance` / `weight_reference` / `weight_unit_sanity` |
| `net_hydrostatic_force_N` | **NO** | **NO** | *无* |
| `free_surface_force_N` | YES | YES | `free_surface_zero` |
| `constraint_force_N` | YES | YES | `force_balance` |
| `constraint_force_abs_N` | **NO** | **NO** | *无* |

**未检出：13 / 26。**

---

## 4. 三个真实盲区

> **⚠️ 2026-10-20 更正**：本节初版断言"几何 → 浮力的链条完全未校验，
> 门禁会为一个算错的物理结果背书"。**该断言错误**，已由实测推翻。
> 更正过程见 §4.0。

### 4.0 更正：核心物理列其实被钉得很死

我原以为可以构造一个"内部自洽但物理错误"的结果通过门禁。
实测（`--consistent`）显示**不行**：

| 体积与浮力同乘因子 | 约束力 | 结果 | 抓它的 check |
|---:|---|---|---|
| 1.10 | 原值 | **caught** | `buoyancy_range` / `buoyancy_unit_sanity` / `force_balance` |
| 1.10 | 重算 | **caught** | `buoyancy_range` / `buoyancy_unit_sanity` |
| 1.001（+0.1%） | 原值 | **caught** | 同上 |
| 1.001 | 重算 | **caught** | 同上 |
| **1.000001（+1e-6）** | 任意 | **PASSES** ← 唯一逃过的 |
| 0.999（−0.1%） | 任意 | **caught** | `buoyancy_unit_sanity` |
| 0.99 | 任意 | **caught** | `buoyancy_unit_sanity` |

**原因**：`buoyancy_unit_sanity` 把 `max(buoyancy)` 钉死在常数
`FULL_BUOYANCY_N` 上，相对容差 `UNIT_SANITY_REL_TOL = 1e-6`。
所以任何**系统性缩放**（放大或缩小）都会被抓住，无论约束力是否跟着改。

**检出阈值 ≈ 1e-5 相对**（1e-6 逃过，1e-3 被抓）。
**这比我先前的判断严格得多。**

**因此：「一个生成器 bug 会产出完全验证通过的错误结果」这一说法不成立**
——只要该 bug 使 `max(buoyancy)` 偏离 `πR²L·ρg` 超过约 1e-5。

### 4.1 真正未被校验的是**派生列**

探针显示下列列可被任意改动而门禁不变色：

| 列 | 有检查吗 | 谁读它 |
|---|---|---|
| `submerged_length_m` | ❌ 无 | 无 |
| `immersion_fraction` | ❌ 无 | 无 |
| `submerged_volume_m3` | ❌ 无 | 无 |
| `net_hydrostatic_force_N` | ❌ 无 | 无 |
| `constraint_force_abs_N` | ❌ 无 | 无 |

**这批列的共同点：它们是冗余/派生量，没有任何检查读取它们，
也没有任何检查验证"派生量 = 由其它列算出的值"。**

**例如**：

```
net_hydrostatic_force_N  ≠  buoyancy_N − weight_N    （无检查）
constraint_force_abs_N   ≠  |constraint_force_N|      （无检查）
submerged_volume_m3      ≠  A_cross · submerged_length_m （无检查）
```

**实际风险（判断）**：
- 核心物理（浮力、重量、约束力、平衡）**被校验**；
- 但一个读者若直接引用 `submerged_volume_m3` 或 `net_hydrostatic_force_N`，
  他拿到的是一个**没有任何门禁背书的数字**，且**无从得知这一点**。

这比"门禁为错误物理背书"轻得多，但仍是一个真实的边界。

### 4.2 恒定偏移在运动学列上不可见

`time_s`、`z_center_m`、`velocity_m_s` 的 `all` 扰动**未被检出**，
因为**给每行加同一个常数不破坏单调性**。

**含义**：系统性的时间零点偏移、或位置/速度的常数偏差**逃过门禁**。
这在实验数据处理中很常见（零点标定、传感器偏置）。

门禁检查的是**单调性（形状）**，不是**数值（标定）**。
这一条**未被任何后续测试推翻**。

### 4.3 派生列的补充说明

见 4.1。特别地：

- `net_hydrostatic_force_N` 与 `constraint_force_abs_N` 都可由其它列算出，
  但**没有检查断言这一点**；
- 这不是"物理被算错"的风险，而是"**冗余列可能与主列不一致而无人发现**"的风险。

---

## 5. 检出阈值（量级扫描）

### 5.1 单列扰动

| `delta` | `buoyancy_N` | `weight_N` | `constraint_force_N` |
|---:|:---:|:---:|:---:|
| 1e-2（1%） | YES | YES | YES |
| 1e-4（0.01%） | YES | YES | YES |
| **1e-6** | **NO** | **NO** | **NO** |

### 5.2 自洽缩放（体积+浮力同乘）

| 因子 | 相对偏差 | 结果 |
|---:|---:|---|
| 1.001 | 1e-3 | caught |
| 1.000001 | 1e-6 | **passes** |

**与声明一致**：`tolerance_n = 1e-4 N`、`UNIT_SANITY_REL_TOL = 1e-6`。
**实测落点与这两个常数吻合**，说明力的检查是"诚实"的：
它抓得住大于声明容差的一切扰动，且不假装抓得住更小的。

---

## 6. 这是设计缺陷还是可接受设计？

**更正后的评估：这不是"物理可能被算错"的风险，而是"未校验列可能被误用"的风险。**

### 被充分校验的部分

| 量 | 约束方式 | 严格程度 |
|---|---|---|
| 浮力量级 | `buoyancy_unit_sanity` 钉死 `max(buoyancy)` 于 `FULL_BUOYANCY_N` | **1e-6 相对** |
| 重量 | `weight_reference` 钉死 `WEIGHT_N` | 1e-4 N 绝对 |
| 力平衡 | `force_balance`（含 `m·a`） | 1e-4 N |
| 自由液面项 | `free_surface_zero` | 1e-4 N |
| 运动形状 | `monotonic_time/position/speed` | 严格单调 |
| 单位一致性 | `buoyancy_unit_sanity` / `weight_unit_sanity` | 1e-6 相对 |

**结论：核心物理链条实际上被钉得比我先前的评估更死。**

### 未被校验的部分

1. **冗余/派生列**（§4.1）：`submerged_volume_m3`、`submerged_length_m`、
   `immersion_fraction`、`net_hydrostatic_force_N`、`constraint_force_abs_N`；
2. **运动学绝对值**（§4.2）：只有单调性，没有标定。

### 判断

- **§4.1 类风险：可接受但应披露。** 这些列是冗余的，主物理由
  浮力/重量/约束力三列承担且被钉死。**但它们出现在产物里，
  读者无法从产物本身判断哪些列被校验过。**
- **§4.2 类风险：这是更实际的问题。** 工程数据最常见的错误是标定偏移，
  而这恰好落在盲区。`Ref-01S` 实验计划一旦产出真实数据，
  这类错误会直接影响结论。

---

## 7. 建议（按成本排序）

| # | 建议 | 成本 | 堵住 |
|---|---|---|---|
| 1 | 加 `derived_column_consistency`：断言 `net_hydrostatic = b − w`、`constraint_abs = |constraint|`、`volume = A · h_sub` | **低** | 4.1 |
| 2 | 在产物里**标注哪些列被校验**（或加一个 `verified_columns` 字段） | **低** | 表述风险 |
| 3 | 在 README 把"验证通过"限定为"通过了以下 N 项不变量" | **低** | 表述风险 |
| 4 | 对运动学列增加**绝对值**检查（需参考时间零点与标定） | 中 | 4.2 |

**本次未实施任何建议**——本文档只做测量。

**优先建议 1**：它是三条低价值列的一致性补丁，改动小、
且能防止"冗余列与主列悄悄不一致"。

---

## 8. 方法论声明

- **事实部分**：覆盖矩阵、阈值表、自洽缩放表、对照组结果，
  全部由 `coverage_probe.py` 实测产生，可复现：
  ```
  py -3 .\Benchmarks\ANRI-RV-001\coverage_probe.py --delta 0.01
  py -3 .\Benchmarks\ANRI-RV-001\coverage_probe.py --consistent
  ```
- **判断部分**：§4.1 的"读者无从得知"，§6 的取舍评估，§7 的成本估计，**均为判断**。
- **本报告初版的一处错误已被实测推翻**（§4.0）：
  原断言"内部自洽的错误物理能通过门禁"，实测证明**不能**——
  `buoyancy_unit_sanity` 在 1e-6 相对容差上钉死了浮力量级。
  **该更正保留在文档内，未删除原断言，以便读者看到判断如何被修正。**
- **探针自身的错误**：§2 记录了两个（乘法扰动对恒零列无效、
  中点乘法扰动对过零列无效），都曾产生**假盲区**。
- **探针仍有的局限**：
  - 只测了 `Ref-01B-B-0p25mps.csv`，未测另两个速度与 6 个加速度工况；
  - 只测"单列扰动"与"体积+浮力自洽缩放"，未穷举多列协同扰动；
  - `delta = 1%` 与 `--consistent` 的因子集合是选择，不是穷举。
