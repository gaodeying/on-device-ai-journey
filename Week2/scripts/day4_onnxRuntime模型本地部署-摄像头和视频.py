from sre_parse import SUCCESS
import cv2
from PIL import Image
import time

import onnxruntime

import torch
from torch._refs import to
import torch.nn.functional as F
from torchvision import transforms

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


ort_session = onnxruntime.InferenceSession('resnet18_imagenet.onnx')

df = pd.read_csv('imagenet_class_index.csv')
idx_to_labels = {}
idx_to_labels_chinese = {}
for idx, row in df.iterrows():
    idx_to_labels[row['ID']] = row['class']
    idx_to_labels_chinese[row['ID']] = row['Chinese']

test_transform = transforms.Compose([transforms.Resize(256),
                                     transforms.CenterCrop(256),
                                     transforms.ToTensor(),
                                     transforms.Normalize(
                                        mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
                                    ])

# 调用摄像头获取一帧并处理
# cap = cv2.VideoCapture(0)
# time.sleep(3)
# success, img_bgr = cap.read()
# cap.release()
# cv2.destroyAllWindows()

# print(f'img_bgr: {img_bgr.shape}')

# # 这句代码的意思是：因为OpenCV读取的图像是BGR格式，而matplotlib要求是RGB格式，所以通过 img_bgr[:, :, ::-1] 把BGR通道反转成RGB，然后用plt.imshow显示图片。
# plt.imshow(img_bgr[:, :, ::-1])
# plt.show()

# img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
# img_pil = Image.fromarray(img_rgb)

# input_img = test_transform(img_pil)
# input_tensor = input_img.unsqueeze(0).numpy()

# print(f'input_tensor shape: {input_tensor.shape}')

# ort_inputs = {'input': input_tensor}

# pred_logits = ort_session.run(['output'], ort_inputs)[0]
# pred_logits = torch.tensor(pred_logits)

# print(f'pred_logits shape: {pred_logits.shape}')

# pred_softmax = F.softmax(pred_logits, dim=1)
# print(f'pred_softmax shape: {pred_softmax.shape}')

# n=5
# top_n = torch.topk(pred_softmax, n)

# print(f'top_n: {top_n}')

# # 这句代码的意思是：top_n[0] 取出 top_k 预测的分数（置信度），
# # .cpu() 确保张量在 CPU 上，.detach() 断开梯度，.numpy() 转成 numpy 数组，
# # .squeeze() 去除多余的维度，最终 confs 就是前 n 个类别的置信度构成的一维 numpy 数组。
# confs = top_n[0].cpu().detach().numpy().squeeze()

# print(f'confs: {confs}')

# pred_ids = top_n[1].cpu().detach().numpy().squeeze()

# print(f'pred_ids: {pred_ids}')

# for i in range(len(confs)):
#     pred_class = idx_to_labels[pred_ids[i]]
#     pred_class_chinese = idx_to_labels_chinese[pred_ids[i]]
#     text = '{:<15} {:<15} {:>.3f}'.format(pred_class, pred_class_chinese, confs[i])

#     img_bgr = cv2.putText(img_bgr, text, (50, 80 + 80 * i), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0,0,255), 5, cv2.LINE_AA)

# plt.imshow(img_bgr[:, :, ::-1])
# plt.show()



def process_frame(img_bgr):
    
    '''
    输入摄像头拍摄画面bgr-array，输出图像分类预测结果bgr-array
    '''
    
    # 记录该帧开始处理的时间
    start_time = time.time()
    
    ## 画面转成 RGB 的 Pillow 格式
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR转RGB
    img_pil = Image.fromarray(img_rgb) # array 转 PIL
    
    ## 预处理
    input_img = test_transform(img_pil) # 预处理
    input_tensor = input_img.unsqueeze(0).numpy()
    
    ## onnx runtime 预测
    ort_inputs = {'input': input_tensor} # onnx runtime 输入
    pred_logits = ort_session.run(['output'], ort_inputs)[0] # onnx runtime 输出
    pred_logits = torch.tensor(pred_logits)
    pred_softmax = F.softmax(pred_logits, dim=1) # 对 logit 分数做 softmax 运算
    
    ## 解析top-n预测结果的类别和置信度
    top_n = torch.topk(pred_softmax, 5) # 取置信度最大的 n 个结果
    pred_ids = top_n[1].cpu().detach().numpy().squeeze() # 解析预测类别
    confs = top_n[0].cpu().detach().numpy().squeeze() # 解析置信度
    
    # 在图像上写英文
    for i in range(len(confs)):
        pred_class = idx_to_labels[pred_ids[i]]
        pred_class_chinese = idx_to_labels_chinese[pred_ids[i]]
        # 写字：图片，添加的文字，左上角坐标，字体，字体大小，颜色，线宽，线型
        text = '{:<15} {:<15} {:>.3f}'.format(pred_class, pred_class_chinese, confs[i])
        img_bgr = cv2.putText(img_bgr, text, (50, 160 + 80 * i), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_AA)
    
    # 记录该帧处理完毕的时间
    end_time = time.time()
    # 计算每秒处理图像帧数FPS
    FPS = 1/(end_time - start_time)  
    # 图片，添加的文字，左上角坐标，字体，字体大小，颜色，线宽，线型
    img_bgr = cv2.putText(img_bgr, 'FPS  '+str(int(FPS)), (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 4, cv2.LINE_AA)

    return img_bgr



# 调用摄像头获取逐帧并处理
# cap = cv2.VideoCapture(0)

# cap.open(0)

# while cap.isOpened():
#     success, frame = cap.read()
#     if not success:
#         print('获取画面不成功，退出')
#         break
#     frame = process_frame(frame)
#     cv2.imshow('my_window', frame)
#     key_pressed = cv2.waitKey(60)
#     if key_pressed in [ord('q'), 27]:
#         break
#     cap.release()
#     cv2.destroyAllWindows()


from tqdm import tqdm

def generate_video(input_path='videos/robot.mp4'):
    filehead = input_path.split('/')[-1]
    output_path = 'out-' + filehead

    print('视频开始处理', input_path)

    cap = cv2.VideoCapture(input_path)
    frame_count = 0
    while(cap.isOpened()):
        success, frame = cap.read()
        frame_count += 1
        if not success:
            break
    cap.release()
    print('视频总帧数为: ', frame_count)

    cap = cv2.VideoCapture(input_path)
    frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, fourcc, fps, (int(frame_size[0]), int(frame_size[1])))

    with tqdm(total=frame_count-1) as pbar:
        try:
            while(cap.isOpened()):
                success, frame = cap.read()
                if not success:
                    break

                try:
                    frame = process_frame(frame)
                except:
                    print('报错！', error)
                    pass
                if success == True:
                    out.write(frame)
                    pbar.update(1)

        except:
            print('中途中断')
            pass

        cv2.destroyAllWindows()
        out.release()
        cap.release()
        print('视频已保存', output_path)


generate_video(input_path='video_4.mp4')