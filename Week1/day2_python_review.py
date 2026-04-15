# ============ 推导式 ============
# 应用：遍历模型层。 找出含有 conv 的layer
layers = ['conv1', 'bn1', 'relu', 'conv2', 'fc']
conditionLayer = []
for l in layers:
    if 'con' in l:
        conditionLayer.append(l)
print('conditionLayer: ', conditionLayer)

conditionLayer2 = [l for l in layers if 'con' in l]
print('conditionLayer2: ', conditionLayer2)
print(f'conditionLayer2 {conditionLayer2}')


# ============ 装饰器 ============
# 计算函数执行时间
import time

def conculateTime(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time()
        duration = t2 -t1
        return duration
    return wrapper

@conculateTime
def fakeLargeFunction():
    time.sleep(2)

duration = fakeLargeFunction()
print(f'duratoin time: {duration}')

# ============ Context Manager ============
import torch

with torch.no_grad():
    x = torch.randn(1, 3, 224, 224)
    print(f"输入 shape: {x.shape}")
    print(f"内存效率更高，梯度不会被计算")
print("day 2 done")