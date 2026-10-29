# 案例强度审计（2026-10-28）

> **对象**：`Models/CDFV-001/Ref-01B/verify_negative_cases.py`（18 个负例）
> ＋ `Benchmarks/ANRI-RV-001/adversarial/`（12 个对抗案例）
> **总计 30 个测试实例。**
>
> **目的**：给每个案例标注强度，并回答一个问题——
> **有没有任何一个测试，检验的是「判据本身不适用」？**

---

## 1. 分级定义

**分级来自错题闭环的「变式强度」（2026-10-28 讨论）。**

| 级别 | 名称 | 定义 | 判据 |
|---|---|---|---|
| **S0** | **值级** | 改一个数值，数据形状不变 | 方法仍适用，只是看到了一个错数 |
| **S1** | **结构级** | 列缺失／改名／单位错／单调性破坏 | 数据形式不对，方法仍适用 |
| **S2** | **前提级（对抗）** | **数据完整且物理上说得通，但判据的前提不成立** | **结果事先不知道** |

**关键区别：**

> **S0 与 S1 的期望结果是**写死的**（必须被拒或被接受）。**
> **S2 的期望结果**事先不知道**——它可能正确地放过，也可能错误地拒绝，二者都是发现。**

**按 `D-ANRI-002` 补充的 L/H 分档：S0、S1 全部是 **L 档**；只有 S2 是 **H 档**。**

---

## 2. 逐条分级：负例 18 个

| # | 案例 | 期望 | **强度** | 机制 |
|---|---|---|---|---|
| 1 | `header_uses_velocity_mps_alias` | PASS | **S1** | 列名别名（**防误报**） |
| 2 | `header_uses_undeclared_fuzzy_name` | FAIL | S1 | 未声明的模糊列名 |
| 3 | `abs_constraint_column_present` | PASS | **S1** | 约束列存在（**防误报**） |
| 4 | `only_abs_constraint_column` | FAIL | S1 | 只有约束列 |
| 5 | `duplicate_header` | FAIL | S1 | 重复列名 |
| 6 | `missing_column_buoyancy_N` | FAIL | S1 | 列缺失 |
| 7 | `missing_column_weight_N` | FAIL | S1 | 列缺失 |
| 8 | `missing_column_constraint_force_N` | FAIL | S1 | 列缺失 |
| 9 | `non_numeric_weight` | FAIL | S1 | 非数值 |
| 10 | `wrong_weight_reference` | FAIL | **S0** | 参考值改错 |
| 11 | `time_not_monotonic` | FAIL | S1 | 单调性破坏 |
| 12 | `position_not_monotonic` | FAIL | S1 | 单调性破坏 |
| 13 | `weight_in_millinewton` | FAIL | S1 | 单位错 |
| 14 | `buoyancy_in_kilonewton` | FAIL | S1 | 单位错 |
| 15 | `buoyancy_above_full_submergence` | FAIL | **S0** | 值超范围 |
| 16 | `buoyancy_negative` | FAIL | **S0** | 值为负 |
| 17 | `free_surface_nonzero` | FAIL | S1 | 判据要求为零 |
| 18 | **`accelerated_without_inertial_term`** | FAIL | **S1（最强）** | **模型方程缺项** |

---

## 3. 逐条分级：对抗案例 12 个

| # | 案例 | **强度** | **对应的负例（同一个机制）** |
|---|---|---|---|
| A01 | `wrong_weight` | **S0** | `wrong_weight_reference` |
| A02 | `broken_force_balance` | **S0** | 同上 |
| A03 | `wrong_weight_mid` | **S0** | 同上（只是幅度不同） |
| A04 | `broken_force_balance_high` | **S0** | 同上（只是幅度不同） |
| A05 | `time_not_monotonic` | S1 | `time_not_monotonic` |
| A06 | `position_not_monotonic` | S1 | `position_not_monotonic` |
| A07 | `missing_buoyancy_column` | S1 | `missing_column_buoyancy_N` |
| A08 | `missing_weight_column` | S1 | `missing_column_weight_N` |
| A09 | `buoyancy_out_of_range` | **S0** | `buoyancy_above_full_submergence` |
| A10 | `weight_wrong_unit_mN` | S1 | `weight_in_millinewton` |
| A11 | `buoyancy_wrong_unit_kN` | S1 | `buoyancy_in_kilonewton` |
| A12 | `free_surface_nonzero` | S1 | `free_surface_nonzero` |

