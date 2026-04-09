import torch

# 这个最小示例用来理解 autograd 的 4 个关键动作：
# 1) 声明可求导参数 -> 2) 前向计算 loss -> 3) backward 求梯度 -> 4) no_grad 推理

# 1) 创建需要求导的张量（参数）
# requires_grad=True 表示：后续涉及该张量的运算要被 autograd 记录到计算图里。
x = torch.tensor([2.0, 3.0], requires_grad=True)
y = torch.tensor([4.0, 5.0], requires_grad=True)

# 2) 前向计算：定义一个“损失”标量
# z = x^2 + 3y，loss = z 所有元素求和
# 这里故意用简单公式，方便你手算验证梯度：
# dloss/dx = 2x, dloss/dy = 3
z = x**2 + 3 * y
loss = z.sum()

print("===== 1) 参数与前向结果 =====")
print(f"x: {x}")
print(f"y: {y}")
print(f"z: {z}")
print(f"loss: {loss}")

# 3) 反向传播：自动计算 loss 对 x/y 的梯度
# 调用 backward 后，梯度会写入 x.grad / y.grad
loss.backward()

print("\n===== 2) backward 后的梯度 =====")
print(f"x.grad: {x.grad}")  # 理论上是 2x -> [4, 6]
print(f"y.grad: {y.grad}")  # 理论上是 3  -> [3, 3]
print(f"手算校验 dloss/dx=2x: {2 * x.detach()}")
print(f"手算校验 dloss/dy=3:  {torch.full_like(y.detach(), 3.0)}")

# 额外说明：梯度默认会“累加”到 .grad 中。
# 在真实训练循环里，每轮反向前通常先执行 optimizer.zero_grad()。

# 4) 推理阶段常用 no_grad()：不建图、更省内存
# no_grad 内部的计算不会被记录到计算图，也就不会产生梯度。
with torch.no_grad():
    pred = x * 10 + y
    print("\n===== 3) no_grad 推理 =====")
    print(f"no_grad 下的 pred: {pred}")
