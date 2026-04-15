# W2 详细执行计划：ONNX 导出与推理（cursor）

> **周期**：2026年4月7日（周二）— 4月13日（周一）  
> **承接前提**：已完成 `W1`（Python/Numpy/PyTorch 基础 + ResNet50 推理）  
> **核心目标**：跑通 `PyTorch -> ONNX -> ONNX Runtime` 最小闭环，并形成可展示的工程产物  
> **本周固定产出**：  
> - 1 个 ONNX 导出脚本  
> - 1 个 ONNX Runtime 推理脚本  
> - 1 份 PyTorch vs ONNX Runtime 时延对比  
> - 1 篇周总结/博客草稿（可发布）

---

## 本周执行总原则

1. 每天必须有**代码输出**或**可验证记录**，禁止“只看不练”。  
2. 每天学习资源按“**官方文档优先 + 视频辅助理解 + GitHub示例落地**”执行。  
3. 只追求“闭环跑通 + 结果可解释”，不追求一次性最优。  
4. 每天结束都做一次 5 分钟复盘：今天完成了什么、哪里卡住、明天如何降阻。

---

## Day 1（周二 4/7）：ONNX 基础认知与环境检查

### 今日目标

- 建立三者关系：`PyTorch（开发） -> ONNX（交换格式） -> ONNX Runtime（执行）`
- 确认本周环境可用，避免后续连续中断

### 时间安排

- **07:00-08:00（理论）**：理解 ONNX 的角色与价值  
- **21:00-22:00（实操）**：检查 Python 环境与依赖版本

### 今日任务

1. 阅读 ONNX 官方介绍，明确 ONNX 不是训练框架。  
2. 阅读 ONNX Runtime Python API 概览，知道后续用 `InferenceSession`。  
3. 终端检查环境：

```bash
conda activate ondevice-ai
python3 --version
python3 -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)"
```

### 高反馈学习资源（今日必看）

- **官方文档**：  
  - ONNX Intro: https://onnx.ai/onnx/intro/  
  - ONNX Runtime Python API: https://onnxruntime.ai/docs/api/python/api_summary.html  
- **视频（理解向）**：  
  - ONNX 官方 - ONNX 101（YouTube，35min）  

### 今日完成标准

- 能用一句话解释 ONNX 的作用  
- 环境检查通过并记录在 `week2/notes/notes_week2.md`

---

## Day 2（周三 4/8）：导出第一个 ONNX 模型

### 今日目标

- 使用 `torch.onnx.export()` 导出 `resnet50.onnx`
- 理解 `opset_version`、`dynamic_axes` 的最小必要含义

### 时间安排

- **07:00-08:00（理论）**：读导出参数  
- **21:00-22:00（实操）**：完成导出脚本并运行

### 今日任务

1. 新建 `week2/day1_onnx_export.py`。  
2. 导出 `week2/models/resnet50.onnx`。  
3. 记录模型大小与导出日志（是否 warning）。

### 高反馈学习资源（今日必看）

- **官方文档**：  
  - `torch.onnx.export` 文档: https://pytorch.org/docs/stable/onnx.html  
  - ONNX Operator 文档: https://onnx.ai/onnx/operators/  
- **视频（操作向）**：  
  - PyTorch 官方 - 模型导出（YouTube，25min）  
- **GitHub 示例**：  
  - ONNX Tutorials: https://github.com/onnx/tutorials/tree/main/tutorials

### 今日完成标准

- 成功生成 `.onnx` 文件  
- 记录：`opset=17`、输入 shape、是否启用 dynamic_axes

---

## Day 3（周四 4/9）：Netron 可视化与图结构认知

### 今日目标

- 用 Netron 看懂 ONNX 输入/输出、主干结构
- 建立“计算图”视角，而非“脚本”视角

### 时间安排

- **07:00-08:00（工具学习）**：掌握 Netron 基础  
- **21:00-22:00（观察记录）**：输出观察清单

### 今日任务

1. 打开 `resnet50.onnx`（Netron）。  
2. 记录：输入名/shape、输出名/shape。  
3. 识别主干：卷积、残差块、全连接。  
4. 把观察记录写进 `week2/notes/notes_week2.md`。

### 高反馈学习资源（今日必看）

- **工具**：  
  - Netron: https://netron.app  
- **视频（快速上手）**：  
  - Netron - 模型可视化工具（YouTube，15min）  
- **补充阅读**：  
  - ONNX Runtime 推理示例仓库（提前熟悉结构）  
    https://github.com/microsoft/onnxruntime-inference-examples/tree/main/python

### 今日完成标准

- 能明确说出模型输入输出名称与 shape  
- 形成“模型图可读”能力的第一版记录

---

## Day 4（周五 4/10）：ONNX Runtime Python 推理跑通

### 今日目标

- 脱离 PyTorch，直接用 ONNX Runtime 跑推理
- 输出 Top-5 并记录推理时延

### 时间安排

- **07:00-08:00（理论）**：理解 `InferenceSession` / `session.run()`  
- **21:00-22:00（实操）**：跑通脚本与结果校验

### 今日任务

1. 安装依赖：`onnx onnxruntime numpy pillow`。  
2. 新建 `week2/day4_onnxruntime_infer.py`。  
3. 输入复用 W1 前处理口径，确保可比。  
4. 输出 Top-5 与推理耗时。

### 高反馈学习资源（今日必看）

