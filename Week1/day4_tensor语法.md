# Tensor 与 NumPy 入门笔记

本文与 `w1/tensor语法.py` 配套，便于复习与查阅。

---

## 一、Tensor 和 NumPy 的三个关键区别

总览表：

| 维度 | NumPy | PyTorch Tensor |
|------|--------|----------------|
| **设备** | 主要在 CPU | 可放到 `cpu` / `cuda` / `mps` 等，便于 GPU 加速 |
| **自动求导** | 无计算图、无 `.grad` | `requires_grad=True` + `backward()` 可自动求梯度 |
| **生态与用途** | 通用科学计算、数据分析 | 与 `nn`、`optim`、训练/部署流水线天然衔接 |

一句话：**NumPy 像「纯数值数组」；Tensor 像「能上 GPU、能记梯度、能接模型」的数组。**

下面把这三点拆开讲透。

### 1. 设备（CPU / GPU / MPS）

- **NumPy**：数组常驻 **CPU**。没有「这张表在显卡上」的一等公民概念；若要用 GPU，通常要换别的库或把数据交给框架。
- **Tensor**：每个张量有 **`device` 属性**，可显式迁移：
  - `x.to("cuda")`：NVIDIA GPU（需 CUDA 可用）
  - `x.to("mps")`：Apple Silicon 的 Metal（`torch.backends.mps.is_available()`）
  - `x.cpu()`：回到 CPU
- **为什么要关心设备**：矩阵一大，CPU 算得慢；训练时参数、输入、中间结果最好在 **同一设备**，否则常见报错是 device mismatch。
- **和 NumPy 的衔接**：`torch.from_numpy(np_arr)` 得到的一般是 **CPU Tensor**；要上 GPU 需再 `.to(...)`。GPU 上的 Tensor **不能**再和 NumPy 共享同一块内存（需 `.cpu().numpy()` 拉回 CPU 再转，注意是否脱离计算图）。

### 2. 自动求导（计算图与梯度）

- **NumPy**：`y = f(x)` 只算数值，**不记录**「y 是怎么由 x 算出来的」，因此无法对任意 `f` 自动求 \(\partial y/\partial x\)。
- **Tensor**：
  - **`requires_grad=True`**：告诉 autograd 跟踪运算，构建 **有向无环图（DAG）**。
  - **`loss.backward()`**：从标量 `loss` 往回传，把梯度累加到叶子张量的 **`.grad`**。
  - **`torch.no_grad()`**：推理时常用，**不建图、不占梯度内存**，更快。
- **常见配套概念**（便于和 NumPy 对比）：
  - **叶子节点 / 非叶子**：参数一般是叶子；中间激活值往往带 `grad_fn`。
  - **梯度累加**：多次 `backward` 默认 **加到** `.grad`，训练循环里常配合 **`optimizer.zero_grad()`**。
  - **原地操作**（如 `x += 1`）：有时破坏求导，初学者尽量用 **`x = x + 1`** 等非原地写法更省心。
- **一句话**：NumPy 算「数」；Tensor 在需要时还能算「数对参数的敏感度」（梯度），这是反向传播的基础。

### 3. 生态与用途（为什么深度学习首选 Tensor）

- **NumPy**：强项是 **离线数据处理、统计、和 C/Fortran 生态互操作**；几乎任何 Python 科学栈都认它。
- **Tensor**：
  - **`nn.Module`** 里参数和 buffer 都是 Tensor；**`optim`** 直接消费 `model.parameters()`。
  - **保存/加载**：`state_dict`、TorchScript、ONNX 等链路围绕 Tensor 设计。
  - **与 NumPy 互转**：`numpy()` / `from_numpy()` / `torch.as_tensor()`，便于预处理在 NumPy、训练在 PyTorch。
- **API 相似性**：很多函数名和直觉接近 NumPy（如 `mean`、`permute` 对应 `transpose` 思想），降低迁移成本；但 **语义不完全相同**（例如维度命名、是否就地、是否记录梯度），要以 PyTorch 文档为准。

### 小结对照（记这三条就够）

1. **要不要上 GPU** → Tensor 有 `device`，NumPy 默认没有这套。
2. **要不要训练（求梯度）** → Tensor + autograd；NumPy 需自己手写导数或换框架。
3. **是不是在模型/优化器里流转** → 用 Tensor；纯数据分析仍常先用 NumPy。

---

## 二、Tensor 常见创建方式（对应脚本第 1 节）

- **`torch.tensor(data, dtype=...)`**：从 Python 列表或数组创建，可指定精度（如 `float16`）。
- **`torch.randn(1, 2, 224, 224)`**：标准正态随机数，常用于模拟 `(N, C, H, W)` 图像 batch。
- **`torch.zeros` / `torch.ones`**：全 0 / 全 1。
- **`torch.from_numpy(ndarray)`**：与 NumPy **共享内存**；改 `ndarray` 会反映到 Tensor 上。
- **`torch.tensor(ndarray)`**：一般会 **拷贝**，不共享内存。

---

## 三、设备迁移（对应脚本第 3 节）

- 默认 Tensor 在 **CPU**，`tensor.device` 可查看。
- **`tensor.to('mps')`**：在 Apple Silicon 上可用时，把数据迁到 **MPS（Apple GPU）**。
- **`tensor.to('cuda')`**：在 NVIDIA GPU 可用时使用 CUDA。

