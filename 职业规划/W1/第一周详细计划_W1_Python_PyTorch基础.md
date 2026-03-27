# W1 详细执行计划：Python + PyTorch 基础强化

> **周期**：2026年4月1日（周三）— 4月6日（周一）
> **核心目标**：建立张量思维，掌握 Numpy/PyTorch 核心操作
> **本周产出**：
> - ✅ 一个可运行的 PyTorch 推理 Demo（ResNet50 跑图片分类）
> - ✅ 一篇技术博客草稿（"移动端开发者的PyTorch第一周"）
> - ✅ GitHub 仓库建立 + 第一次 commit

---

## 开始前（3月26日 - 3月31日）：预热准备

> **用时**：30分钟，一次性完成，不占学习时间

**必做事项**：

1. **建立 GitHub 仓库**（面试展示用，越早越好）
   ```
   仓库名：on-device-ai-journey
   描述：Android/iOS Dev → On-Device AI Engineer | 3-Month Journey
   README：写你的背景 + 学习目标 + 周次规划
   ```

2. **收藏以下网址**（本周会频繁用到）
   - PyTorch 60分钟入门：https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
   - 《动手学深度学习》在线版：https://zh.d2l.ai/chapter_preliminaries/ndarray.html
   - Numpy 官方入门：https://numpy.org/doc/stable/user/quickstart.html
   - cppreference（备用）：https://en.cppreference.com/w/

3. **配置环境（可提前做）**
   ```bash
   # 检查 Python 版本 ≥ 3.10
   python3 --version

   # 安装 Conda（如未安装）
   # 下载地址：https://docs.conda.io/en/latest/miniconda.html

   # 创建虚拟环境
   conda create -n ondevice-ai python=3.10
   conda activate ondevice-ai

   # 安装核心依赖（M系Mac用CPU版PyTorch即可）
   pip install torch torchvision numpy matplotlib pillow
   pip install jupyter notebook   # 可选，方便交互调试
   ```

---

## 第一天 · 4月1日（周三）：环境搭建 + 整体认知建立

> **时间**：早7:00-8:00（理论），晚21:00-22:00（实操）
> **主题**：知道自己在学什么，跑通第一行代码

### 早上 7:00-8:00：认知建立（重要，不能跳过）

**为什么这样安排**：作为移动开发者，你有15年工程经验，但缺乏 AI 框架的心智模型。第一天的核心任务不是写代码，而是建立"我在做什么"的全局认知。

**必读（按顺序）**：

