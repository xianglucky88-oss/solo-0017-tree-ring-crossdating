# 木芯年轮定年工作台

原生 HTML、CSS 和 JavaScript 工作台，业务计算由 Python 完成，使用本机 SQLite 持久化。无需安装前端依赖。仅用于本地合成样本，不对公网开放。

```sh
python3 -B -m workbench
```

浏览器打开命令输出的地址（默认 `http://127.0.0.1:8817`）。工作台支持样例与文件导入、发布历史、指定版本加工、对比、复算和证据导出。可用 `--port`、`--db` 指定本机端口和数据库文件。

新增领域加工：逐芯留出复核、无共识年份、逐年票源证据。流程验收：`python3 -B examples/workbench_check.py`。

### 木芯关联定年

在工作台运行 `relative-dating`。用通过实测的相对起年关系和各芯候选交集确定组件绝对年份，不以局部并列直接任取起年。演练：`python3 -B examples/workbench_check.py relative-dating`。

### 定年木芯年度清单

在工作台运行 `calendar-inventory`。按联合定年的正式起年抽取该年度的实测槽位，量测与空槽保持原索引。演练：`python3 -B examples/workbench_check.py calendar-inventory`。

### 按树年度汇总

在工作台运行 `tree-chronology`。在明确定年的实测木芯中按母树聚合，再按不同母树计算年度支持和等权均值。演练：`python3 -B examples/workbench_check.py tree-chronology`。

### 成品复核与交接

运行 `independent-check` 后在结果中打开「查看复核交接」。合格成品可通过复核后签发；不合格成品可退回且保留原判定。发布新修订或恢复旧修订都会换代，已经通过但未签发的旧复核不能补签。已签凭据可从同一运行的历史复核中下载。

旧版工作台数据库打开时会在事务中自动升级到 SQLite 结构 v2，不改写原始录入、历史运行或证据。升级后的数据库不再由旧版工作台打开；保留旧版时请使用数据库的独立副本。

兼容保留原 HTTP 服务和数据格式，以下是原服务说明。

---

# 木芯年轮交叉定年

年轮样本整理员输入有年份的参考木芯宽度，建立逐年升降参考表，再评估未定年木芯的起年。只演示基于相邻变化投票的简化合成方法，不宣称科研定年准确性。

## 运行

Python 3.11 或以上，仅标准库。切换到此仓库目录。

```sh
python3 -B -m tree.http_api --port 8744
curl --json @examples/demo.json http://127.0.0.1:8744/chronology/dated-widths
```

不常驻启动也可运行以下演示；每次使用临时本机端口，结束后释放。

```sh
python3 -B -m tree.example /chronology/reference-votes
python3 -B -m tree.example /chronology/candidate-offsets
python3 -B -m tree.example /chronology/dated-widths
```

参见 [领域规则与接口](PROJECT_SPEC.md)。`examples/demo.json` 为完整合成输入；其他示例用于观察拒收或待核。业务单元测试留待后续，当前不假设联网、数据库或已有用户数据。

### 独立复测定年复核

发布更新后的 `examples/workbench.json`，在结果区选择「独立复测定年复核」。验收命令：`python3 -B examples/workbench_check.py independent-check`。这项加工可选；老原料不含 `witness_reading` 时仍可使用原操作。
