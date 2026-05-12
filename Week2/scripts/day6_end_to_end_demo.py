"""
w2 核心产出：完整的端到端推理 Demo
PyTorch 模型 -》 ONNX 导出 -》 ONNX Runtime 推理 -》 Top5 结果展示
"""

from pathlib import Path
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import onnxruntime as ort
import numpy as np
import json
import os
import urllib.request
import time

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IMAGE_PATH = PROJECT_ROOT / "Week2/scripts/banana1.jpg"
ONNX_PATH = PROJECT_ROOT / "Week2/resnet50_dynamic_batch.onnx"
LABELS_PATH = PROJECT_ROOT / "Week2/imagenet_labels.json"


def download_imagenet_labels(save_path=LABELS_PATH):
    """下载并缓存 ImageNet 1000 类标签。"""
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    if save_path.exists():
        with open(save_path, encoding="utf-8") as f:
            return json.load(f)
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    print("下载 ImageNet 标签...")
    urllib.request.urlretrieve(url, save_path)
    with open(save_path, encoding="utf-8") as f:
        return json.load(f)


def preprocess_image(image_path, image_size=224):
    """
    预处理输入图片，产出 NCHW 格式张量:
    - Resize(256) + CenterCrop(224): 对齐 ResNet 常见验证集预处理
    - Normalize: 对齐 ImageNet 训练时的数据分布
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    img = Image.open(image_path).convert("RGB")
    return transform(img).unsqueeze(0)


def export_model_if_needed(model, onnx_path):
    """若 ONNX 不存在则导出；存在则直接复用。"""
    onnx_path = Path(onnx_path)
    onnx_path.parent.mkdir(parents=True, exist_ok=True)

    if onnx_path.exists():
        print(f" ONNX 文件已存在： {onnx_path}")
        return

    print(" 导出 ONNX 模型...")
    dummy = torch.randn(1, 3, 224, 224)
    torch.onnx.export(
        model, dummy, str(onnx_path),
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"},
        "output": {0: "batch_size"}},
        opset_version=18
    )
    print(f" OK 导出完成：{onnx_path}")


def show_top5(logits, labels):
    """
    展示 Top-5 分类结果。
    logits 是模型原始分数，先过 softmax 再看概率更直观。
    """
    # 数值稳定版 softmax，避免 exp(大数) 溢出。
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exp_scores = np.exp(shifted)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

    # 先升序排序，取最后 5 个，再反转成从大到小。
    top5_idx = np.argsort(probs[0])[-5:][::-1]
    print("\n Top-5 预测结果：")
    for rank, idx in enumerate(top5_idx, 1):
        label = labels[idx] if idx < len(labels) else f"class_{idx}"
        print(f" #{rank}: {label:30s} ({probs[0][idx]*100:0.2f}%)")


def main():
    print("=" * 60)
    print("W2 端到端 Demo: PyTorch -> ONNX -> ORT推理")
    print("=" * 60)

    # 1. 准备测试图片（不存在时用随机输入，便于验证链路可运行）
    test_image_path = DEFAULT_IMAGE_PATH
    if not test_image_path.exists():
        print("\n[提示] 没有找到测试图片， 使用随机 Tensor 代替")
        input_np = np.random.randn(1, 3, 224, 224).astype(np.float32)
    else:
        print(f"\n 使用测试图片： {test_image_path}")
        input_tensor = preprocess_image(test_image_path)
        input_np = input_tensor.numpy()
    
    # 2. 加载 PyTorch 模型并导出 ONNX
    print("\n [Step 1] 加载 PyTorch 模型...")
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    # eval 模式会关闭 dropout，并让 batchnorm 使用统计量，保证推理稳定。
    model.eval()

    onnx_path = ONNX_PATH
    export_model_if_needed(model, onnx_path)

    # 3. 创建 ONNX Runtime Session
    print("\n [Step 2] 创建 ONNX Runtime Session...")
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    ort_session = ort.InferenceSession(str(onnx_path), sess_options=sess_options)
    print(f" 输入节点：{ort_session.get_inputs()[0].name}, shape: {ort_session.get_inputs()[0].shape}")
    print(f" 输出节点：{ort_session.get_outputs()[0].name}, shape: {ort_session.get_outputs()[0].shape}")

    # 4. 执行推理
    print("\n [Step 3] 执行推理...")
    input_name = ort_session.get_inputs()[0].name
    output_name = ort_session.get_outputs()[0].name
    start = time.time()
    result = ort_session.run([output_name], {input_name: input_np})[0]
    elapsed = (time.time() - start) * 1000
    print(f" 推理耗时：{elapsed:.1f}ms")
    print(f" 输出 shape: {result.shape}")

    # 5. 展示结果
    print("\n[Step 4] 解析结果...")
    try:
        labels = download_imagenet_labels()
        show_top5(result, labels)
    except Exception as e:
        print(f" 无法下载标签：{e}")
        top5_idx = np.argsort(result[0])[-5:][::-1]
        print(f" Top-5 类别 ID：{top5_idx}")
    
    print("\n" + "=" * 60)
    print("OK W2 端到端 Demo 完成！")
    print("=" * 60)
    print("\n本周成果总结：")
    print("  1. ResNet50 成功导出为 ONNX 格式（动态 batch）")
    print("  2. ONNX Runtime 推理结果与 PyTorch 一致（误差 < 1e-4）")
    print("  3. 用 Netron 可视化了计算图，理解了节点结构")
    print("  4. 用 onnx-simplifier 做了图优化，节点数减少")
    print("  5. 完成端到端推理 Demo")
    print("\n下周（W3）：用 C++ ONNX Runtime API 做命令行推理 Demo")

if __name__ == "__main__":
    main()
