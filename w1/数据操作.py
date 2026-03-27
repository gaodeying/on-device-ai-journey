import torch
import numpy as np

# 创建张量
t = torch.randn(2, 3)
print("Tensor: ", t)
print("Tensor shape: ", t.shape)
print("Tensor dtype: ", t.dtype)

# tensor -> numpy
arr = t.numpy()
print("numpy array: ", arr)

# numpy -> tensor
t = torch.from_numpy(arr)
print("back to tensor: ", t)