---

## 4. 四条发现

### 发现 1：**S2（对抗级）案例数 = 0**

**30 个案例中，没有任何一个检验「判据本身不适用」。**

**全部 30 个的期望结果都是事先写死的。**

### 发现 2：★ **12 个「对抗案例」没有引入任何新机制**

**逐条比对：A01–A12 每一个都对应一个已存在的负例，机制相同。**

**它们的区别只在**实现层面**（文件级 vs 内存级），不在**检验内容**层面。**

> **所以：名义上 30 个测试，实际不同的检验机制约 **10 个**。**

### 发现 3：**只有 2 个防误报案例**

`header_uses_velocity_mps_alias` 与 `abs_constraint_column_present` 期望 PASS。

**这是好做法——但 16:2 的比例意味着：**

> **系统主要在证明「我能拒绝坏数据」，很少证明「我不会拒绝好数据」。**

**而在真实使用中，后者的代价更高**：误拒一份正确数据，会让人不再信任门禁。

### 发现 4：最强的一个是 `accelerated_without_inertial_term`

**它是 30 个里唯一触及「模型方程是否完整」的案例。**

**但它仍然是 S1**，因为它的期望结果是写死的（必须被拒）。

> **它检验的是「缺项会被发现」，不是「这个方程在这个区制下是否适用」。**

---

## 5. 一个 S2 案例应该长什么样

**S2 的定义特征是：**它的结果不是断言，是发现**。**

**所以 S2 案例不能写成 `expected_status="FAIL"`。它需要第三种形态：**

```python
# 期望结果未知。交付物是"系统做了什么"，不是"系统做对了"。
Case(
    "probe_free_surface_dynamic",   # 自由面在动态工况下是否真的受力为零
    ...,
    expected_status=None,           # ← 未指定
    observe=True,                   # ← 只记录，不判定
)
```

### 三个候选（都可算、都不改代码）

| # | 探针 | 前提是什么 | 为什么结果未知 |
|---|---|---|---|
| **P1** | 自由面力**有物理依据地**非零（表面张力、弯月面） | 「自由面对物体无作用力」 | 判据会拒绝，但数据可能没错——**这正是要发现的** |
| **P2** | 数据处在**附加质量不可忽略**的区制 | 「力平衡不含附加质量」 | 判据可能通过（恰好抵消）也可能拒绝——**未知** |
| **P3** | 数据满足力平衡，但**违反了某个未写出的假设**（如准静态） | 「过程是准静态的」 | **未写出的假设无法被检查**——这是最有价值的一类 |

**P3 是本项目真正的空白：**

> **判据检查的都是**写下来的**条件。**
> **而失败最常发生在**没写下来的**条件上。**

---

## 6. 结论

| 项 | 值 |
|---|---|
| 测试实例总数 | **30** |
| 其中 S0（值级） | **8** |
| 其中 S1（结构级） | **22** |
| **其中 S2（前提级）** | **0** |
| **不同的检验机制** | **约 10** |
| **防误报案例** | **2** |
| **H 档测试** | **0** |

> **所以「30 个测试」这个数字应当被读作：**
> **「10 个机制 × 以 30 种方式重复，全部为轻档。」**

**这与 `loops_closed = L(2) + H(0)` 是同一个形状——两处都是重档为零，而且原因相同。**

---

## 7. 方法论声明

- **事实部分**：30 个案例的名称、期望状态、所触发的失败项，
  为 2026-10-28 通过导入 `verify_negative_cases.build_cases()` 与列举
  `adversarial/` 目录**实测获得**，非转述。S0/S1/S2 的归类为判断。
- **判断部分**：**分级定义、逐条归类、四条发现、S2 探针设计，均为判断。**
- **未核实**：约 10 个"不同机制"的口径（按机制名归并，**归并规则本身是判断**）；
  A01–A12 与负例的对应关系（按名称比对，**未逐行读实现**）。
- **本文件不修改任何测试。** 它只记录现状，并提出 S2 的方向。
