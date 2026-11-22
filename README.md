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