迁移后参与运算的两个 Tensor 一般要在 **同一设备** 上。

---

## 四、自动求导与 `no_grad`（对应脚本第 4 节）

1. **`requires_grad=True`**：标记需要对该张量求导，运算会记入计算图。
2. **标量**才能直接 **`loss.backward()`**；若为多元素，需 `.sum()` 或传入 `gradient`。
3. **`x.grad`**：存储对 `x` 的梯度（偏导）。
4. **`torch.no_grad()`**：块内不建图、不求导，**推理/验证**时常用，省内存、略快。

---

## 五、`requires_grad` 的作用（详解）

**一句话**：`requires_grad` 决定这张量上的运算要不要被 autograd **记录进计算图**；只有被记录的路径，才能在 `loss.backward()` 时把梯度往回传。

### 设为 `True` 时会发生什么

- PyTorch 会跟踪「这个张量参与了哪些运算」，形成 **DAG（计算图）**。
- 前向时不仅算数值，还为反向保存必要信息。
- 对最终标量 `loss` 调用 **`backward()`** 后，梯度会累加到相关叶子张量的 **`.grad`**（如可学习参数）。

### 设为 `False` 或不设置（默认 `False`）时

- 不建图（对该张量而言），**省内存、更快**，适合纯数据、标签、推理中间结果等不需要对「输入」求导的场景。

### 结果张量会不会需要梯度？（传播规则）

- 若某个运算的**任意输入** `requires_grad=True`，且不在 `torch.no_grad()` 里，则**输出**通常是 **`requires_grad=True`**（表示「这条链路可继续反传」）。
- 模型 **`nn.Parameter`** 默认 `requires_grad=True`，所以训练时参数会更新；微调里可对部分层 `param.requires_grad_(False)` **冻结**。

### 常见用法对照

| 场景 | 建议 |
|------|------|
| 可训练权重 / 你希望求导的变量 | `requires_grad=True` |
| 训练数据、标签、常量 | 默认 `False` 即可 |
| 整段只做推理 | `with torch.no_grad():` 包起来，内部运算不建图 |
| 冻结某层参数 | `for p in layer.parameters(): p.requires_grad_(False)` |

### 易混点

- **`requires_grad` 只控制「是否跟踪」**；真正更新参数还要 **`optimizer.step()`**，且训练循环里通常每步 **`optimizer.zero_grad()`** 清掉上轮梯度。
- 标量 `loss` 才能直接 `backward()`；若 `loss` 是多元素张量，需 `.sum()` 或传入 `gradient` 参数（见官方 autograd 教程）。

---

## 六、图片前处理五步流程（`H,W,C` → `N,C,H,W`）

与 `w1/tensor语法.py` 第 5 节一致。目标：把「像素图」变成模型常吃的 **`(N, C, H, W)`** 浮点 Tensor（batch × 通道 × 高 × 宽）。

| 步骤 | 做什么 | 目的（通俗） | 典型形状 / 操作 |
|:----:|--------|--------------|-----------------|
| **1** | 得到图像数组 | 读文件或模拟数据，保持常见内存布局 | **`(H, W, C)`**，如 `uint8`，取值常 `0~255`；脚本里用 `np.random.randint(..., (224,224,3), dtype=np.uint8)` |
| **2** | 转浮点 + 缩放到 `[0,1]` | 把整数像素变成适合矩阵运算的浮点，并把亮度归一 | `image.astype(np.float32)`，再 **`image_float = image / 255.0`**（脚本为简化有时省略 `/255`，**真实推理建议不要省**） |
| **3** | 按通道标准化 | 减均值除标准差，让分布接近预训练模型训练时的分布 | `(image_float - mean) / std`，`mean/std` 各 `(3,)`，与 ImageNet 预训练常配套 |
| **4** | **HWC → CHW** 并转成 Tensor | PyTorch 卷积默认按 **通道在前** | `normalized.transpose(2, 0, 1)` 得 **`(C, H, W)`**，再 `torch.from_numpy(...).float()` |
| **5** | 加 **batch 维** | 模型输入要「一批图」，即使只有一张也要 `N=1` | **`unsqueeze(0)`** → **`(1, C, H, W)`**，即 `NCHW` |

### 口诀（背这五步）

**读图 HWC → 除 255 → 减均值除方差 → 转 CHW 进 Torch → 前面加个 N。**

### 与 ResNet 等预训练模型的关系

- 第 3 步的 `mean/std` 要与**权重来源**一致（例如 ImageNet 预训练就用教程里那组数）。
- 若某模型文档要求 **BGR**、固定 `resize`、`center crop` 等，需在上述流程前后补上；五步是「核心数值管线」骨架。

---

## 七、相关文件

| 文件 | 说明 |
|------|------|
| `w1/tensor语法.py` | 可运行示例（创建、设备、autograd、图像预处理） |
| `w1/autograd_min_demo.py` | 更小的 autograd 演示 |
| `w1/AutoGrad.py` | ResNet18 + 前向/反向/优化器流程骨架 |

---

## 八、脚本里的小笔误（可选修正）

- `tensor语法.py` 中打印字符串写成了 `iamge_tensor`，若需与变量名一致可改为 `image_tensor`。
