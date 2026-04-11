# 移动端老兵转型端侧 AI：第一周，我跑通了 ResNet50 推理

> 15 年移动端开发，第一次让神经网络在我的 MacBook 上认出了一张图片。

---

## 我是谁，为什么要转型

我做了 15 年移动端开发，从 Objective-C 写到 Swift，从 Java 写到 Kotlin，经历了移动互联网最野蛮生长的年代。但最近两年，我越来越清晰地感受到：**端侧 AI 才是下一个真正的战场**。手机里的大模型、相机里的实时推理、可穿戴设备上的智能感知——这些都需要既懂 AI 又懂端侧工程的人。所以，我决定系统性地转型，从零开始学 PyTorch，目标是成为一名端侧 AI 工程师。

这是我的第一周学习记录。

---

## 这周学了什么

### 1. PyTorch Tensor 和 NumPy 有多像？

刚接触 PyTorch 的时候，我以为 Tensor 是个全新的东西，结果发现它和 NumPy 的 ndarray 几乎是孪生兄弟。下面这个对比让我一下子就理解了：

```python
import numpy as np
import torch

# ── 创建数组 / 张量 ──────────────────────────────────────
image_np = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)  # NumPy
image_t  = torch.randint(0, 256, (224, 224, 3), dtype=torch.uint8)   # PyTorch

# ── 维度变换（HWC → CHW）────────────────────────────────
chw_np = np.transpose(image_np, (2, 0, 1))          # NumPy
chw_t  = image_t.permute(2, 0, 1)                   # PyTorch

# ── 添加 batch 维度 ──────────────────────────────────────
batch_np = np.expand_dims(chw_np, 0)                # NumPy  → (1, 3, 224, 224)
batch_t  = chw_t.unsqueeze(0)                       # PyTorch → (1, 3, 224, 224)

# ── 互转：共享内存，改一个另一个也变 ────────────────────
arr = np.array([1, 2, 3])
t   = torch.from_numpy(arr)   # 共享内存
arr[0] = 100
print(t)  # tensor([100,   2,   3])  ← arr 改了，t 也变了
```

最让我惊喜的是 `from_numpy` 的共享内存机制——这和 iOS 里 `Data` 与 `UnsafeBufferPointer` 共享底层存储的思路如出一辙，移动端的内存意识在这里直接复用了。

---

### 2. 推理时为什么必须加 `torch.no_grad()`？

这是我这周搞得最清楚的一个原理点。PyTorch 的自动求导引擎（Autograd）在每次前向计算时，都会悄悄地把"计算图"记录下来，以便后续反向传播求梯度。

```python
# 训练阶段：需要梯度，Autograd 会记录计算图
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()
print(x.grad)  # tensor([7.])  ← dy/dx = 2x+3 = 7

# 推理阶段：不需要梯度，关掉计算图记录
with torch.no_grad():
    x2 = torch.tensor([2.0])
    y2 = 2 * x2 + 3 * x2 + 1
    print(y2.item())  # 11.0，没有梯度，但速度更快、内存更省
```

推理时加上 `torch.no_grad()` 有两个实际好处：**节省显存**（不用存中间激活值）和**加快速度**（省去了构建计算图的开销）。对于端侧部署来说，这两点都至关重要——手机上的内存就那么多，一点都不能浪费。

---

### 3. 图片前处理的 5 个步骤

把一张普通图片喂给 ResNet50，中间要经历 5 道"加工"：

```python
from torchvision import transforms

transform = transforms.Compose([
    # Step 1：缩放短边到 256px，保持宽高比
    transforms.Resize(256),

    # Step 2：从中心裁剪 224×224（与 ImageNet 训练对齐）
    transforms.CenterCrop(224),

    # Step 3：PIL Image → Tensor，像素值归一化到 [0, 1]
    transforms.ToTensor(),

    # Step 4：按 ImageNet 统计值做标准化（减均值、除标准差）
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std =[0.229, 0.224, 0.225]
    ),
])

input_tensor = transform(image)       # shape: (3, 224, 224)
input_batch  = input_tensor.unsqueeze(0)  # Step 5：加 batch 维度 → (1, 3, 224, 224)
print(input_batch.shape)  # torch.Size([1, 3, 224, 224])
```

这 5 步走完，一张任意尺寸的图片就变成了模型期待的 `(1, 3, 224, 224)` 张量——这就是 ResNet50 的"标准餐"。

---

## 我的第一个推理结果

代码跑通的那一刻，终端输出了这些：

```
 1. tabby, tabby cat              | 0.4821 | 🧧🧧🧧🧧🧧🧧🧧🧧🧧🧧🧧🧧🧧🧧
 2. tiger cat                     | 0.1732 | 🧧🧧🧧🧧🧧
 3. Egyptian cat                  | 0.0891 | 🧧🧧
 4. lynx, catamount               | 0.0312 | 🧧
 5. Persian cat                   | 0.0187 | 

推理耗时：187.3ms
模型参数：25,557,032 个
模型大小：98 MB（FP32）
设备：CPU（MacBook M 系列）
```

ResNet50 以 **48.2% 的置信度**认出了图片里的猫，Top-5 全是猫科动物，结果完全合理。**187ms 的 CPU 推理延迟**，对于一个没有任何优化的 FP32 模型来说，已经是个不错的基准数字——后续量化、ONNX 导出之后，这个数字还会大幅下降。

---

## 移动端工程师的意外优势

转型过程中，我发现自己有两个"意外优势"，是纯算法背景的同学不一定有的。

**第一个：理解内存布局让我秒懂 CHW 格式。** 移动端开发天天和内存打交道——图片的像素数据在内存里怎么排列、stride 是什么、为什么 `CVPixelBuffer` 要区分 planar 和 interleaved。所以当我看到 PyTorch 要求图片从 `HWC`（高×宽×通道，OpenCV 默认）转成 `CHW`（通道×高×宽）时，我立刻就明白了：这是为了让同一通道的数据在内存里连续存放，对 SIMD 指令和 GPU 的 cache 更友好。

**第二个：多线程经验让我理解为什么推理不能在主线程。** 做过 iOS/Android 的人都知道，主线程是 UI 线程，任何耗时操作都会卡帧。ResNet50 在 CPU 上跑一次推理要 187ms，远超一帧的 16ms 预算。这个直觉让我在设计推理架构时，天然就会把模型推理放到后台线程，用异步回调把结果传回 UI——这正是端侧 AI 工程化的核心思路之一。

---

## 下周预告

下周我要做一件真正有工程价值的事：**把 PyTorch 模型导出成 ONNX，实现跨框架部署**。

ONNX 是端侧 AI 的"通用语言"——导出之后，同一个模型可以用 CoreML 跑在 iPhone 上，用 NNAPI 跑在 Android 上，用 TensorRT 跑在 Jetson 上。这一步是从"能跑通推理"到"能真正部署到设备"的关键跨越。

如果你也在做类似的转型，欢迎关注，我们一起踩坑。

---

*本文代码均已上传至 [GitHub](https://github.com/gaodeying/on-device-ai-journey)，Week 1 目录下可以直接运行。*
