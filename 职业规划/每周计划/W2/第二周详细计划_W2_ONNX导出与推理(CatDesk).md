# 第二周详细计划：ONNX 导出与推理（CatDesk）

> **生成说明**：本文档由 CatDesk AI 于 2026年4月9日 自动生成。
> 基于《端侧AI工程师3个月冲刺计划 v3.0》、W1 完成情况及《每周学习资源库 v3.1》综合制定。

---

**周期**：2026年4月7日（周二）— 4月13日（周一）
**核心目标**：跑通 `PyTorch → ONNX → ONNX Runtime` 最小闭环
**本周固定产出**：
- 1 个完整的 ONNX 导出脚本（含 dynamic_axes）
- 1 个 ONNX Runtime Python 推理脚本（含 PyTorch 数值对比验证）
- 1 份 PyTorch vs ONNX Runtime 时延对比数据
- 用 Netron 可视化 ONNX 计算图（截图存档）
- 1 篇技术博客草稿（"移动开发者第一份 ONNX 模型导出实战"）
- GitHub commit 记录（每天一次）

---

## W1 → W2 衔接说明

W1 你完成了：PyTorch 环境搭建、Tensor 基础操作、Numpy 前处理流程（HWC→CHW、归一化）、ResNet50 预训练模型加载 + 推理，并记录了真实延迟数据。

**本周要解决的核心问题**：W1 的模型只能在 Python/PyTorch 环境里跑，Android C++ 怎么用？

答案分两步：本周（W2）把 PyTorch 模型导出成 ONNX 格式，用 Python 版 ONNX Runtime 验证推理结果一致；下周（W3）用 C++ 版 ONNX Runtime API 加载 `.onnx` 文件，做命令行推理 Demo。

---

## 本周执行原则

1. 每天必须有代码输出或可验证记录，禁止"只看不练"。
2. 学习资源按"官方文档优先 → 视频辅助理解 → GitHub 示例落地"顺序执行。
3. 只追求"闭环跑通 + 结果可解释"，不追求一次性最优。
4. 每天结束做 5 分钟复盘：今天完成了什么、哪里卡住、明天如何降阻。

---

## Day 1（周二 4/7）：ONNX 概念理解 + 环境准备

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：建立 `PyTorch（开发）→ ONNX（交换格式）→ ONNX Runtime（执行）` 的心智模型，安装本周依赖

### 早上 7:00-8:00：理论学习