1. **先读这篇（15分钟）**：[PyTorch 60分钟入门 - 第1节：张量](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
   - 只读到 "Operations on Tensors" 部分，不要往后翻
   - 重点建立一个类比：**Tensor ≈ Android 里的 float[][]，但多了自动求导能力**
   - 记录：PyTorch 的 Tensor 和 Numpy array 有什么关系？（答案：互转无缝）

2. **再看这个（20分钟）**：李沐 B 站《动手学深度学习》2.1 数据操作
   - B站搜索"李沐动手学深度学习"，找第2章第1节
   - **为什么看这个而不是官方视频**：李沐用中文讲，配合代码现场演示，对移动端工程师友好得多
   - 这节课会让你搞懂：shape、dtype、广播机制这3个核心概念

3. **最后扫一眼（10分钟）**：3Blue1Brown [神经网络本质](https://www.youtube.com/watch?v=aircAruvnKk)
   - 只看前5分钟，建立直觉：神经网络 = 矩阵乘法的堆叠

### 晚上 21:00-22:00：动手搭环境

**操作序列（严格按顺序）**：

```bash
# Step 1: 验证 Conda 环境
conda activate ondevice-ai
python3 -c "import torch; print(torch.__version__)"
# 预期输出：2.x.x

# Step 2: 跑通第一行代码（复制到终端）
python3 -c "
import torch
import numpy as np

# 创建张量
t = torch.randn(2, 3)
print('Tensor:', t)
print('Shape:', t.shape)
print('Dtype:', t.dtype)

# Tensor → Numpy
arr = t.numpy()
print('As numpy:', arr)

# Numpy → Tensor
t2 = torch.from_numpy(arr)
print('Back to tensor:', t2)

print('✅ 环境正常！')
"
```

**今天的 GitHub commit**：
```bash
mkdir -p ~/on-device-ai-journey/week1
cd ~/on-device-ai-journey
echo "# Week1: Python + PyTorch 基础" > week1/README.md
git add . && git commit -m "W1D1: 环境搭建完成，第一行 PyTorch 代码跑通"
```

**今天不需要理解自动求导**，那是明天后天的事。

---

## 第二天 · 4月2日（周四）：Python 进阶语法扫盲

> **时间**：早7:00-8:00（理论），晚21:00-22:00（实操）
> **主题**：补足 Python 工程语法，这些语法在 PyTorch 源码和 AI 项目里无处不在

### 为什么今天学 Python 语法？

你是终端工程师，Python 语法你懂基础，但以下3个特性在 AI 代码里出现频率极高，**不懂会导致读不懂 PyTorch 源码和 GitHub 示例**：

1. **列表/字典/集合推导式** → 模型层结构遍历
2. **装饰器 @** → `@torch.no_grad()`、`@property`（AI代码里到处是）
3. **Context Manager (with 语句)** → `with torch.no_grad():`, `with profile(...) as prof:`

### 早上 7:00-8:00：理论学习

**必读（按顺序，这个顺序有连贯性）**：

**第一步（20分钟）：推导式**
- 读：[Python 官方文档 - List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- 只需要掌握列表推导式，字典推导式看懂即可
- 核心在于：`[表达式 for 变量 in 可迭代对象 if 条件]`

**第二步（20分钟）：装饰器**
- 读：[Python 官方文档 - decorator 词条](https://docs.python.org/3/glossary.html#term-decorator)
- 再看一个具体示例，B 站搜"Python 装饰器 10分钟"（随便一个，只看函数装饰器）
- **移动端类比**：装饰器 ≈ AOP（面向切面编程），你在 Android 里用过注解处理器，道理一样

**第三步（15分钟）：Context Manager**
- 读：[Python 文档 - Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
- 理解：`with X as y:` = `y = X.__enter__(); ...; X.__exit__()`
- **为什么重要**：`with torch.no_grad():` 是推理代码的必用语法

### 晚上 21:00-22:00：代码实操

把今天的概念全部串联到一个练习文件里：

```python
# week1/day2_python_review.py

# ============ 推导式 ============
# 应用：遍历模型层
layers = ['conv1', 'bn1', 'relu', 'conv2', 'fc']
conv_layers = [l for l in layers if 'conv' in l]
print(f"Conv layers: {conv_layers}")

# 字典推导式：构建层名到索引的映射
layer_idx = {name: idx for idx, name in enumerate(layers)}
print(f"Layer index: {layer_idx}")

# ============ 装饰器 ============
import time
import functools

def timer(func):
    """用来测量函数执行时间，这在 AI 推理计时里非常常见"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000
        print(f"[Timer] {func.__name__} 耗时: {elapsed:.2f}ms")
        return result
    return wrapper

@timer
def fake_inference(batch_size=1):
    """模拟一次推理调用"""
    import time
    time.sleep(0.05)  # 模拟50ms推理
    return [0.9, 0.05, 0.05]  # 假设的分类概率

result = fake_inference()
print(f"推理结果: {result}")

# ============ Context Manager ============
import torch

# 关键：推理时必须用 no_grad，否则会计算梯度浪费内存
with torch.no_grad():
    x = torch.randn(1, 3, 224, 224)  # 模拟一张图片
    # 如果这里跑真实模型，不会记录梯度
    print(f"输入 shape: {x.shape}")
    print(f"内存效率更高，梯度不会被计算")

print("✅ Day2 完成")
```

**今天的 GitHub commit**：
```bash
git add week1/day2_python_review.py
git commit -m "W1D2: Python 推导式/装饰器/Context Manager 练习"
```

---

## 第三天 · 4月3日（周五）：Numpy 实战

> **时间**：早7:00-8:00（理论），晚21:00-22:00（实操）
> **主题**：Numpy 是 PyTorch 的"前辈"，搞懂它才能搞懂张量操作
> **连贯性**：今天的 Numpy 知识直接为明天的 PyTorch Tensor 铺路

### 为什么要单独学 Numpy？

你可能觉得"我直接学 PyTorch 不就行了？"——不行，原因如下：

1. **AI 推理的前后处理几乎全用 Numpy**（图片读取、resize、normalize 都是 Numpy 操作）
2. **PyTorch Tensor 和 Numpy 共享内存**（`t.numpy()` 零拷贝），不理解这个会导致隐藏 Bug
3. **推理结果是 Numpy array**，解析输出、画图全靠 Numpy

### 早上 7:00-8:00：理论学习

**学习路径（连贯，不要乱序）**：

**第一步（15分钟）**：[Numpy 官方快速入门](https://numpy.org/doc/stable/user/quickstart.html)
- 只读到 "Shape Manipulation" 部分
- 重点记住：`ndim`、`shape`、`dtype`、`reshape`、`flatten`

**第二步（20分钟）**：《动手学深度学习》[2.1 数据操作](https://zh.d2l.ai/chapter_preliminaries/ndarray.html)
- 这节讲的是 PyTorch Tensor，但所有概念和 Numpy 是通用的
- **连贯性**：今天用 Numpy 练，明天换成 Tensor，API 几乎一样

**第三步（10分钟）**：重点理解广播（Broadcasting）
- 读：[Numpy Broadcasting 官方解释](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- 用你的 Android 类比：广播 ≈ dp 单位自动适配屏幕密度，形状不同的数组可以直接运算

### 晚上 21:00-22:00：代码实操

```python
# week1/day3_numpy_practice.py
import numpy as np

print("=" * 40)
print("1. 基础操作")
print("=" * 40)

# 创建数组（对应图片的形状理解）
# 一张 224×224 RGB 图片 = shape (224, 224, 3)
image = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
print(f"图片 shape: {image.shape}")
print(f"图片 dtype: {image.dtype}")

# resize 操作（手工实现缩放理解）
# 实际工程用 PIL 或 cv2，但理解这个操作很重要
h, w = image.shape[:2]
print(f"原始尺寸: {w}×{h}")

print("\n" + "=" * 40)
print("2. 核心操作：切片和索引")
print("=" * 40)

# 提取第一个颜色通道（R通道）
r_channel = image[:, :, 0]
print(f"R通道 shape: {r_channel.shape}")

# 提取左上角 32×32 patch
patch = image[:32, :32, :]
print(f"图片 patch shape: {patch.shape}")

print("\n" + "=" * 40)
print("3. 关键操作：归一化（AI推理必用）")
print("=" * 40)

# 把图片像素从 [0, 255] 归一化到 [0.0, 1.0]
image_float = image.astype(np.float32) / 255.0
print(f"归一化后 dtype: {image_float.dtype}")
print(f"最小值: {image_float.min():.4f}, 最大值: {image_float.max():.4f}")

# ImageNet 标准化（均值/标准差，ResNet 推理必用）
mean = np.array([0.485, 0.456, 0.406])   # ImageNet 均值
std  = np.array([0.229, 0.224, 0.225])   # ImageNet 标准差
# 广播：mean shape (3,) 与 image_float shape (224, 224, 3) 自动对齐
normalized = (image_float - mean) / std
print(f"标准化后均值: {normalized.mean(axis=(0,1))}")

print("\n" + "=" * 40)
print("4. 关键操作：维度变换（HWC → CHW）")
print("=" * 40)

# PyTorch 需要 CHW 格式（通道×高×宽），OpenCV 是 HWC 格式
# 这个转换在实际推理前处理中必须做
image_chw = np.transpose(normalized, (2, 0, 1))  # (H, W, C) → (C, H, W)
print(f"HWC → CHW: {normalized.shape} → {image_chw.shape}")

# 添加 batch 维度（模型需要 NCHW = batch × channel × height × width）
image_batch = np.expand_dims(image_chw, axis=0)
print(f"添加 batch 维度: {image_chw.shape} → {image_batch.shape}")
print(f"最终输入 shape: {image_batch.shape}  ← 这就是 ResNet50 的标准输入格式！")

print("\n" + "=" * 40)
print("5. Numpy ↔ 矩阵运算")
print("=" * 40)

A = np.array([[1, 2], [3, 4]], dtype=np.float32)
B = np.array([[5, 6], [7, 8]], dtype=np.float32)

print(f"矩阵乘法 A@B:\n{A @ B}")            # @ 运算符
print(f"点积 np.dot:\n{np.dot(A, B)}")      # 等价
print(f"转置:\n{A.T}")
print(f"逐元素乘:\n{A * B}")               # 不是矩阵乘！

print("\n✅ Day3 完成，明天开始真正的 PyTorch Tensor！")
```

**今天的 GitHub commit**：
```bash
git add week1/day3_numpy_practice.py
git commit -m "W1D3: Numpy 数组操作、归一化、HWC→CHW 前处理练习"
```

---

## 第四天 · 4月4日（周六）：PyTorch Tensor 深入

> **时间**：早9:00-12:00（项目实战），下午15:00-17:00（总结），晚19:00-21:00（预习）
> **主题**：Tensor 是 PyTorch 的核心，今天要把它摸透
> **连贯性**：昨天的 Numpy 知识今天全部复用，换成 PyTorch API 即可

### 09:00-12:00：PyTorch Tensor 系统学习

**学习资源顺序（精心设计，不要乱）**：

**第一步（30分钟）**：[PyTorch 官方 60分钟入门](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
- 精读第1节"Tensors"
- 重点对照昨天的 Numpy 代码，找一一对应的 PyTorch API：

| Numpy | PyTorch | 说明 |
|-------|---------|------|
| `np.array([1,2,3])` | `torch.tensor([1,2,3])` | 创建 |
| `arr.shape` | `t.shape` 或 `t.size()` | 形状 |
| `arr.reshape(2,3)` | `t.view(2,3)` 或 `t.reshape(2,3)` | 变形 |
| `arr.T` | `t.T` 或 `t.transpose(0,1)` | 转置 |
| `np.expand_dims(arr, 0)` | `t.unsqueeze(0)` | 增维 |
| `arr[0, :, :]` | `t[0, :, :]` | 切片（完全相同） |

**第二步（45分钟）**：动手写代码（见下方代码块）

**第三步（45分钟）**：重点理解自动求导（Autograd）
- 读官方文档第2节：[Autograd](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html#a-gentle-introduction-to-torch-autograd)
- **关键理解**：推理时为什么要 `torch.no_grad()`？
  - 有 autograd：每次运算都记录"计算图"（浪费内存+时间）
  - 推理只需要前向传播，不需要反向传播，所以关掉

```python
# week1/day4_pytorch_tensor.py
import torch
import numpy as np

print("=" * 50)
print("1. Tensor 创建（对比昨天的 Numpy）")
print("=" * 50)

# 从数据创建
t1 = torch.tensor([1.0, 2.0, 3.0])
print(f"从列表创建: {t1}")

# 随机 Tensor（最常用）
t2 = torch.randn(3, 224, 224)  # 3通道 224×224 图片
print(f"随机图片 shape: {t2.shape}")

# 全零、全一
zeros = torch.zeros(2, 3)
ones  = torch.ones(2, 3)
print(f"Zeros:\n{zeros}")
print(f"Ones:\n{ones}")

print("\n" + "=" * 50)
print("2. Numpy ↔ Tensor 互转（共享内存！）")
print("=" * 50)

arr = np.array([1.0, 2.0, 3.0])
t = torch.from_numpy(arr)         # Numpy → Tensor（共享内存）
print(f"Numpy → Tensor: {t}")

# 修改 Numpy，Tensor 也会变（共享内存的证明）
arr[0] = 100.0
print(f"修改 arr[0] 后，Tensor 也变了: {t}")  # 会变成 100!

t_copy = torch.tensor(arr)        # 深拷贝，不共享内存
arr[0] = 999.0
print(f"深拷贝 Tensor 不受影响: {t_copy}")   # 不会变

print("\n" + "=" * 50)
print("3. 设备迁移（CPU ↔ MPS/CUDA）")
print("=" * 50)

t = torch.randn(2, 3)
print(f"默认设备: {t.device}")

# Mac M系列 GPU
if torch.backends.mps.is_available():
    t_gpu = t.to('mps')
    print(f"MPS GPU 可用，迁移后设备: {t_gpu.device}")
    t_back = t_gpu.to('cpu')
    print(f"迁回 CPU: {t_back.device}")
else:
    print("MPS 不可用（Intel Mac 或无 GPU），使用 CPU 即可")

print("\n" + "=" * 50)
print("4. 自动求导（推理时不需要，但要理解原理）")
print("=" * 50)

# 有梯度跟踪（训练模式）
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1   # y = x² + 3x + 1
y.backward()              # 计算梯度
print(f"y = x² + 3x + 1，x=2 时 dy/dx = {x.grad}")  # 应该是 2*2+3=7

# 推理时关闭梯度（节省内存和时间）
with torch.no_grad():
    x2 = torch.tensor([2.0])
    y2 = x2 ** 2 + 3 * x2 + 1
    print(f"no_grad 模式，y={y2.item():.1f}，没有梯度计算")

print("\n" + "=" * 50)
print("5. 图片前处理流程（复用昨天 Numpy 知识）")
print("=" * 50)

# 模拟一张图片
image_np = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)

# 归一化 + 标准化（完全对应昨天的 Numpy 代码）
image_float = image_np.astype(np.float32) / 255.0
mean = np.array([0.485, 0.456, 0.406])
std  = np.array([0.229, 0.224, 0.225])
normalized = (image_float - mean) / std

# 转成 PyTorch Tensor
# HWC Numpy → CHW Tensor
image_tensor = torch.from_numpy(normalized.transpose(2, 0, 1)).float()
print(f"图片 Tensor shape: {image_tensor.shape}")  # [3, 224, 224]

# 添加 batch 维度
batch = image_tensor.unsqueeze(0)
print(f"带 batch 的 Tensor: {batch.shape}")  # [1, 3, 224, 224]
print("✅ 这就是 ResNet50 的标准输入！明天直接用")

print("\n✅ Day4 完成！")
```

### 15:00-17:00：整理笔记 + 博客提纲

写一份 `week1/notes_day4.md`，用自己的话记录：
- Tensor 和 Numpy 的3个关键区别
- `requires_grad` 的作用
- 图片前处理的5步流程

### 19:00-21:00：预习明天内容

- 快速浏览：[torchvision.models 文档](https://pytorch.org/vision/stable/models.html)
- 找到 ResNet50 的输入/输出格式
- 思考：明天要做什么？（答：加载预训练模型，跑一次推理，打印结果）

**今天的 GitHub commit**：
```bash
git add week1/
git commit -m "W1D4: PyTorch Tensor 系统实践，含自动求导和图片前处理流程"
```

---

## 第五天 · 4月5日（周日）：预训练模型加载 + 推理

> **时间**：早9:00-12:00（项目实战），下午15:00-17:00（总结），晚19:00-21:00（预习W2）
> **主题**：本周最重要的一天！把前4天的知识全部串联起来
> **产出**：一个完整可运行的推理脚本（这是你的第一个 AI 代码）

### 09:00-12:00：预训练模型推理实战

**学习资源（学完就立刻写代码，资源和代码交替）**：

**先读（20分钟）**：
- [PyTorch 官方 - 预训练模型](https://pytorch.org/vision/stable/models.html)
- 重点看：ResNet50 的权重选项、输入要求、输出格式
- torchvision 模型的输入规范：`[N, 3, H, W]`，H/W ≥ 224，像素已归一化

**边读边写（90分钟）**：完整推理脚本

```python
# week1/day5_pretrained_inference.py
"""
第一个完整推理 Demo：加载 ResNet50 预训练模型，对一张图片进行分类
这是后续所有端侧部署的起点！
"""
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import time
import urllib.request
import os

# ============================
# Step 1: 加载预训练模型
# ============================
print("Step 1: 加载 ResNet50 预训练模型...")
start = time.time()

model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()  # 切换到推理模式（关闭 Dropout 和 BatchNorm 的训练行为）

elapsed = (time.time() - start) * 1000
print(f"  加载耗时: {elapsed:.0f}ms")
print(f"  模型参数量: {sum(p.numel() for p in model.parameters()):,} 个")
print(f"  模型大小估计: ~{sum(p.numel() * 4 for p in model.parameters()) / 1e6:.0f} MB（FP32）")

# ============================
# Step 2: 打印模型结构（理解层次）
# ============================
print("\nStep 2: 查看模型结构（前5层）")
for i, (name, module) in enumerate(model.named_children()):
    print(f"  [{i}] {name}: {type(module).__name__}")
    if i >= 4:
        print("  ...")
        break

# ============================
# Step 3: 准备输入数据
# ============================
print("\nStep 3: 准备输入图片...")

# 下载一张测试图片（如果本地没有）
test_image_path = "week1/test_cat.jpg"
if not os.path.exists(test_image_path):
    print("  下载测试图片...")
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/320px-Cat_November_2010-1a.jpg"
    urllib.request.urlretrieve(url, test_image_path)
    print(f"  图片已保存到: {test_image_path}")

# 加载图片
image = Image.open(test_image_path).convert('RGB')
print(f"  原始图片尺寸: {image.size}")

# 定义预处理流程（ImageNet 标准预处理）
transform = transforms.Compose([
    transforms.Resize(256),        # 先缩放短边到 256
    transforms.CenterCrop(224),    # 再裁剪中心 224×224
    transforms.ToTensor(),         # HWC uint8 → CHW float32 [0,1]
    transforms.Normalize(          # ImageNet 标准化
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# 应用预处理
input_tensor = transform(image)           # shape: [3, 224, 224]
input_batch  = input_tensor.unsqueeze(0)  # shape: [1, 3, 224, 224]
print(f"  预处理后 shape: {input_batch.shape}")

# ============================
# Step 4: 执行推理
# ============================
print("\nStep 4: 执行推理...")

with torch.no_grad():  # 推理必须关闭梯度！
    # 计时
    start = time.time()
    output = model(input_batch)
    elapsed_ms = (time.time() - start) * 1000

print(f"  推理耗时: {elapsed_ms:.1f}ms")
print(f"  输出 shape: {output.shape}")  # [1, 1000]

# ============================
# Step 5: 解析输出（Top-5 分类结果）
# ============================
print("\nStep 5: 解析分类结果（Top-5）")

# Softmax 转成概率
probabilities = torch.nn.functional.softmax(output[0], dim=0)

# 下载 ImageNet 类别标签
labels_path = "week1/imagenet_classes.txt"
if not os.path.exists(labels_path):
    print("  下载 ImageNet 标签...")
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    urllib.request.urlretrieve(url, labels_path)

with open(labels_path) as f:
    categories = [line.strip() for line in f.readlines()]

# Top-5 结果
top5_prob, top5_catid = torch.topk(probabilities, 5)

print("\n  分类结果：")
for i in range(top5_prob.size(0)):
    category = categories[top5_catid[i]]
    prob = top5_prob[i].item()
    bar = "█" * int(prob * 30)
    print(f"  {i+1}. {category:30s} | {prob:.4f} | {bar}")

# ============================
# Step 6: 记录性能数据（重要！）
# ============================
print("\n" + "=" * 50)
print("性能数据汇总（面试时可以提到）")
print("=" * 50)
print(f"  设备: CPU (MacBook)")
print(f"  模型: ResNet50（FP32）")
print(f"  输入: 1×3×224×224")
print(f"  模型参数: 25.6M")
print(f"  推理延迟: {elapsed_ms:.1f}ms")
print(f"  （这个数据是你真实测到的，记住它！）")
print("\n✅ 第一个完整推理 Demo 完成！")
```

### 15:00-17:00：深入理解 + 整理笔记

**读这篇（30分钟）**：[《动手学深度学习》3.1 线性回归原理](https://zh.d2l.ai/chapter_linear-networks/linear-regression.html)
- 不需要跑代码，只是理解：为什么要有 softmax？输出的 1000 个数字代表什么？

**整理 `week1/notes_week1.md`**（参考格式）：
```markdown
# W1 学习总结

## 核心概念图谱
PyTorch Tensor
  ├── 类似 Numpy array，但可以 GPU 计算 + 自动求导
  ├── 推理时必须 torch.no_grad()（关掉梯度计算）
  └── 与 Numpy 可以互转（from_numpy / tensor.numpy()）

## 图片推理完整流程
图片文件 → PIL.Image.open → transforms.Resize/CenterCrop/ToTensor/Normalize
         → [1, 3, 224, 224] Tensor → model(input) → [1, 1000] → softmax → Top-5

## 我的第一次性能数据
- ResNet50 FP32 on CPU：____ ms

## 遇到的问题和解决方式
- 问题1：...
- 解决：...

## 明天（W2）要做什么
ONNX：把今天的 PyTorch 模型导出成 .onnx 文件，实现跨框架部署
```

### 19:00-21:00：预习 W2

- 读 5 分钟：[ONNX 官网首页](https://onnx.ai/onnx/intro/)，了解"为什么需要 ONNX"
- 思考：今天跑通了 PyTorch 推理，但 PyTorch 模型只能在 Python 里跑。怎么在 Android C++ 里跑？→ 这就是 W2 要解决的问题

**今天的 GitHub commit**：
```bash
git add week1/
git commit -m "W1D5: ResNet50 预训练模型推理完整 Demo，含性能计时和 Top-5 输出"
```

---

## 第六天 · 4月6日（周一）：复盘 + 写技术博客

> **时间**：早7:00-8:00（写博客），晚21:00-22:00（GitHub 整理）
> **主题**：输出是最好的学习检验。不写博客，等于没学

### 早上 7:00-8:00：写博客草稿

**博客标题**：`移动端工程师的 PyTorch 第一周：我踩了哪些坑`

**博客结构（600-800字，发掘金/知乎）**：

```
1. 我的背景（2句话）
   - 15年移动端开发，想转端侧AI

2. 这周我学了什么（用具体代码展示，不要干说）
   - PyTorch Tensor 和 Numpy 有多像（代码对比表）
   - 为什么推理时要 torch.no_grad()（原理解释）
   - 图片前处理的5个步骤（代码）

3. 我的第一个推理结果（截图/数据）
   - ResNet50 识别出了什么
   - 推理耗时 xxms

4. 移动端工程师的优势感受
   - 理解内存布局让我更容易理解 CHW 格式
   - 多线程经验让我理解为什么推理不能在主线程

5. 下周预告（吸引订阅）
   - 把 PyTorch 模型导出成 ONNX，实现跨框架部署
```

**发布到**：掘金（https://juejin.cn）或知乎

### 晚上 21:00-22:00：GitHub 整理

整理 GitHub 仓库，确保结构清晰：

```
on-device-ai-journey/
├── README.md          # 项目介绍 + 学习进度
├── week1/
│   ├── README.md      # W1 总结 + 性能数据
│   ├── day2_python_review.py
│   ├── day3_numpy_practice.py
│   ├── day4_pytorch_tensor.py
│   ├── day5_pretrained_inference.py
│   └── notes_week1.md
└── .gitignore         # 排除 __pycache__, *.pyc, *.jpg 等
```

**W1 最终 commit**：
```bash
git add .
git commit -m "W1 完成：Python/Numpy/PyTorch 基础 + ResNet50 推理 Demo + 技术博客发布"
git push origin main
```

---

## W1 自检清单（周一完成后对照）

完成打勾，未完成标注"待补"，不强求100%：

| 项目 | 状态 |
|------|------|
| Conda 环境搭建，`import torch` 成功 | [ ] |
| 能解释 Tensor 和 Numpy 的区别（内存共享、设备、梯度） | [ ] |
| 理解推导式、装饰器、Context Manager | [ ] |
| 能写出图片前处理的完整流程（5步） | [ ] |
| 能解释为什么推理要 `torch.no_grad()` | [ ] |
| ResNet50 推理 Demo 跑通，有 Top-5 结果 | [ ] |
| 记录了真实推理耗时数据 | [ ] |
| GitHub 仓库已建立，有代码 commit | [ ] |
| 技术博客草稿已写（可以还没发） | [ ] |

**及格线**：完成7项以上 → 继续 W2
**优秀线**：完成9项 + 博客已发布 → 你的进度比预期好

---

## W1 → W2 连贯性说明

本周学的内容与下周的直接关联：

| 本周（W1）产出 | 下周（W2）用途 |
|---------------|---------------|
| `model = resnet50(weights=...)` 加载模型 | W2 直接导出这个模型为 ONNX |
| 理解 input_batch 的 shape `[1,3,224,224]` | W2 导出时需要指定 `dummy_input` |
| `model.eval()` + `torch.no_grad()` | W2 ONNX Runtime 推理也需要同样的前处理 |
| 记录的推理时延（PyTorch CPU） | W2 与 ONNX Runtime 做对比 |

**W2 的关键问题**：今天的模型只能在 Python/PyTorch 环境里跑，Android C++ 怎么用？
→ 答案：先导出成 ONNX 格式，再用 ONNX Runtime C++ API 加载推理。

---

*计划制定：2026年3月26日*
*执行周期：2026年4月1日 - 4月6日*
*配套文档：最终版_端侧AI工程师_3个月冲刺计划_v3.0_优化版.md*
