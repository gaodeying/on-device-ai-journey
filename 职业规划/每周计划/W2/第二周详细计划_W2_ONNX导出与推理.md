# W2 详细执行计划：ONNX 导出与推理

> **生成说明**：本文档由 CatDesk AI 于 2026年4月9日 自动生成，基于《3个月冲刺计划 v3.0》及 W1 完成情况制定。
>
> **周期**：2026年4月7日（周二）— 4月13日（周一）
> **核心目标**：完成 `PyTorch → ONNX → 推理` 最小闭环跑通
> **本周产出**：
> - 完整的 Python 端到端推理脚本（PyTorch → ONNX → ONNX Runtime 推理 → Top5 结果）
> - 用 Netron 可视化 ONNX 模型，理解计算图结构
> - 第二篇技术博客：移动开发者第一份 ONNX 模型导出实战
> - GitHub commit 记录

---

## W1 → W2 衔接说明

上周你完成了：

- PyTorch 环境搭建，Tensor 基础操作
- Numpy 前处理流程（HWC → CHW，归一化）
- ResNet50 预训练模型加载 + 推理，记录了真实延迟数据

**本周要解决的核心问题**：上周的模型只能在 Python/PyTorch 环境里跑，Android C++ 怎么用？

答案分两步：

1. **本周（W2）**：把 PyTorch 模型导出成 ONNX 格式，用 Python 版 ONNX Runtime 验证推理结果一致
2. **下周（W3）**：用 C++ 版 ONNX Runtime API 加载 `.onnx` 文件，做命令行推理 Demo

---

## 开始前：快速预热（10分钟，一次性完成）

在正式开始 W2 之前，花 10 分钟建立"为什么需要 ONNX"的直觉认知。

