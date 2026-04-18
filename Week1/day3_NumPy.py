import numpy as np

# a = np.arange(15).reshape(3, 5)

# print(f'a: {a}')

# print(f'a.ndim: {a.ndim}')

# print(f'a.itemsize: {a.itemsize}')

# a = np.arange(10)**3
# print(f"a arange: {a}")

# a[:6:2] = 1000
# print(f"a [:6:2]: {a}")

# a[::-1]
# print(f"a -1: {a}")

# def f(x, y):
#     return 10*x + y
# b = np.fromfunction(f, (5, 4), dtype=int)
# print(f"b:\n {b}")

# for row in b:
#     print(f"row: {row}")

# for i in b.flat:
#     print(f"i_flat: {i}")

# rg = np.random.default_rng(42)
# print(f"rg: {rg}")
# b = rg.random((3, 4))
# print(f"b: {b}")
# a = np.floor(10 * rg.random((3, 4)))
# print(f"a: {a}")

# c = np.arange(0, 10, 1)
# print(f"c: {c}")

# import torch

# x = torch.arange(12)
# print(x)

# print(x.shape)

# a = torch.randn(3, 4)
# print(a)

# torch.exp(a)

# X = torch.arange(12, dtype=torch.float32).reshape((3,4))
# Y = torch.tensor([[2.0, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
# before = id(Y)
# Y[:] = X + Y
# after = id(Y)
# print(f"before: {before}, after: {after}")


import numpy as np
from sympy import im
print("=" *40)
print("1. 基础操作")
print("="*40)

# 创建数组（对应图片的形状理解）
# 一张 224×224 RGB 图片 = shape (224, 224, 3)
image = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
print(f"image shape: {image.shape}")
print(f"dataType: {image.dtype}")

# resize 操作（手工实现缩放理解）
# 实际工程用 PIL 或 cv2，但理解这个操作很重要
h, w = image.shape[:2]
print(f"原始尺寸：{w} * {h}")

print("\n" + "=" * 40)
print("2. 核心操作：切片和索引")
print("=" * 40)

# 提取第一个颜色通道（R通道）
r_channel = image[:, :, 0]
print(f"r通道shape: {r_channel.shape}")

patch = image[:32, :32, :]
print(f"图片 patch shape: {patch.shape}")

print("\n" + "=" * 40)
print("3. 关键操作：归一化（AI推理必用）")
print("=" * 40)

print(f"归一化之前的dataType: {image.dtype}")
image_float = image.astype(np.float32) / 255.0
print(f"归一化之后的dataType: {image_float.dtype}")


# ImageNet 标准化（均值/标准差，ResNet 推理必用）
mean = np.array([0.485, 0.456, 0.406])   # ImageNet 均值
std  = np.array([0.229, 0.224, 0.225])   # ImageNet 标准差
# 广播：mean shape (3,) 与 image_float shape (224, 224, 3) 自动对齐
normalized = (image_float - mean) / std
print(f"标准化后均值： {normalized.mean(axis=(0,1))}")


print("\n" + "=" * 40)
print("4. 关键操作：维度变换（HWC → CHW）")
print("=" * 40)

# PyTorch 需要 CHW 格式（通道×高×宽），OpenCV 是 HWC 格式
# 这个转换在实际推理前处理中必须做
image_chw = np.transpose(normalized, (2, 0, 1))
print(f"HWC -> CHW: {normalized.shape} -> {image_chw.shape}")

# 添加 batch 维度（模型需要 NCHW = batch × channel × height × width）
image_batch = np.expand_dims(image_chw, 0)
print(f"添加batch维度： {image_chw.shape} -> {image_batch.shape}")
print(f"最终输入 shape: {image_batch.shape}  ← 这就是 ResNet50 的标准输入格式！")

print("\n" + "=" * 40)
print("5. Numpy ↔ 矩阵运算")
print("=" * 40)


A = np.array([[1, 2], [3, 4]], dtype=np.float32)
B = np.array([[5, 6], [7, 8]], dtype=np.float32)

print(f"矩阵乘法 A@B：\n {A@B}")
print(f"点积 np.dot: \n {np.dot(A, B)}")
print(f"转置：\n {A.T}")
print(f"逐元素乘：\n {A * B}")