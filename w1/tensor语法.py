import torch
import numpy as np
from torch.cpu import is_available

print("=" * 50)
print("1. Tensor 创建（对比昨天的 Numpy）")
print("=" * 50)

# 从数据创建
a = torch.tensor([1, 2, 3], dtype=torch.float16)
print(f"从数据创建 tensor：{a}")

# 随机tensor
b = torch.randn(1, 2, 224, 224)
print(f"随机图片tensor: {b}")

#全零 全1
c = torch.zeros(2, 4)
e = torch.ones(3, 4)
print(f"全零：{c} \n 全1：{e}")

f = np.array([1, 2, 3])
g = torch.from_numpy(f)
print(f"f->g: {g}")

# 修改np，tensor也会变，共享内存的证明
f[0] = 100
print(f"g: {g}")

# 深copy，不共享内存
h = torch.tensor(f)
f[0] = 200
print(f"f: {f}")
print(f"h: {h}")

print("\n" + "=" * 50)
print("3. 设备迁移（CPU ↔ MPS/CUDA）")
print("=" * 50)

t = torch.randn(2, 3)
print(f"默认设备: {t.device}")

if torch.backends.mps.is_available():
    # 这行代码的意思是：如果设备支持苹果的MPS（苹果芯片的GPU加速），
    # 就把原本在CPU上的Tensor t迁移到MPS设备（即Apple GPU）上进行计算，提升运算速度。
    t_gpu = t.to('mps')
    print(f"MPS GPU可用，迁移后设备：{t_gpu.device}")
else:
    print("MPS不可用（Inter Mac 或无GPU）， 使用CPU即可")


print("\n" + "=" * 50)
print("4. 自动求导（推理时不需要，但要理解原理）")
print("=" * 50)

# 创建一个可计算梯度的 tensor x，并赋值为 2.0
x = torch.tensor([2.0], requires_grad=True)

# 定义一个关于 x 的函数 y = x^2 + 3x + 1
y = x ** 2 + 3 * x + 1

# 反向传播，计算 y 关于 x 的梯度。即：dy/dx
y.backward()

# 输出当 x=2 时，y 对 x 的导数；即 dy/dx 的值（存储在 x.grad 中）
print(f"当x=2时，dy/dx = {x.grad}")


# 下面这段代码演示了 torch.no_grad() 的作用：
# 在 with torch.no_grad() 代码块内，所有Tensor的运算都不会被自动求导引擎记录，也不会构建计算图，因此不会产生梯度。
# 这种模式主要用于：模型推理或验证阶段，只需前向推理、不需要反向传播/梯度，节省内存和加速推理。
with torch.no_grad():
    x2 = torch.tensor([2.0])  # 创建不需要梯度的Tensor
    # 计算 y2 = 2*x2 + 3*x2 + 1，这里不会记录梯度信息
    y2 = 2 * x2 + 3 * x2 + 1
    # y2 是一个单元素张量（tensor），用 .item() 方法可以取出其数值（Python float），格式化为一位小数后输出
    print(f"no_grad模式，y = {y2.item():.1f} （y2.item() 取出 float 数值，:.1f 保留一位小数），没有梯度计算")


print("\n" + "=" * 50)
print("5. 图片前处理流程（复用昨天 Numpy 知识）")
print("=" * 50)

# 生成一个 224x224 的“随机图片”，每个像素有3个通道（RGB），数值范围0~255，模拟真实的8位无符号整型图片数据（和OpenCV读取的图片格式一样）。
image_np = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
print(f"image_np_shape: {image_np.shape}")

# 归一化 + 标准化
# 将原始图片（image_np）转换为32位浮点型，便于后续的数值计算
image_float = image_np.astype(np.float32)

# 定义每个通道（R, G, B）的均值和标准差
# 这些参数是基于 ImageNet 数据集的预训练模型预处理方式
mean = np.array([0.485, 0.456, 0.406])  # R通道均值、G通道均值、B通道均值
std = np.array([0.229, 0.224, 0.225])   # R通道标准差、G通道标准差、B通道标准差

# 对图片进行归一化和标准化处理
# 注意：减均值/除标准差时，numpy 会自动按通道广播
# 归一化：把像素值缩放到0-1区间（通常前一步会有 /255；这里为简单起见省略）
# 标准化：让每个通道的数据分布更适合深度学习模型，提高收敛能力
normalized = (image_float - mean) / std

image_tensor = torch.from_numpy(normalized.transpose(2, 0, 1)).float()
print(f"iamge_tensor shape: {image_tensor.shape}")

#添加batch维度
batch = image_tensor.unsqueeze(0)
print(f"iamge_tensor_batch: {batch.shape}")

