# 贡献指南（CONTRIBUTING）

> **本项目希望做到：从未接触过科研的人，也能贡献第一份东西。**
>
> 若你符合这句话，请直接看 §1.3 —— 你不需要先读完所有文档。

---

## 1. 你可以贡献什么

### 1.1 不需要写代码的贡献

| 类型 | 具体做什么 | 价值 |
|---|---|---|
| **清室复现** | 在没有任何口头解释的情况下，只凭仓库文档跑通验证流程，记录你卡在哪 | **最高**——它检验项目能否脱离作者运行 |
| **报告文档缺口** | 你说"我不知道从哪开始"，本身就是数据 | 高 |
| **盲测** | 用带故障的副本，看你的流程能否发现被改坏的数 | 高 |
| **领域数据** | 你的实验/仿真数据，按 `Research_Objects/` 的格式整理 | 高 |
| **文献线索** | 一篇该被引用但我们没有的文献 | 中 |
| **指出措辞问题** | 某个结论说得过于肯定，或过于含糊 | 中 |

### 1.2 需要写代码的贡献

| 类型 | 位置 |
|---|---|
| 新的校验不变量 | `Models/CDFV-001/Ref-01B/verify_baseline.py` |
| 新的负例（应当被抓的故障） | `verify_negative_cases.py` |
| 新的对抗用例 | `Benchmarks/ANRI-RV-001/make_adversarial_cases.py` |
| 新的失效模式检查 | `scripts/validate_gate_selftest.py` |

### 1.3 如果你从未做过科研

**从这里开始，三步：**

1. 读 `README.md` 的 **"Where the project actually is"** 一节（不是开头那段愿景）
2. 跑 §2 的五条命令，确认都能通过
3. 做 `Experiment_Requests/CLEANROOM-Replication_Task.md` 里的事，
   把你的卡点写进 `REPLICATION_LOG.md`

**你卡住的地方，比任何代码贡献都有价值。** 因为作者看不到自己的盲区。

---

## 2. 本地跑通验证（五条命令）

需要 Python 3。不需要 GPU、不需要联网、不需要 API key。

```powershell
py -3 .\scripts\validate_research_object.py .\Research_Objects\RO-CDFV-001-Ref-01B.json --repo-root .
py -3 .\Models\CDFV-001\Ref-01B\verify_baseline.py
py -3 .\Models\CDFV-001\Ref-01B\verify_negative_cases.py
py -3 .\Benchmarks\ANRI-RV-001\run_adversarial_cases.py
py -3 .\scripts\check_report_mechanism.py
```

**五条都应以 exit 0 结束。** 若有一条失败，先看 `Reviews/ANRI_Failure_Mode_Report_v0.1.md`
——那里面记录了已知会怎么失败。

Linux/macOS 把 `py -3` 换成 `python3`。

---

## 3. 唯一的硬规则

> **不得为了让测试通过而修改科学结论。**

这条优先于其余一切。具体含义：

- ❌ 校验器报错 → 把断言改松
- ❌ 门禁不通过 → 删掉那条检查
- ❌ 结论是 `unresolved` → 改成 `Accepted` 让流程好看
- ✅ 结论错了 → 改结论，并记录**为什么改、依据是什么**
- ✅ 检查写错了 → 改检查，并记录**它原本错在哪、为什么会写错**

**本项目的核心资产是"诚实地记录了失效"，不是"看起来都通过"。**

顺带一提：作者自己在 2026-10-20 记录了 26 条自己的缺陷，
其中三条是"声称已修复但实际没修完"。**这不是丢人，这是本项目的价值所在。**

---

## 4. 修改已登记产物的流程

`Research_Objects/RO-CDFV-001-Ref-01B.json` 哈希登记了全部产物。
**改动任何登记文件后，必须重新生成，否则门禁会失败。**

```powershell
# 1. 先取对象自己记录的 provenance（不要用当前 HEAD）
$c = py -3 -c "import json;print(json.load(open('Research_Objects/RO-CDFV-001-Ref-01B.json',encoding='utf-8'))['provenance']['git_commit'])"
$u = py -3 -c "import json;print(json.load(open('Research_Objects/RO-CDFV-001-Ref-01B.json',encoding='utf-8'))['provenance']['created_utc'])"
$d = py -3 -c "import json;print(json.load(open('Research_Objects/RO-CDFV-001-Ref-01B.json',encoding='utf-8'))['review']['reviews'][0]['date'])"

# 2. 重新生成对象与清单
py -3 .\scripts\gen_research_object.py --git-commit $c --created-utc $u --review-date $d

# 3. 验证
py -3 .\scripts\validate_research_object.py .\Research_Objects\RO-CDFV-001-Ref-01B.json --repo-root .
```

**注意三个坑（都是真实踩过的）**：

1. **`--git-commit` 必须传对象自己记录的值**，不是 `git rev-parse HEAD`。
   传 HEAD 会让检查在每个后续提交上误报"过期"。
2. **新增文件要同时加入** `scripts/gen_research_object.py` 的产物清单，
   否则不会被登记。
3. **文件必须 LF 换行**。仓库用 `.gitattributes` 强制，但别用会自动改行的编辑器。

---

## 5. 冻结产物的三条纪律

| 纪律 | 为什么 |
|---|---|
| **只用 LF 换行** | 换行符差异会改变哈希 |
| **不写机器相关路径** | 冻结产物里出现 `C:\Users\...` 会使别人无法复现 |
| **不写时间戳** | 会使产出不可重现 |

**CI 的 `cold-start` job 专门在无 `.git` 的导出树里重跑一遍**，
就是为了抓"只在我的机器上成立"这类问题。

---

## 6. 不要做的事

1. ❌ **不要 `git reset --hard` 或强推**（`main` 有保护规则）
2. ❌ **不要删除历次记录**。触发器、结论、失效模式都允许**原地退役**，不允许删除
   （历史日报引用了它们）
3. ❌ **不要用 P002 的数据冒充 CDFV-001 的数据**。
   `P003` 明确规定过这一点
4. ❌ **不要在盲测副本里留答案**。`Blind_Copies/` 已在 `.gitignore` 中
5. ❌ **不要把未复核的结论说成已复核**。`independent_human_reviews = 0` 是事实

---

## 7. 提交前自检

- [ ] 五条命令全部 exit 0
- [ ] 若改了登记产物，已重新生成对象与清单
- [ ] 文件为 LF 换行
- [ ] 没有把结论改得比证据更肯定
- [ ] 若引入新的不确定性，已在文档里写明

---

## 8. 提问与讨论

**可以提问。** 但请注意：

- 若你正在做**清室复现**，任务书要求你**不要在交付前**向作者提问。
  交付之后随便问——**你当时卡住的位置就是交付物的一部分。**
- 其他情况直接开 issue。

---

## 9. 本项目不提供什么

诚实说明，避免误解：

- **不提供"帮你跑 AI"的服务**，也不为你的推理付费
  （原因见 `docs/ANRI_Sustainability.md` §3.2）
- **不保证研究结论正确**——它只保证**产物完整、可复现、检查项已列出**
- **不承诺永久维护**——单人项目无法承诺这一点

---

## 10. 许可

MIT。你可以商用、闭源、再分发，无需授权。
若你用它做出了东西，**告诉我们一声**（不是义务，但会让这个项目知道自己在被使用）。
