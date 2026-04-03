"""
第一个完整推理DEMO：加载ResNet50 预训练模型，对一张图片进行分类。
这是后续搜有端侧部署的起点！
"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import time
import urllib.request
import os

# ========================
# Step1: 加载预训练模型
# ========================

print(" Step 1: 加载 RestNet50 预训练模型 ...")

start = time.time()
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

elapsed = (time.time() - start) * 1000

print(f"加载模型时间: {elapsed: .0f} ms")
# 统计模型内所有参数（weights和bias等）的总数。其中 model.parameters() 会返回模型中所有参数张量，p.numel() 获取每个参数张量的元素个数，sum(...) 计算这些元素个数的总和，格式化输出为用逗号分隔的整数。
print(f"模型的参数量: {sum(p.numel() for p in model.parameters()):,} 个")
# 计算模型大小的估算方法如下：
# 1. model.parameters() 会返回模型中所有的参数张量（如权重、偏置）。
# 2. p.numel() 表示每个参数张量中元素的数量。遍历所有参数张量后，用 sum(p.numel() * 4 for p in model.parameters()) 计算全部参数所占的总字节数；
#    这里*4是因为PyTorch默认参数类型为float32，每个元素占4字节。
# 为什么除以 1e6？因为 model.parameters() 统计的是元素个数，每个 float32 参数占 4 字节，
# 所以总字节数除以 1,000,000（1e6）即可得到 MB（兆字节）为单位的模型大小估算
# 4. :.0f 是格式化输出，不显示小数。
print(f"模型大小估计: {sum(p.numel() * 4 for p in model.parameters()) / 1e6:.0f} MB")

# ===============
# 打印模型结构
# ===============

print("step2: 查看模型结构 （前5层）")
# 下面这行代码的作用是：遍历ResNet50模型的所有子模块（例如conv1、bn1等），enumerate会同时返回索引i（表示第几个子模块）以及(name, moduel)，其中name是子模块的名字（字符串），moduel是对应的子模块对象；这样我们可以依次打印出模型的结构层次和名称，方便理解网络的组成部分。
for i, (name, moduel) in enumerate(model.named_children()):
    print(f"[{i}] {name}: {type(moduel).__name__}")
    if i>= 4:
        print("....")
        break

# ===============
# Step3: 准备输入数据
# ===============

print("step3: 准备输入图片")
# 这两行代码用于生成要测试的图片文件的绝对路径。
# os.path.dirname(__file__) 获取当前 Python 脚本文件所在的目录路径（即 day5_pretrained_inference.py 的文件夹）。
base_dir = os.path.dirname(__file__)
# os.path.join(base_dir, "企业微信截图_20250911200053.png") 将这个目录路径和图片文件名拼成完整的图片文件路径，
# 这样无论脚本从哪里运行，都能正确定位到当前目录下的指定图片文件。
test_image_path = os.path.join(base_dir, "企业微信截图_20250911200053.png")

# 加载图片文件，这里使用 Image.open 打开图片，是因为 open 可以直接读取本地的图片文件并自动识别格式（如PNG、JPG等），返回一个 PIL 图像对象。
# 需要注意的是神经网络通常要求图片为 RGB 三通道，因此用 .convert('RGB') 将图片强制转换为 RGB 格式（无论原始图片是灰度还是有透明通道）。
image = Image.open(test_image_path).convert('RGB')
print(f"原始图片尺寸： {image.size}")

# 定义预处理流程（ImageNet 标准预处理）
# 下面定义的 transform 是一个“图片预处理流水线”，用于把原始图片转换成神经网络可以直接使用的张量（Tensor）格式，并做常见的数据归一化处理，流程如下：
# 1. transforms.Resize(256)：把图片的短边缩放至256像素，保持宽高比例不变。
# 2. transforms.CenterCrop(224)：从中心裁剪一个224x224的正方形区域，和ImageNet训练时对齐。
# 3. transforms.ToTensor()：把PIL图片转为PyTorch张量（Tensor），同时会把像素值统一归一化到[0,1]之间。
# 4. transforms.Normalize(...)：以Imagenet的标准均值、标准差对每个通道做标准化，让图片分布和预训练模型训练时一致。
transform = transforms.Compose([
    transforms.Resize(256),              # 1. 缩放短边到256像素
    transforms.CenterCrop(224),          # 2. 中心裁剪224x224
    transforms.ToTensor(),               # 3. 转为Tensor并归一到[0,1]
    transforms.Normalize(                # 4. 标准化（减均值、除方差）
        # 这里的 mean 和 std 为什么这样选？—— 是有讲究的！
        # [0.485, 0.456, 0.406]（均值）和 [0.229, 0.224, 0.225]（标准差）是 ImageNet 数据集上所有训练图片统计出来的归一化参数：
        # 这里做的事情其实很简单，假设你有一张色彩图片，每个像素的数值范围是0~255，就像你平时拍的照片那样。
        # 首先，把这些数值都除以255，让它们变成0到1之间的小数，这样处理叫“归一化”，方便计算机理解。
        # 接着，对于每个颜色通道（红、绿、蓝），我们再做两步小调整：先减去一个平均值（比如红色通道就减掉0.485），然后除以一个标准值（比如红色通道除以0.229）。
        # 这样做的目的其实很人性化 —— 就好像让不同品牌、不同光线下拍的图片，都变成“机器最习惯看到的样子”，这样AI才不会因为图片风格太不同而感到困惑。
        # 总结：这样标准化之后，模型就能更容易看懂各种图片，也能做出更稳定、更靠谱的识别结果。
        # - 这样做的好处是让我们自己的推理图片“数据分布”与模型训练时一致，否则会导致模型输出异常、精度下降。
        mean=[0.485, 0.456, 0.406],      #   ImageNet 训练集RGB三通道归一化均值
        std=[0.229, 0.224, 0.225]        #   ImageNet 训练集RGB三通道归一化方差
    ),
])

input_tensor = transform(image)
input_batch = input_tensor.unsqueeze(0)
print(f"预处理后的shape: {input_batch.shape}")


# ==========================================
# Step 4: 执行推理
# ==========================================
print("\n Step 4: 执行推理....")
# 这里是模型推理的核心代码。我们用 with torch.no_grad(): 包裹住代码块，表示其中的操作不会计算梯度，也不会为反向传播保存计算图，这样可以节省显存，加快推理速度（推理阶段不需要梯度）。
with torch.no_grad():
    # 获取当前时间，开始计时，用于衡量前向推理（inference）耗时
    start = time.time()
    # 将预处理后的图片张量送入模型，得到输出（即分类结果的原始分数logits）
    output = model(input_batch)
    # 再次获取当前时间，计算推理总耗时（毫秒ms）
    elapsed_ms = (time.time() - start) * 1000

print(f"推理耗时：{elapsed_ms:.1f}ms")
print(f"输出模型: {output.shape}")


# ===========================================
# Step 5: 解析输出 （Top-5 分类结果）
# ===========================================
print("\n Step 5: 解析分类结果 （Top-5）")

# Softmax 转成概率
# 我们拿到模型的输出 output，其实是一个很长的一维向量（output[0]），它里面每个数字对应一个类别，代表“原始分数”（logits），此时还不是概率。
# 举个简单的例子：假设 output[0][0:3] 的内容是 [2.0, 1.0, 0.1]，这三个数字分别代表图片是「类别A」「类别B」「类别C」的原始分数。
# 这个时候我们看不出图片到底像哪个类别，只能说分数高低。
# softmax 这一步的作用，就是把这些分数映射成 0~1 之间的小数（概率），并且三者加起来正好是1。
# 上面的例子 softmax 之后可能变成这样：[0.65, 0.24, 0.11]——表示：属于A的概率65%，B的概率24%，C的概率11%，一目了然！
# 为什么用 softmax？—— 因为模型输出的 output[0] 是生硬的分数，没有归一化、不满足概率分布。只有用 softmax 转换后，“每个类别的数字才真正能代表‘可能性’（概率）”。
probabilities = torch.nn.functional.softmax(output[0], dim=0)
print(f"probabilities shape: {probabilities.shape}")

# 下载 ImageNet 类别标签
labels_path = os.path.join(base_dir, "imagenet_classes.txt")
if not os.path.exists(labels_path):
    print(" 下载ImageNet 标签...")
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    urllib.request.urlretrieve(url, labels_path)

# 这句代码的作用是：打开存放类别名称（如"tabby, tabby cat"）的文本文件，并按行读取所有类别，去除换行符，最终得到一个类别名的列表。
with open(labels_path, "r", encoding="utf-8") as f:
    # 下面这句的作用是：依次读取 imagenet_classes.txt 文件中的每一行（每行对应一个类别名称），用 strip() 去掉每行开头和末尾可能的空白符或换行符，最后组成一个字符串列表 categories
    categories = [line.strip() for line in f]

# Top-5 结果
# 这行代码的作用是：从概率张量 probabilities 中选出数值最大的前5个元素。
# 其中，top5_prob 存放的是前5个最大概率（从大到小排序），top5_catid 存放的是对应的类别索引（类别编号）。
# 比如，如果 probabilities 维度为 [1000]，结果 top5_catid = [281, 285, 409, 282, 207]，说明最大概率的是编号281的类别。
top5_prob, top5_catid = torch.topk(probabilities, 5)
print("\n 分类结果")
# 这段代码用于输出 Top-5 预测结果的详细信息：
# 遍历 top5_prob（概率）和 top5_catid（类别索引）的前5个结果
for i in range(top5_prob.size(0)):
    # 取出第i个预测的类别名称，categories列表是对应ImageNet类别名的列表
    category = categories[top5_catid[i].item()]
    # 取出当前类别的概率值
    prob = top5_prob[i].item()
    # 用"🧧"符号打印一个进度条，长度和概率成正比（最多30个）
    bar = "🧧" * int(prob * 30)
    # 按照指定格式输出排名、类别名、概率和可视化条形图
    print(f" {i+1}. {category:30s} | {prob:.4f} | {bar}")



# ========================================================
# Step 6: 记录性能数据 (重要！)
# ========================================================
print("\n" + "=" * 50)
print("性能数据汇总（面试时可以提到）")
print("=" * 50)
print(" 设备：CPU （MacBook）")
print(" 模型：ResNet50 (FP32)")
print(" 输入：1x3x224x224")
print(" 模型参数: 25.6M")
print(f" 推理延迟: {elapsed_ms:.1f}ms")
print(" (这是数据是指真实测到的，记住它！)")
print("\n 第一个完整推理 Demo 完成！")

