import onnxruntime
import numpy as np
import torch
import torch.nn.functional as F
import pandas as pd
import onnx


print(f"pytorch版本：{torch.__version__}")
print(f"onnx版本：{onnx.__version__}")
print(f"onnx runtime版本：{onnxruntime.__version__}")


ort_session = onnxruntime.InferenceSession('resnet18_imagenet.onnx')


x = torch.randn(1, 3, 256, 256).numpy()
print(f'x shape: {x.shape}')
ort_inputs = {'input': x}
ort_output = ort_session.run(['output'], ort_inputs)[0]
print(f'ort_output shape: {ort_output.shape}')


img_path = 'banana1.jpg'
from PIL import Image
img_pil = Image.open(img_path)
print(f'image pil: {img_pil}')


from torchvision import transforms
test_transform = transforms.Compose([transforms.Resize(256),
                                    transforms.CenterCrop(256),
                                    transforms.ToTensor(),
                                    transforms.Normalize(
                                        mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
                                    ])

input_img = test_transform(img_pil)
print(f'input img shape: {input_img.shape}')


input_tensor = input_img.unsqueeze(0).numpy()
print(f'input tensor shape: {input_tensor.shape}')


ort_inputs = {'input': input_tensor}
pred_logits = ort_session.run(['output'], ort_inputs)[0]
pred_logits = torch.tensor(pred_logits)
print(f'pred logits shape: {pred_logits.shape}')
pred_softmax = F.softmax(pred_logits, dim=1)
print(f'pred softmax shape: {pred_softmax.shape}')


n = 3
top_n = torch.topk(pred_softmax, n)
print(f'top_n: {top_n}')

# 这行代码的作用是从 top_n.indices 获取模型输出概率中排名前 n 位类别的索引（类别ID）。
# top_n.indices 是一个形状为 (batch_size, n) 的张量，此处 batch_size=1，n=3。
# .numpy() 会把 tensor 转成 numpy 数组，得到形状 (1, 3)；
# [0] 表示只取第一个样本（只有一张图片），最终 pred_ids 存储了 top 3 的类别ID，类型为 numpy 数组。
pred_ids = top_n.indices.numpy()[0]
print(f'pred_ids: {pred_ids}')
confs = top_n.values.numpy()[0]
print(f'confs: {confs}')


df = pd.read_csv('imagenet_class_index.csv')
idx_to_labels = {}
idx_to_labels_chinese = {}
for idx, row in df.iterrows():
    idx_to_labels[row['ID']] = row['class']
    idx_to_labels_chinese[row['ID']] = row['Chinese']
# print(f'idx_to_label: {idx_to_labels}')
# print(f'idx_to_labels_chinese: {idx_to_labels_chinese}')

for i in range(n):
    class_name = idx_to_labels[pred_ids[i]]
    class_name_chinese = idx_to_labels_chinese[pred_ids[i]]
    confidence = confs[i] * 100
    text = '{:<20} {:<20} {:>.3f}'.format(class_name, class_name_chinese, confidence)
    print(text)