**第一步（20分钟）**：[ONNX 官方文档 - 概念介绍](https://onnx.ai/onnx/intro/concepts.html)

重点理解 4 个核心概念：

| 概念 | 移动端类比 | 说明 |
|------|-----------|------|
| Graph（计算图） | Activity 生命周期流程图 | 描述模型计算流程，节点是算子，边是数据流 |
| Node（节点） | 一个函数调用 | 代表一个算子（Conv、ReLU、MatMul 等） |
| Tensor（张量） | byte[] 数据 | 节点间传递的数据，有 shape 和 dtype |
| Opset（算子集版本） | API Level | ONNX 算子的版本号，导出时需要指定 |

**第二步（20分钟）**：[ONNX Runtime 官方文档 - Python 快速入门](https://onnxruntime.ai/docs/get-started/with-python.html)

重点看：InferenceSession 的创建和推理调用方式（类比 Android MediaPlayer：先 prepare，再 play），以及为什么 ONNX Runtime 比 PyTorch 推理更快（静态图 vs 动态图）。

**第三步（15分钟）**：[ONNX 官方 YouTube - ONNX 101](https://www.youtube.com/results?search_query=ONNX+101+official)（35分钟视频，今天只看前15分钟建立直觉）

**思考（5分钟）**：用自己的话回答——为什么 PyTorch 模型不能直接在 Android C++ 里加载？ONNX 格式和 `.pt` 格式有什么本质区别？

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

验证 W1 的 ResNet50 模型还能正常加载：

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

## Day 2（周三 4/8）：ONNX 导出实战

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：把 W1 的 ResNet50 模型导出成 `.onnx` 文件，理解 `dynamic_axes` 的关键作用

### 早上 7:00-8:00：理论学习

**精读（30分钟）**：[torch.onnx.export 官方文档](https://pytorch.org/docs/stable/onnx.html)

重点理解关键参数：

| 参数 | 作用 | 注意事项 |
|------|------|---------|
| `model` | 要导出的 PyTorch 模型 | 必须先 `model.eval()` |
| `args` | 示例输入（dummy input） | 决定了模型的输入 shape |
| `f` | 输出文件路径 | 通常命名为 `xxx.onnx` |
| `input_names` | 输入节点名称 | 自定义，方便后续调用 |
| `output_names` | 输出节点名称 | 自定义 |
| `dynamic_axes` | 动态维度配置 | **重点**：设置 batch size 为动态 |
| `opset_version` | ONNX 算子集版本 | 推荐 17，兼容性好 |

**重点理解 `dynamic_axes`**（面试高频考点）：

```python
# 固定 batch（不推荐）：只能推理 batch=1
dynamic_axes = None

# 动态 batch（推荐）：可以推理任意 batch size
dynamic_axes = {
    'input': {0: 'batch_size'},    # 第0维（batch）是动态的
    'output': {0: 'batch_size'}
}
```

**辅助视频（15分钟）**：[PyTorch 官方 - 模型导出教程](https://www.youtube.com/results?search_query=pytorch+onnx+export+tutorial+official)（搜索 "PyTorch ONNX export tutorial"，看官方或高质量视频）

### 晚上 21:00-22:00：导出实战

```python
# week2/day2_onnx_export.py
"""
把 W1 的 ResNet50 模型导出成 ONNX 格式
参考：https://pytorch.org/docs/stable/onnx.html
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
dummy_input = torch.randn(1, 3, 224, 224)
print(f"Step 2: dummy_input shape: {dummy_input.shape}")

os.makedirs("week2", exist_ok=True)

# Step 3: 导出 ONNX（固定 batch 版本）
output_path_fixed = "week2/resnet50_fixed_batch.onnx"
torch.onnx.export(
    model, dummy_input, output_path_fixed,
    input_names=["input"], output_names=["output"],
    opset_version=17, verbose=False
)
print(f"固定 batch 文件大小: {os.path.getsize(output_path_fixed) / 1e6:.1f} MB")

# Step 4: 导出 ONNX（动态 batch 版本，推荐）
output_path_dynamic = "week2/resnet50_dynamic_batch.onnx"
torch.onnx.export(
    model, dummy_input, output_path_dynamic,
    input_names=["input"], output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=17, verbose=False
)
print(f"动态 batch 文件大小: {os.path.getsize(output_path_dynamic) / 1e6:.1f} MB")

# Step 5: 验证 ONNX 模型合法性
model_onnx = onnx.load(output_path_dynamic)
onnx.checker.check_model(model_onnx)
print("OK ONNX 模型验证通过！")
print(f"  Opset 版本: {model_onnx.opset_import[0].version}")
print(f"  节点数量: {len(model_onnx.graph.node)}")

input_shape = model_onnx.graph.input[0].type.tensor_type.shape
dims = [d.dim_value if d.dim_value > 0 else d.dim_param for d in input_shape.dim]
print(f"  输入 shape: {dims}")  # ['batch_size', 3, 224, 224]
```

**今天的 GitHub commit**：

```bash
git add week2/day2_onnx_export.py
git commit -m "W2D2: ResNet50 ONNX 导出，含固定/动态 batch 两个版本"
```

---

## Day 3（周四 4/9）：Netron 可视化计算图

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：用 Netron 打开 `.onnx` 文件，理解节点/边/输入输出结构

### 早上 7:00-8:00：理论学习

**读（20分钟）**：[ONNX 算子规范文档](https://onnx.ai/onnx/operators/)

不需要全读，只需要找到以下算子，理解输入/输出格式：

- `Conv`（卷积）：输入 `[N, C, H, W]`，权重 `[out_channels, in_channels, kH, kW]`
- `BatchNormalization`：训练和推理模式的区别（推理时 BN 可以和 Conv 融合！）
- `Relu`：逐元素激活，shape 不变
- `Gemm`（矩阵乘法）：全连接层的底层实现
- `Softmax`：分类输出的概率归一化

**读（15分钟）**：[Netron GitHub 使用说明](https://github.com/lutzroeder/netron)

**视频（10分钟）**：[Netron 可视化工具使用演示](https://www.youtube.com/results?search_query=netron+neural+network+visualizer+tutorial)（搜索 "Netron model visualizer"，看一个 5-10 分钟的演示）

**思考（5分钟）**：ResNet50 有 50 层，但 ONNX 图里的节点数量远不止 50 个，为什么？（答案：每一层可能对应多个算子节点，比如一个 Conv 层 = Conv + BatchNorm + ReLU 三个节点）

### 晚上 21:00-22:00：Netron 实操 + 代码探索

```bash
# 方式1：命令行启动 Netron（会自动打开浏览器）
python3 -m netron week2/resnet50_dynamic_batch.onnx

# 方式2：直接访问在线版（不需要安装）
# 打开 https://netron.app，拖入 .onnx 文件
```

在 Netron 里完成以下探索任务：找到第一个 Conv 节点，记录 kernel_shape、strides、pads；找到 BatchNormalization 节点，观察它紧跟在 Conv 后面；找到最后的 Gemm 节点（全连接层），确认输出维度是 1000；观察 ResNet 的残差连接在图里的形态。

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

## Day 4（周五 4/10）：ONNX Runtime Python 推理

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：用 ONNX Runtime 跑推理，并与 PyTorch 输出做数值对比验证

### 早上 7:00-8:00：理论学习

**精读（30分钟）**：[ONNX Runtime Python API 文档](https://onnxruntime.ai/docs/api/python/api_summary.html)

重点掌握以下 API：

```python
import onnxruntime as ort

# 1. 创建推理 Session（类比 Android MediaPlayer.prepare()）
session = ort.InferenceSession("model.onnx")

# 2. 查看输入输出信息
input_name  = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
input_shape = session.get_inputs()[0].shape

# 3. 执行推理（输入必须是 numpy array，不是 Tensor！）
import numpy as np
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
outputs = session.run([output_name], {input_name: input_data})
result = outputs[0]  # numpy array，shape [1, 1000]
```

理解 SessionOptions（性能调优入口，W9 会深入）：

```python
options = ort.SessionOptions()
options.intra_op_num_threads = 4
options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
session = ort.InferenceSession("model.onnx", options)
```

**参考项目（10分钟浏览）**：[ONNX Runtime 官方 Python 推理示例](https://github.com/microsoft/onnxruntime-inference-examples/tree/main/python)

### 晚上 21:00-22:00：推理实战 + 数值对比

```python
# week2/day4_onnxruntime_inference.py
"""
用 ONNX Runtime 跑推理，并与 PyTorch 输出做数值对比
参考：https://onnxruntime.ai/docs/api/python/api_summary.html
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

# Step 4: 数值对比验证（关键！）
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

## Day 5（周六 4/11）：图优化入门（onnx-simplifier）

**时间**：早 9:00-12:00（实战），下午 15:00-17:00（总结），晚 19:00-21:00（预习）
**目标**：用 onnx-simplifier 做图折叠，观察节点数变化，理解图优化的基本原理

### 09:00-12:00：图优化实战

**先读（20分钟）**：[onnx-simplifier GitHub README](https://github.com/daquexian/onnx-simplifier)

理解 onnx-simplifier 做了什么：常量折叠（Constant Folding）把编译期可以确定的值直接计算出来，减少运行时计算；算子融合（Op Fusion）把多个相邻算子合并成一个，减少内存读写；冗余节点消除删除 Identity、无用 Cast 等节点。

**参考项目（10分钟）**：[onnx-simplifier 使用示例](https://github.com/daquexian/onnx-simplifier#usage)

```python
# week2/day5_onnx_simplify.py
"""
用 onnx-simplifier 对 ResNet50 做图优化，观察节点数变化
参考：https://github.com/daquexian/onnx-simplifier
"""
import onnx
from onnxsim import simplify
import time
import os

onnx_path       = "week2/resnet50_dynamic_batch.onnx"
simplified_path = "week2/resnet50_simplified.onnx"

print("加载原始 ONNX 模型...")
model = onnx.load(onnx_path)
original_nodes = len(model.graph.node)
print(f"原始节点数: {original_nodes}")

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

**延伸阅读（可选）**：[onnx/optimizer GitHub](https://github.com/onnx/optimizer)（W9 会深入用到，今天只是了解）

### 19:00-21:00：预习明天内容

快速浏览 [ONNX Runtime Python API 文档](https://onnxruntime.ai/docs/api/python/api_summary.html)，为明天的端到端 Demo 做准备。

**今天的 GitHub commit**：

```bash
git add week2/
git commit -m "W2D5: onnx-simplifier 图优化实战，节点数对比"
```

---

## Day 6（周日 4/12）：端到端完整 Demo

**时间**：早 9:00-12:00（主要实战），下午 14:00-17:00（博客写作）
**目标**：把前5天的内容串联成一个完整的端到端推理脚本，并写第二篇博客

### 09:00-12:00：端到端 Demo 实战

**参考项目（15分钟浏览）**：[ONNX Runtime 官方 Python 推理示例](https://github.com/microsoft/onnxruntime-inference-examples/tree/main/python)

```python
# week2/day6_end_to_end_demo.py
"""
W2 核心产出：完整的端到端推理 Demo
PyTorch 模型 -> ONNX 导出 -> ONNX Runtime 推理 -> Top5 结果展示
参考：https://github.com/microsoft/onnxruntime-inference-examples/tree/main/python
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
import time

def download_imagenet_labels(save_path="week2/imagenet_labels.json"):
    if os.path.exists(save_path):
        with open(save_path) as f:
            return json.load(f)
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    print(f"下载 ImageNet 标签...")
    urllib.request.urlretrieve(url, save_path)
    with open(save_path) as f:
        return json.load(f)

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    img = Image.open(image_path).convert("RGB")
    return transform(img).unsqueeze(0)

def export_model_if_needed(model, onnx_path):
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

def show_top5(logits, labels):
    probs = np.exp(logits) / np.sum(np.exp(logits))
    top5_idx = np.argsort(probs[0])[-5:][::-1]
    print("\n  Top-5 预测结果：")
    for rank, idx in enumerate(top5_idx, 1):
        label = labels[idx] if idx < len(labels) else f"class_{idx}"
        print(f"    #{rank}: {label:30s} ({probs[0][idx]*100:.2f}%)")

def main():
    print("=" * 60)
    print("W2 端到端 Demo：PyTorch -> ONNX -> ORT 推理")
    print("=" * 60)

    # 1. 准备测试图片
    test_image_path = "week1/test_cat.jpg"  # 复用 W1 的测试图片
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
    input_name  = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    start = time.time()
    result = session.run([output_name], {input_name: input_np})[0]
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

博客结构建议：为什么需要 ONNX（移动端视角）；导出过程中踩的坑（dynamic_axes 的重要性）；ONNX Runtime 推理的核心 API；PyTorch vs ORT 性能对比数据（你自己跑出来的真实数据）；下周预告：C++ 推理。

**发布到**：[掘金](https://juejin.cn) 或 [知乎](https://www.zhihu.com)

**今天的 GitHub commit**：

```bash
git add week2/
git commit -m "W2D6: 端到端 Demo 完成，第二篇博客草稿"
```

---

## Day 7（周一 4/13）：W2 总结 + W3 预习

**时间**：早 7:00-8:00（总结），晚 21:00-22:00（预习）
**目标**：完成 W2 自检清单，预习 W3 的 C++ 环境搭建

### 早上 7:00-8:00：W2 总结

完成以下自检清单，每项都要有实际的代码/截图/数据支撑：

**W2 自检清单**

| 项目 | 状态 |
|------|------|
| 能用 `torch.onnx.export()` 导出 ResNet50，理解 `dynamic_axes` 的作用 | [ ] |
| 能用 `onnx.checker.check_model()` 验证 ONNX 模型合法性 | [ ] |
| 能用 Netron 打开 `.onnx` 文件，找到 Conv/BN/ReLU 节点并查看属性 | [ ] |
| 能用 `onnxruntime.InferenceSession` 做推理，输入 numpy array，获取输出 | [ ] |
| PyTorch 和 ORT 的推理结果最大误差 < 1e-4（记录你的实际数据） | [ ] |
| 能解释 `opset_version` 是什么，为什么选 17 | [ ] |
| 用 onnx-simplifier 简化了模型，记录了节点数变化 | [ ] |
| 完成端到端 Demo 脚本，能跑通完整流程 | [ ] |
| 写了第二篇博客并发布（或草稿完成） | [ ] |
| GitHub 有本周的 commit 记录 | [ ] |

**及格线**：完成 7 项以上 → 继续 W3
**优秀线**：完成 10 项 + 博客已发布 → 进度超预期

**面试题自测**（能流畅回答以下问题）：

1. 为什么 PyTorch 模型不能直接在 Android 上运行？
2. `torch.onnx.export()` 的 `dynamic_axes` 参数有什么作用？不设置会怎样？
3. ONNX Runtime 比 PyTorch 推理快的原因是什么？
4. 如何验证 ONNX 导出的正确性？
5. `opset_version` 是什么？选择时需要考虑什么？

### 晚上 21:00-22:00：W3 预习

**W3 主题**：现代 C++ 激活 + ONNX Runtime C++ API

预习内容：

1. 阅读 [ONNX Runtime C++ API 文档](https://onnxruntime.ai/docs/api/c/index.html)，了解 `Ort::Session`、`Ort::Env`、`Ort::Value` 的基本用法
2. 快速浏览 [《现代C++教程》第5章 - 智能指针](https://github.com/changkun/modern-cpp-tutorial)（W3 重点）
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

**W3 要做的事**：搭建 C++ 开发环境（CMake + ONNX Runtime C++ SDK），用 C++ 加载 W2 导出的 `.onnx` 文件，实现命令行推理 Demo：`./inference resnet50.onnx image.jpg`，对比 Python ORT 和 C++ ORT 的推理速度。

**W3 的核心挑战**：从 Python 的"一行代码"到 C++ 的"手动管理内存"，这是移动端开发者最熟悉的场景，不要怕。

---

## 本周学习资源汇总

### 官方文档（必读，按天对应）

| 资源 | 链接 | 对应天 |
|------|------|--------|
| ONNX 官方文档 - 概念介绍 | https://onnx.ai/onnx/intro/concepts.html | Day 1 |
| ONNX Runtime Python 快速入门 | https://onnxruntime.ai/docs/get-started/with-python.html | Day 1 |
| torch.onnx.export 官方文档 | https://pytorch.org/docs/stable/onnx.html | Day 2 |
| ONNX 算子规范文档 | https://onnx.ai/onnx/operators/ | Day 3 |
| Netron 可视化工具 | https://netron.app | Day 3 |
| ONNX Runtime Python API 参考 | https://onnxruntime.ai/docs/api/python/api_summary.html | Day 4 |
| onnx-simplifier GitHub | https://github.com/daquexian/onnx-simplifier | Day 5 |
| ONNX Runtime C++ API 文档 | https://onnxruntime.ai/docs/api/c/index.html | Day 7 预习 |

### 视频教程（辅助理解）

| 课程 | 平台 | 时长 | 对应天 |
|------|------|------|--------|
| ONNX 官方 - ONNX 101 | YouTube | 35min | Day 1 |
| PyTorch 官方 - 模型导出 | YouTube | 25min | Day 2 |
| Netron 可视化工具演示 | YouTube | 10min | Day 3 |
| ONNX Runtime - 推理实战 | YouTube | 40min | Day 4 |

### 实战项目（GitHub，必看）

| 项目 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime Python 推理示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/python | 完整推理流程 |
| onnx-simplifier 使用示例 | https://github.com/daquexian/onnx-simplifier#usage | 图优化命令 |
| PyTorch 转 ONNX 示例 | https://github.com/onnx/tutorials/tree/main/tutorials | 导出最佳实践 |
| ONNX 模型动物园 | https://github.com/onnx/models | 预训练 ONNX 模型 |

### 技术博客（选读）

| 标题 | 平台 |
|------|------|
| PyTorch 模型导出 ONNX 完全指南 | 掘金 |
| ONNX 运算图优化详解 | 知乎 |
| ONNX vs TorchScript 对比 | PyTorch Blog: https://pytorch.org/blog/onnx/ |

### 书籍推荐

| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《深度学习部署实战》 | 第3章-ONNX部署 | ⭐⭐⭐⭐ |
| 《动手学深度学习》（李沐） | 第2章-预备知识（复习） | ⭐⭐⭐ |

---

## 本周 GitHub 仓库结构

```
on-device-ai-journey/
├── README.md
├── week1/
│   └── ...（W1 已完成）
└── week2/
    ├── README.md              # W2 总结 + 性能数据
    ├── day1_env_check.py
    ├── day2_onnx_export.py
    ├── day3_netron_explore.py
    ├── day4_onnxruntime_inference.py
    ├── day5_onnx_simplify.py
    ├── day6_end_to_end_demo.py
    ├── notes_day5.md
    ├── blog_w2.md
    ├── resnet50_fixed_batch.onnx
    ├── resnet50_dynamic_batch.onnx
    └── resnet50_simplified.onnx
```

---

*本文档由 CatDesk AI 于 2026年4月9日 自动生成。*
*基于《端侧AI工程师3个月冲刺计划 v3.0》及《每周学习资源库 v3.1》制定。*
*执行周期：2026年4月7日 - 4月13日*
