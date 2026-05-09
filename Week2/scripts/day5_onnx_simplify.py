import onnx
from onnxsim import simplify
import time
import os

onnx_path = 'resnet50_dynamic_batch.onnx'
simplified_path = 'resnet50_simplified.onnx'

print('加载原始模型...')
model = onnx.load(onnx_path)
original_nodes = len(model.graph.node)
print(f'原始节点数: {original_nodes}')

print('执行 onnx-simplifier 图优化...')
start = time.time()
model_simplified, check = simplify(model)
elapsed = (time.time() - start) * 1000

if check:
    print(f'简化成功！ 耗时 {elapsed:.0f} ms')
else:
    print('简化失败')
    model_simplified = model

simplified_nodes = len(model_simplified.graph.node)
reduction = original_nodes - simplified_nodes
print(f'简化后的节点数：{simplified_nodes}, 减少了: {reduction} 个, 降低 {reduction/original_nodes *100:.1f} %')

onnx.save(model_simplified, simplified_path, save_as_external_data=True, all_tensors_to_one_file=True, location='resnet50_simplified.onnx.data')
print(f"简化后的模型存储在: {simplified_path}")

original_size = os.path.getsize(onnx_path) / 1e6
simplified_size = os.path.getsize(simplified_path) / 1e6

print(f'原始模型大小：{original_size:.5f} MB, 简化后的模型大小: {simplified_size:.5f} MB')
print("OK day5 完成")