- **官方文档**：  
  - ONNX Runtime Python API: https://onnxruntime.ai/docs/api/python/api_summary.html  
- **视频（实战向）**：  
  - ONNX Runtime - 推理实战（YouTube，40min）  
- **GitHub 示例（对照代码）**：  
  - https://github.com/microsoft/onnxruntime-inference-examples/tree/main/python

### 今日完成标准

- 推理成功，输出 Top-5  
- 有可记录时延（ms）  
- 与 W1 结果大致一致

---

## Day 5（周六 4/11）：ONNX 图优化入门（onnx-simplifier）

### 今日目标

- 体验一次模型图简化流程
- 能解释“为什么优化前后要对比”

### 时间安排

- **09:00-12:00（实操）**：执行简化命令、生成简化模型  
- **15:00-17:00（对比）**：对比模型大小/节点/推理时延  
- **19:00-21:00（复盘）**：记录结论与下一步

### 今日任务

1. 安装并执行：

```bash
pip install onnxsim
python3 -m onnxsim week2/models/resnet50.onnx week2/models/resnet50_simplified.onnx
```

2. Netron 对比原始模型与简化模型。  
3. 用 Day4 脚本分别跑两份模型，记录延迟差异。

### 高反馈学习资源（今日必看）

- **工具文档**：  
  - onnx-simplifier: https://github.com/daquexian/onnx-simplifier  
- **补充文档**：  
  - ONNX Runtime 量化/优化入口（先建立地图）  
    https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html  
- **视频（理解优化）**：  
  - ONNX 图优化原理（YouTube，30min）

### 今日完成标准

- 有 `resnet50_simplified.onnx` 产物  
- 有“优化前后对比表”（至少：大小、延迟、结果一致性）

---

## Day 6（周日 4/12）：端到端闭环脚本与周产出封装

### 今日目标

- 一键跑通：加载 PyTorch -> 导出 ONNX -> ORT 推理 -> Top-5 输出
- 形成可展示的 `week2/README.md`

### 时间安排

- **09:00-12:00（编码）**：完成 `day6_end2end_pipeline.py`  
- **15:00-17:00（数据）**：整理性能对比数据表  
- **19:00-21:00（文档）**：完善 README 与笔记

### 今日任务

1. 编写端到端脚本（可复用此前脚本合并）。  
2. 写 `week2/README.md`，包含：目标、流程图（文字版）、时延表、结论。  
3. 截图或保存关键输出，便于后续面试展示。

### 高反馈学习资源（今日必看）

- **GitHub 示例**：  
  - ONNX Runtime 示例总仓：  
    https://github.com/microsoft/onnxruntime-inference-examples  
- **博客参考（表达结构）**：  
  - ONNX vs TorchScript（PyTorch Blog）  
    https://pytorch.org/blog/onnx/

### 今日完成标准

- 端到端脚本可重复执行  
- README 中含有“可量化结果”

---

## Day 7（周一 4/13）：复盘与输出（博客/面试话术）

### 今日目标

- 将本周学习转成“可传播、可复述、可面试”的表达

### 时间安排

- **07:00-08:00（写作）**：完成博客草稿  
- **21:00-22:00（收尾）**：仓库结构整理 + 最终自检

### 今日任务

1. 输出博客草稿（600-900 字即可）。  
2. 整理 `week2` 目录结构，保证他人可读。  
3. 形成 30 秒面试话术（建议背熟）：

> 我已完成 PyTorch 模型导出 ONNX、Netron 可视化检查、ONNX Runtime 独立推理与性能对比，具备端侧模型交付第一阶段能力。

### 高反馈学习资源（今日必看）

- **博客素材池（从你的资源库筛选）**：  
  - PyTorch 模型导出 ONNX 完全指南（掘金）  
  - ONNX 运算图优化详解（知乎）  
  - Netron 可视化你的神经网络模型（Medium）

### 今日完成标准

- 博客草稿完成  
- 周总结完成  
- 可口述 W2 完整闭环

---

## W2 自检清单（完成打勾）

| 检查项 | 状态 |
|---|---|
| 我能解释 PyTorch / ONNX / ONNX Runtime 的关系 | [ ] |
| 我导出了可用的 `resnet50.onnx` | [ ] |
| 我看懂了输入输出 name/shape（Netron） | [ ] |
| 我用 ONNX Runtime 跑通了推理 | [ ] |
| 我有至少一次真实推理时延记录 | [ ] |
| 我做了优化前后对比（大小/速度/一致性） | [ ] |
| 我完成了端到端闭环脚本 | [ ] |
| 我完成了 W2 README + 笔记 + 博客草稿 | [ ] |

**及格线**：6 项及以上  
**优秀线**：8 项全完成

---

## 与总计划的衔接（W2 -> W3）

- W2 产物 `resnet50.onnx` 将直接进入 W3 的 C++ 推理。  
- 你在 W2 建立的输入输出与图结构认知，会显著降低 W3 的 JNI/NDK 接入难度。  
- W2 若顺利完成，W3 可直接进入“ONNX Runtime C++ API + CLI 推理工具”。

---

*生成时间：2026-04-09*  
*依据文档：`最终版_端侧AI工程师_3个月冲刺计划_v3.0_优化版.md`、`端侧AI工程师_每周学习资源库_v3.1.md`、`每周计划/W1/第一周详细计划_W1_Python_PyTorch基础.md`*
