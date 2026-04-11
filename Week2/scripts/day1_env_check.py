# import onnx
# import onnxruntime as ort

# print(f"onnx version: {onnx.__version__}")
# print(f"onnxruntime version: {ort.__version__}")
# print("OK Success Install")

import torch
import torchvision.models as models

print("验证 W1 环境...")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)
with torch.no_grad():
    output = model(dummy_input)

print(f"ResNet50 输出 shape: {output.shape}")
print("OK W环境正常 可以开始W2")