**读这一页**：[ONNX 官网首页 - Why ONNX](https://onnx.ai/onnx/intro/)

核心理解：

- PyTorch 模型 = 只能在 PyTorch 环境里跑（Python + 大量依赖）
- ONNX = 一种"通用模型格式"，就像 PDF 之于文档，任何支持 ONNX 的运行时都能加载
- ONNX Runtime = 微软开源的高性能推理引擎，支持 Windows/Android/iOS/Linux，C++ API 完善

**移动端类比**：ONNX 就像 Android 的 APK 格式——你用 Java/Kotlin 写代码，打包成 APK 后，任何 Android 设备都能安装运行，不需要知道你用了什么 IDE。

---

## 第一天 · 4月7日（周二）：ONNX 概念理解

> **时间**：早7:00-8:00（理论），晚21:00-22:00（实操）
> **主题**：搞清楚 ONNX 是什么、为什么需要它、它的核心概念

### 早上 7:00-8:00：理论学习

**学习路径（按顺序，不要乱）**：

**第一步（20分钟）**：[ONNX 官方文档 - 概念介绍](https://onnx.ai/onnx/intro/concepts.html)

重点理解以下 4 个核心概念：

| 概念 | 类比（移动端视角） | 说明 |
|------|-----------------|------|
| **Graph（计算图）** | Activity 的生命周期流程图 | 描述模型的计算流程，节点是算子，边是数据流 |
| **Node（节点）** | 一个函数调用 | 代表一个算子（如 Conv、ReLU、MatMul） |
| **Tensor（张量）** | byte[] 数据 | 节点之间传递的数据，有 shape 和 dtype |
| **Opset（算子集版本）** | API Level | ONNX 算子的版本号，导出时需要指定，影响兼容性 |

**第二步（20分钟）**：[ONNX Runtime 官方文档 - Python 快速入门](https://onnxruntime.ai/docs/get-started/with-python.html)

重点看：ONNX Runtime 的 Session 概念（类比 Android 的 MediaPlayer：先 prepare，再 play），`InferenceSession` 的创建和推理调用方式，以及为什么 ONNX Runtime 比 PyTorch 推理更快（静态图 vs 动态图）。

**第三步（15分钟）**：思考并记录以下问题的答案（不用查，凭直觉写）：

1. 为什么 PyTorch 模型不能直接在 Android C++ 里加载？
2. ONNX 格式和 `.pt` 格式有什么本质区别？
3. 如果 ONNX 导出时指定了固定 batch size，在推理时能改变 batch size 吗？

（这三个问题的答案在今晚实操后会自然清晰）

### 晚上 21:00-22:00：安装依赖 + 验证环境

```bash
# 激活 W1 创建的虚拟环境
conda activate ondevice-ai

# 安装本周需要的依赖
pip install onnx onnxruntime onnx-simplifier netron

# 验证安装
python3 -c "
import onnx
import onnxruntime as ort
print(f'ONNX 版本: {onnx.__version__}')
print(f'ONNX Runtime 版本: {ort.__version__}')
print('OK 依赖安装成功')
"
```

写一个简单的验证脚本，确认 W1 的 ResNet50 模型还能正常加载：

```python
# week2/day1_env_check.py
import torch
import torchvision.models as models

print("验证 W1 环境...")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)
with torch.no_grad():
    output = model(dummy_input)

print(f"ResNet50 输出 shape: {output.shape}")  # [1, 1000]
print("OK W1 环境正常，可以开始 W2")
```

**今天的 GitHub commit**：

```bash
mkdir -p ~/on-device-ai-journey/week2
cd ~/on-device-ai-journey
echo "# Week2: ONNX 导出与推理" > week2/README.md
git add week2/
git commit -m "W2D1: ONNX 概念学习，依赖安装验证"
```

---

## 第二天 · 4月8日（周三）：ONNX 导出实战

> **时间**：早7:00-8:00（理论），晚21:00-22:00（实操）
> **主题**：把 W1 的 ResNet50 模型导出成 `.onnx` 文件
> **连贯性**：今天的导出结果，后面几天全部复用

### 早上 7:00-8:00：理论学习

**精读（30分钟）**：[PyTorch 官方 ONNX 导出文档](https://pytorch.org/docs/stable/onnx.html)

重点理解 `torch.onnx.export()` 的关键参数：

| 参数 | 作用 | 注意事项 |
|------|------|---------|
| `model` | 要导出的 PyTorch 模型 | 必须先 `model.eval()` |
| `args` | 示例输入（dummy input） | 决定了模型的输入 shape |
| `f` | 输出文件路径 | 通常命名为 `xxx.onnx` |
| `input_names` | 输入节点名称 | 自定义，方便后续调用 |
| `output_names` | 输出节点名称 | 自定义 |
| `dynamic_axes` | 动态维度配置 | **重点**：设置 batch size 为动态，否则只能推理固定 batch |
| `opset_version` | ONNX 算子集版本 | 推荐 17，兼容性好 |

**重点理解 `dynamic_axes`**（这是面试高频考点）：

```python
# 固定 batch（不推荐）：只能推理 batch=1
dynamic_axes = None

# 动态 batch（推荐）：可以推理任意 batch size
dynamic_axes = {
    'input': {0: 'batch_size'},    # 第0维（batch）是动态的
    'output': {0: 'batch_size'}
}
```

**思考（5分钟）**：为什么端侧推理通常 batch=1？（答案：手机上一次只处理一张图片，不需要批量推理）

### 晚上 21:00-22:00：导出实战

```python
# week2/day2_onnx_export.py
"""
把 W1 的 ResNet50 模型导出成 ONNX 格式
这是端侧部署的第一步！
"""
import torch
import torchvision.models as models
import onnx
import os

# Step 1: 加载 PyTorch 模型
print("Step 1: 加载 ResNet50...")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()  # 必须！导出前一定要切换到 eval 模式

# Step 2: 准备 dummy input
# ResNet50 标准输入：[batch, channel, height, width] = [1, 3, 224, 224]
dummy_input = torch.randn(1, 3, 224, 224)
print(f"Step 2: dummy_input shape: {dummy_input.shape}")

# Step 3: 导出 ONNX（固定 batch 版本）
os.makedirs("week2", exist_ok=True)
output_path_fixed = "week2/resnet50_fixed_batch.onnx"

torch.onnx.export(
    model, dummy_input, output_path_fixed,
    input_names=["input"], output_names=["output"],
    opset_version=17, verbose=False
)
print(f"  固定 batch 文件大小: {os.path.getsize(output_path_fixed) / 1e6:.1f} MB")

# Step 4: 导出 ONNX（动态 batch 版本，推荐）
output_path_dynamic = "week2/resnet50_dynamic_batch.onnx"

torch.onnx.export(
    model, dummy_input, output_path_dynamic,
    input_names=["input"], output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=17, verbose=False
)
print(f"  动态 batch 文件大小: {os.path.getsize(output_path_dynamic) / 1e6:.1f} MB")

# Step 5: 验证 ONNX 模型合法性
model_onnx = onnx.load(output_path_dynamic)
onnx.checker.check_model(model_onnx)
print("OK ONNX 模型验证通过！")
print(f"  - Opset 版本: {model_onnx.opset_import[0].version}")
print(f"  - 节点数量: {len(model_onnx.graph.node)}")

input_shape = model_onnx.graph.input[0].type.tensor_type.shape
dims = [d.dim_value if d.dim_value > 0 else d.dim_param for d in input_shape.dim]
print(f"  - 输入 shape: {dims}")  # ['batch_size', 3, 224, 224]
```

**今天的 GitHub commit**：

```bash
git add week2/day2_onnx_export.py
git commit -m "W2D2: ResNet50 ONNX 导出，含固定/动态 batch 两个版本"
```

---

## 第三天 · 4月9日（周四）：Netron 可视化

> **时间**：早7:00-8:00（理论），晚21:00-22:00（实操）
> **主题**：用 Netron 打开 `.onnx` 文件，理解计算图的节点/边/输入输出
> **为什么重要**：能看懂计算图，才能做图优化（W9 的核心技能）

### 早上 7:00-8:00：理论学习

**读（20分钟）**：[ONNX 算子规范文档](https://onnx.ai/onnx/operators/)

不需要全读，只需要找到以下几个算子，理解它们的输入/输出格式：

- `Conv`（卷积）：输入 `[N, C, H, W]`，权重 `[out_channels, in_channels, kH, kW]`
- `BatchNormalization`：训练和推理模式的区别（推理时 BN 可以和 Conv 融合！）
- `Relu`：逐元素激活，shape 不变
- `Gemm`（矩阵乘法）：全连接层的底层实现
- `Softmax`：分类输出的概率归一化

**读（15分钟）**：[Netron GitHub 使用说明](https://github.com/lutzroeder/netron)

重点了解：如何打开 `.onnx` 文件，如何点击节点查看属性（kernel_size、stride、padding 等），如何查看 Tensor 的 shape 信息。

**思考（10分钟）**：ResNet50 有 50 层，但 ONNX 图里的节点数量远不止 50 个，为什么？

（答案：每一层可能对应多个算子节点，比如一个 Conv 层 = Conv + BatchNorm + ReLU 三个节点）

### 晚上 21:00-22:00：Netron 实操 + 代码探索

**操作步骤**：

```bash
# 方式1：命令行启动 Netron（会自动打开浏览器）
python3 -m netron week2/resnet50_dynamic_batch.onnx

# 方式2：直接访问在线版（不需要安装）
# 打开 https://netron.app，拖入 .onnx 文件
```

**在 Netron 里完成以下探索任务**：

1. 找到第一个 Conv 节点，记录：kernel_shape（卷积核大小）、strides（步长）、pads（填充）
2. 找到 BatchNormalization 节点，观察它紧跟在 Conv 后面
3. 找到最后的 Gemm 节点（全连接层），确认输出维度是 1000
4. 观察整体图的形状：ResNet 的残差连接在图里是什么样的？

**用代码探索 ONNX 图结构**：

```python
# week2/day3_netron_explore.py
import onnx
from collections import Counter

model = onnx.load("week2/resnet50_dynamic_batch.onnx")
graph = model.graph

print(f"总节点数: {len(graph.node)}")
print(f"总参数张量数: {len(graph.initializer)}")

# 统计各类算子的数量
op_counts = Counter(node.op_type for node in graph.node)
print("\n算子类型统计（Top 10）：")
for op, count in op_counts.most_common(10):
    print(f"  {op:30s}: {count}")

# 打印前5个节点的详细信息
print("\n前5个节点：")
for i, node in enumerate(graph.node[:5]):
    print(f"\n  [{i}] {node.op_type}")
    print(f"    输入: {list(node.input)}")
    print(f"    输出: {list(node.output)}")
    for attr in node.attribute:
        if attr.type == 7:  # INTS
            print(f"    {attr.name}: {list(attr.ints)}")

# 查看模型输入输出的完整 shape 信息
print("\n模型输入：")
for inp in graph.input:
    shape = inp.type.tensor_type.shape
    dims = []
    for d in shape.dim:
        dims.append(d.dim_param if d.dim_param else d.dim_value)
    print(f"  {inp.name}: {dims}")

print("\n模型输出：")
for out in graph.output:
    shape = out.type.tensor_type.shape
    dims = []
    for d in shape.dim:
        dims.append(d.dim_param if d.dim_param else d.dim_value)
    print(f"  {out.name}: {dims}")

print("\nOK Day3 完成！")
```

**今天的 GitHub commit**：

```bash
git add week2/day3_netron_explore.py
git commit -m "W2D3: Netron 可视化 ONNX 计算图，代码探索节点结构"
```

---

## 第四天 · 4月10日（周五）：ONNX Runtime Python 推理

> **时间**：早7:00-8:00（理论），晚21:00-22:00（实操）
> **主题**：用 ONNX Runtime 跑推理，并与 PyTorch 输出做数值对比
> **关键验证**：ONNX 导出是否正确？两者输出是否一致？

### 早上 7:00-8:00：理论学习

**精读（30分钟）**：[ONNX Runtime Python API 文档](https://onnxruntime.ai/docs/api/python/api_summary.html)

重点掌握以下 API：

```python
import onnxruntime as ort

# 1. 创建推理 Session（类比 Android MediaPlayer.prepare()）
session = ort.InferenceSession("model.onnx")

# 2. 查看输入输出信息
input_name  = session.get_inputs()[0].name   # 输入节点名
output_name = session.get_outputs()[0].name  # 输出节点名
input_shape = session.get_inputs()[0].shape  # 输入 shape

# 3. 执行推理（输入必须是 numpy array，不是 Tensor！）
import numpy as np
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
outputs = session.run([output_name], {input_name: input_data})
result = outputs[0]  # numpy array，shape [1, 1000]
```

**理解 SessionOptions（性能调优入口）**：

```python
# 这是 W9 性能优化的预热知识
options = ort.SessionOptions()
options.intra_op_num_threads = 4          # 算子内并行线程数
options.graph_optimization_level = (
    ort.GraphOptimizationLevel.ORT_ENABLE_ALL  # 开启所有图优化
)
session = ort.InferenceSession("model.onnx", options)
```

**思考（15分钟）**：ONNX Runtime 的输入为什么必须是 numpy array 而不是 PyTorch Tensor？如果 PyTorch 和 ONNX Runtime 的输出不一致，可能是什么原因？

### 晚上 21:00-22:00：推理实战 + 数值对比

```python
# week2/day4_onnxruntime_inference.py
"""
用 ONNX Runtime 跑推理，并与 PyTorch 输出做数值对比
这是验证 ONNX 导出正确性的标准做法
"""
import torch
import torchvision.models as models
import onnxruntime as ort
import numpy as np
import time

# Step 1: 准备统一的测试输入
print("Step 1: 准备测试输入...")
torch.manual_seed(42)
np.random.seed(42)

input_np    = np.random.randn(1, 3, 224, 224).astype(np.float32)
input_torch = torch.from_numpy(input_np)

# Step 2: PyTorch 推理
print("\nStep 2: PyTorch 推理...")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

with torch.no_grad():
    start = time.time()
    pytorch_output = model(input_torch)
    pytorch_time = (time.time() - start) * 1000

pytorch_result = pytorch_output.numpy()
print(f"  PyTorch 推理耗时: {pytorch_time:.1f}ms")
print(f"  PyTorch Top-1 类别 ID: {np.argmax(pytorch_result[0])}")

# Step 3: ONNX Runtime 推理
print("\nStep 3: ONNX Runtime 推理...")

options = ort.SessionOptions()
options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

session = ort.InferenceSession(
    "week2/resnet50_dynamic_batch.onnx",
    sess_options=options
)

input_name  = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

start = time.time()
ort_outputs = session.run([output_name], {input_name: input_np})
ort_time = (time.time() - start) * 1000

ort_result = ort_outputs[0]
print(f"  ORT 推理耗时: {ort_time:.1f}ms")
print(f"  ORT Top-1 类别 ID: {np.argmax(ort_result[0])}")

# Step 4: 数值对比（关键验证）
print("\nStep 4: 数值对比验证...")

max_diff  = np.max(np.abs(pytorch_result - ort_result))
mean_diff = np.mean(np.abs(pytorch_result - ort_result))

print(f"  最大绝对误差: {max_diff:.6f}")
print(f"  平均绝对误差: {mean_diff:.6f}")

if max_diff < 1e-4:
    print("  OK PyTorch 和 ONNX Runtime 输出一致！导出正确")
else:
    print(f"  WARNING 误差较大（{max_diff:.6f}），请检查导出参数")

pytorch_top5 = np.argsort(pytorch_result[0])[-5:][::-1]
ort_top5     = np.argsort(ort_result[0])[-5:][::-1]
print(f"\n  PyTorch Top-5 类别 ID: {pytorch_top5}")
print(f"  ORT     Top-5 类别 ID: {ort_top5}")
print(f"  Top-5 完全一致: {list(pytorch_top5) == list(ort_top5)}")

# Step 5: 性能对比汇总
print("\n" + "=" * 50)
print("性能对比汇总（面试时可以提到）")
print("=" * 50)
print(f"  PyTorch CPU   | {pytorch_time:.1f}ms")
print(f"  ORT CPU       | {ort_time:.1f}ms")
speedup = pytorch_time / ort_time if ort_time > 0 else 0
print(f"  ORT 加速比    | {speedup:.1f}x")
print("\n  （ORT 通常比 PyTorch 快 1.5-3x，因为静态图优化）")
```

**今天的 GitHub commit**：

```bash
git add week2/day4_onnxruntime_inference.py
git commit -m "W2D4: ONNX Runtime Python 推理，PyTorch vs ORT 数值对比验证"
```

---

## 第五天 · 4月11日（周六）：图优化入门（onnx-simplifier）

> **时间**：早9:00-12:00（项目实战），下午15:00-17:00（总结），晚19:00-21:00（预习）
> **主题**：用 onnx-simplifier 做图折叠，观察节点数变化，理解图优化的基本原理

### 09:00-12:00：图优化实战

**先读（20分钟）**：[onnx-simplifier GitHub README](https://github.com/daquexian/onnx-simplifier)

理解 onnx-simplifier 做了什么：

- **常量折叠（Constant Folding）**：把编译期可以确定的值直接计算出来，减少运行时计算
- **算子融合（Op Fusion）**：把多个相邻算子合并成一个，减少内存读写
- **冗余节点消除**：删除 Identity、无用 Cast 等节点

```python
# week2/day5_onnx_simplify.py
"""
用 onnx-simplifier 对 ResNet50 做图优化，观察节点数变化
"""
import onnx
from onnxsim import simplify
import time
import os

onnx_path       = "week2/resnet50_dynamic_batch.onnx"
simplified_path = "week2/resnet50_simplified.onnx"

# 加载原始 ONNX 模型
print("加载原始 ONNX 模型...")
model = onnx.load(onnx_path)

original_nodes = len(model.graph.node)
print(f"原始节点数: {original_nodes}")

# 执行简化
print("\n执行 onnx-simplifier 图优化...")
start = time.time()
model_simplified, check = simplify(model)
elapsed = (time.time() - start) * 1000

if check:
    print(f"OK 简化成功！耗时: {elapsed:.0f}ms")
else:
    print("WARNING 简化后验证失败，使用原始模型")
    model_simplified = model

simplified_nodes = len(model_simplified.graph.node)
reduction = original_nodes - simplified_nodes
print(f"简化后节点数: {simplified_nodes}")
print(f"节点减少: {reduction} 个 ({reduction/original_nodes*100:.1f}%)")

# 保存简化后的模型
onnx.save(model_simplified, simplified_path)
print(f"\n简化模型已保存: {simplified_path}")

orig_size = os.path.getsize(onnx_path) / 1e6
simp_size = os.path.getsize(simplified_path) / 1e6
print(f"原始模型大小: {orig_size:.1f} MB")
print(f"简化模型大小: {simp_size:.1f} MB")

print("\nOK Day5 完成！")
```

### 15:00-17:00：整理图优化笔记

写 `week2/notes_day5.md`，记录：常量折叠、算子融合、冗余消除各自的原理，你观察到的节点数变化数据，以及什么情况下图优化效果最明显。

### 19:00-21:00：预习明天内容

快速浏览 [ONNX Runtime Python API 文档](https://onnxruntime.ai/docs/api/python/api_summary.html)，了解 InferenceSession 的参数选项，为明天的端到端 Demo 做准备。

**今天的 GitHub commit**：

```bash
git add week2/
git commit -m "W2D5: onnx-simplifier 图优化实战，节点数对比"
```

---

## 第六天 · 4月12日（周日）：端到端完整 Demo

> **时
## 第六天 · 4月12日（周日）：端到端完整 Demo

> **时间**：早9:00-12:00（主要实战），下午14:00-17:00（博客写作）
> **主题**：把前5天的内容串联成一个完整的端到端推理脚本，并写第二篇博客

### 09:00-12:00：端到端 Demo 实战

```python
# week2/day6_end_to_end_demo.py
"""
W2 核心产出：完整的端到端推理 Demo
PyTorch 模型 -> ONNX 导出 -> ONNX Runtime 推理 -> Top5 结果展示
"""
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import onnxruntime as ort
import numpy as np
import json
import os
import urllib.request

# ============================================================
# 工具函数
# ============================================================

def download_imagenet_labels(save_path="week2/imagenet_labels.json"):
    """下载 ImageNet 1000 类别标签"""
    if os.path.exists(save_path):
        with open(save_path) as f:
            return json.load(f)
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    print(f"下载 ImageNet 标签...")
    urllib.request.urlretrieve(url, save_path)
    with open(save_path) as f:
        return json.load(f)

def preprocess_image(image_path):
    """标准 ImageNet 预处理"""
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    img = Image.open(image_path).convert("RGB")
    return transform(img).unsqueeze(0)  # [1, 3, 224, 224]

def export_model_if_needed(model, onnx_path):
    """如果 ONNX 文件不存在，则导出"""
    if os.path.exists(onnx_path):
        print(f"  ONNX 文件已存在: {onnx_path}")
        return
    print(f"  导出 ONNX 模型...")
    dummy = torch.randn(1, 3, 224, 224)
    torch.onnx.export(
        model, dummy, onnx_path,
        input_names=["input"], output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
        opset_version=17
    )
    print(f"  OK 导出完成: {onnx_path}")

def run_inference(session, input_tensor_np):
    """ONNX Runtime 推理"""
    input_name  = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    outputs = session.run([output_name], {input_name: input_tensor_np})
    return outputs[0]

def show_top5(logits, labels):
    """展示 Top-5 预测结果"""
    probs = np.exp(logits) / np.sum(np.exp(logits))  # softmax
    top5_idx = np.argsort(probs[0])[-5:][::-1]
    print("\n  Top-5 预测结果：")
    for rank, idx in enumerate(top5_idx, 1):
        label = labels[idx] if idx < len(labels) else f"class_{idx}"
        print(f"    #{rank}: {label:30s} ({probs[0][idx]*100:.2f}%)")

# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 60)
    print("W2 端到端 Demo：PyTorch -> ONNX -> ORT 推理")
    print("=" * 60)

    # 1. 准备测试图片（使用随机图片，或替换为真实图片路径）
    test_image_path = "week2/test_image.jpg"
    if not os.path.exists(test_image_path):
        print("\n[提示] 没有找到测试图片，使用随机 Tensor 代替")
        input_np = np.random.randn(1, 3, 224, 224).astype(np.float32)
    else:
        print(f"\n使用测试图片: {test_image_path}")
        input_tensor = preprocess_image(test_image_path)
        input_np = input_tensor.numpy()

    # 2. 加载 PyTorch 模型并导出 ONNX
    print("\n[Step 1] 加载 PyTorch 模型...")
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.eval()

    onnx_path = "week2/resnet50_dynamic_batch.onnx"
    export_model_if_needed(model, onnx_path)

    # 3. 创建 ONNX Runtime Session
    print("\n[Step 2] 创建 ONNX Runtime Session...")
    options = ort.SessionOptions()
    options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    session = ort.InferenceSession(onnx_path, sess_options=options)
    print(f"  输入节点: {session.get_inputs()[0].name}, shape: {session.get_inputs()[0].shape}")
    print(f"  输出节点: {session.get_outputs()[0].name}, shape: {session.get_outputs()[0].shape}")

    # 4. 执行推理
    print("\n[Step 3] 执行推理...")
    import time
    start = time.time()
    result = run_inference(session, input_np)
    elapsed = (time.time() - start) * 1000
    print(f"  推理耗时: {elapsed:.1f}ms")
    print(f"  输出 shape: {result.shape}")

    # 5. 展示结果
    print("\n[Step 4] 解析结果...")
    try:
        labels = download_imagenet_labels()
        show_top5(result, labels)
    except Exception as e:
        print(f"  无法下载标签: {e}")
        top5_idx = np.argsort(result[0])[-5:][::-1]
        print(f"  Top-5 类别 ID: {top5_idx}")

    print("\n" + "=" * 60)
    print("OK W2 端到端 Demo 完成！")
    print("=" * 60)
    print("\n本周成果总结：")
    print("  1. ResNet50 成功导出为 ONNX 格式（动态 batch）")
    print("  2. ONNX Runtime 推理结果与 PyTorch 一致（误差 < 1e-4）")
    print("  3. 用 Netron 可视化了计算图，理解了节点结构")
    print("  4. 用 onnx-simplifier 做了图优化，节点数减少")
    print("  5. 完成端到端推理 Demo")
    print("\n下周（W3）：用 C++ ONNX Runtime API 做命令行推理 Demo")

if __name__ == "__main__":
    main()
```

### 14:00-17:00：写第二篇博客

在 `week2/blog_w2.md` 中写博客，标题：**《移动开发者的 ONNX 第一课：从 PyTorch 到端侧推理》**

博客结构建议：

1. 为什么需要 ONNX（移动端视角）
2. 导出过程中踩的坑（dynamic_axes 的重要性）
3. ONNX Runtime 推理的核心 API
4. PyTorch vs ORT 性能对比数据（你自己跑出来的真实数据）
5. 下周预告：C++ 推理

**今天的 GitHub commit**：

```bash
git add week2/
git commit -m "W2D6: 端到端 Demo 完成，第二篇博客草稿"
```

---

## 第七天 · 4月13日（周一）：W2 总结 + W3 预习

> **时间**：早7:00-8:00（总结），晚21:00-22:00（预习）
> **主题**：完成 W2 自检清单，预习 W3 的 C++ 环境搭建

### 早上 7:00-8:00：W2 总结

完成以下自检清单，每项都要有实际的代码/截图/数据支撑：

**W2 自检清单**

- [ ] 能用 `torch.onnx.export()` 导出 ResNet50，理解 `dynamic_axes` 的作用
- [ ] 能用 `onnx.checker.check_model()` 验证 ONNX 模型合法性
- [ ] 能用 Netron 打开 `.onnx` 文件，找到 Conv/BN/ReLU 节点并查看属性
- [ ] 能用 `onnxruntime.InferenceSession` 做推理，输入 numpy array，获取输出
- [ ] PyTorch 和 ORT 的推理结果最大误差 < 1e-4（记录你的实际数据）
- [ ] 能解释 `opset_version` 是什么，为什么选 17
- [ ] 用 onnx-simplifier 简化了模型，记录了节点数变化
- [ ] 完成端到端 Demo 脚本，能跑通完整流程
- [ ] 写了第二篇博客并发布（或草稿完成）
- [ ] GitHub 有本周的 commit 记录

**面试题自测**（能流畅回答以下问题）：

1. 为什么 PyTorch 模型不能直接在 Android 上运行？
2. `torch.onnx.export()` 的 `dynamic_axes` 参数有什么作用？不设置会怎样？
3. ONNX Runtime 比 PyTorch 推理快的原因是什么？
4. 如何验证 ONNX 导出的正确性？
5. `opset_version` 是什么？选择时需要考虑什么？

### 晚上 21:00-22:00：W3 预习

**W3 主题**：C++ ONNX Runtime 推理 Demo

预习内容：

1. 阅读 [ONNX Runtime C++ API 文档](https://onnxruntime.ai/docs/api/c/)，了解 `Ort::Session`、`Ort::Env`、`Ort::Value` 的基本用法
2. 了解 CMake 的基本概念（如果不熟悉的话）：[CMake 官方教程 Step 1](https://cmake.org/cmake/help/latest/guide/tutorial/A%20Basic%20Starting%20Point.html)
3. 思考：Python 版 ORT 和 C++ 版 ORT 的 API 有什么相似之处？

**今天的 GitHub commit**：

```bash
git add week2/
git commit -m "W2D7: W2 总结完成，W3 预习笔记，自检清单全部通过"
```

---

## W2 → W3 衔接说明

**W2 完成后你拥有**：

- 一个经过验证的 `resnet50_dynamic_batch.onnx` 文件（W3 直接复用）
- 对 ONNX 计算图结构的直觉认知（W9 图优化的基础）
- ONNX Runtime Python API 的使用经验（C++ API 结构类似）

**W3 要做的事**：

- 搭建 C++ 开发环境（CMake + ONNX Runtime C++ SDK）
- 用 C++ 加载 W2 导出的 `.onnx` 文件
- 实现命令行推理 Demo：`./inference resnet50.onnx image.jpg`
- 对比 Python ORT 和 C++ ORT 的推理速度

**W3 的核心挑战**：从 Python 的"一行代码"到 C++ 的"手动管理内存"，这是移动端开发者最熟悉的场景，不要怕。

---

## 本周参考资料汇总

| 资料 | 链接 | 用途 |
|------|------|------|
| ONNX 官方文档 | https://onnx.ai/onnx/intro/ | 概念理解 |
| ONNX 算子规范 | https://onnx.ai/onnx/operators/ | 查算子定义 |
| PyTorch ONNX 导出文档 | https://pytorch.org/docs/stable/onnx.html | 导出 API |
| ONNX Runtime Python 文档 | https://onnxruntime.ai/docs/get-started/with-python.html | 推理 API |
| ONNX Runtime API 参考 | https://onnxruntime.ai/docs/api/python/api_summary.html | 详细 API |
| Netron 在线版 | https://netron.app | 可视化 ONNX |
| onnx-simplifier | https://github.com/daquexian/onnx-simplifier | 图优化工具 |

---

*本文档由 CatDesk AI 于 2026年4月9日 自动生成，基于《端侧AI工程师3个月冲刺计划 v3.0》及 W1 完成情况制定。*
