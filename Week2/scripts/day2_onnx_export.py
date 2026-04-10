##################################
# 把 W1 的ResNet50 模型导出成 ONNX 格式
##################################

import torch
import torchvision.models as models
import onnx
import os

print("="*50)
print(" Step 1: load Pytorch model")
print("="*50)

model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
# 将模型切换为推理/评估模式，关闭 dropout、BN 的训练行为，保证导出 ONNX 时行为和推理一致
model.eval()

print("="*50)
print(" Step 2: prepare dummy input")
print("="*50)

dummy_input = torch.randn(1, 3, 224, 224)
print(f"dummy_input 是 {dummy_input.ndim} 维数组")  # 这是几维数组
print(f" dummy_input shape: {dummy_input.shape}")

print("="*50)
print(" Step 3: export oonnx (fixed batch)")
print("="*50)

output_path_fixed = "resnet50_fixed_batch.onnx"
torch.onnx.export(
    model,
    dummy_input, 
    output_path_fixed,
    input_names=["input"],
    output_names=["output"],
    opset_version=18,
    verbose= False
)
print(f"fixed batch doc size: {os.path.getsize(output_path_fixed) / 1e6:.1f} MB")

print("="*50)
print(" Step 4: export oonnx (dynamic batch)")
print("="*50)

output_path_dynamic = "resnet50_dynamic_batch.onnx"
# 动态 batch vs 静态 batch 区别说明：
# 静态 batch（前面导出的 fixed_batch）导出的模型只支持 batch size=1，推理时输入 shape 必须也是 [1, 3, 224, 224]；
# 动态 batch 模型则可支持任意 batch size（比如 [8, 3, 224, 224]），更灵活。
# 关键在于 dynamic_axes 参数，把第 0 维（即 batch 维）设置为动态：
torch.onnx.export(
    model,
    dummy_input,
    output_path_dynamic,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={
        "input": {0: "batch_size"},   # input 第 0 维可变
        "output": {0: "batch_size"}   # output 第 0 维可变
    },
    opset_version=18,
    verbose=False
)
print(f"动态 batch 文件大小： {os.path.getsize(output_path_dynamic)/1e6:.1f} MB")

print("="*50)
print(" Step 5: check onnx model ok")
print("="*50)

model_onnx = onnx.load(output_path_dynamic)
onnx.checker.check_model(model_onnx)
print("Ok onnx is ok")
print(f" opset version: {model_onnx.opset_import[0].version}")
# 为什么这里是124？
# 这是导出后的ONNX模型中graph.node的数量，即算子节点数。
# 每当模型中的某一层（如卷积、BN、ReLU、Add等）被转换为ONNX格式时，
# 都会增加一个node到graph.node列表，因此最终数量取决于模型结构+opset+ONNX export策略等。
# 你可以直接打印所有节点类型、统计不同类型节点数量确认：
from collections import Counter
node_types = [n.op_type for n in model_onnx.graph.node]
print(f"node num: {len(node_types)}")
print(f"各类型节点数量: {Counter(node_types)}")