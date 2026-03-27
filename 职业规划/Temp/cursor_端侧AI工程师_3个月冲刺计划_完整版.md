# 端侧 AI 工程师 3 个月冲刺计划（完整版）

> 目标对象：终端全栈开发（Android/iOS/RN），33岁，15年本科，转型端侧 AI Infra 方向  
> 目标岗位：字节跳动「端侧AI Infra开发工程师」/ 智元机器人「端侧AI infra工程师」  
> 学习周期：90 天（12 周）

---

## 一、核心 JD 要求拆解对比

| 能力维度 | 字节跳动 | 智元机器人 | 你现有优势 |
|---|---|---|---|
| 编程语言 | C++、Python | C++、Python | 有 NDK/JNI C++ 基础 |
| 推理框架 | TFLite、PyTorch Mobile、ONNX Runtime | PyTorch、Jax | 有 Android 接入框架经验 |
| 模型优化 | 量化、压缩 | 量化、剪枝、蒸馏（torchao） | 暂无，需重点学习 |
| 硬件架构 | ARM、X86、GPU/NPU | CUDA、cudagraph | 熟悉 ARM，需补 GPU |
| 性能分析 | 性能分析工具 | torch profiler、torch compile | 熟悉 Android Profiler |
| 算法认知 | 推理执行模块 | transformer engine、lerobot/gr00t | 需补充 |
| 数据存储 | SQL、NoSQL | — | 有基础 |

**结论：蔚来 JD 偏向架构师级（10年+，LLVM/CUDA底层），不作为3个月主攻目标。主攻字节+智元。**

---

## 二、你的核心优势（面试话术锚点）

- **ARM 架构理解**：多年 Android/iOS 开发对 ARM 内存布局、线程调度有实际认知，这是纯算法工程师的盲区
- **NDK/JNI 经验**：C++ 与业务层互通，直接复用到端侧推理引擎接入
- **移动端性能调优**：熟悉 Android Studio Profiler、Instruments，迁移到 AI Infra 性能分析门槛低
- **系统稳定性意识**：懂 OOM、ANR、低功耗，AI 模型上端后同样面临这些问题

---

## 三、90 天学习路线图

### 第一阶段：重塑 AI 技术栈基础（第 1-3 周）

**目标：** 具备用 Python+PyTorch 加载/查看/导出模型的基本能力，重激活现代 C++

---

#### Week 1：Python + PyTorch 入门（专注推理，非训练）

**每天 2 小时，共 14 小时**

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | Python 快速扫盲 | 数据类型、列表推导、numpy 基础、虚拟环境 venv/conda |
| 3-4 | PyTorch Tensor 操作 | Tensor 创建、维度变换、数据类型（FP32/FP16/INT8） |
| 5-6 | 加载预训练模型 | `torchvision.models.resnet50(pretrained=True)` 跑推理 |
| 7 | 理解模型结构 | 用 `print(model)` 查看层结构，理解参数量 |

**学习资源：**
- [PyTorch 官方 60分钟入门](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
- [Fast.ai Practical Deep Learning（只看第1课）](https://course.fast.ai)

---

#### Week 2：现代 C++ 激活 + NDK 接入复习

**每天 2 小时，共 14 小时**

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | C++11/14/17 现代特性 | `unique_ptr`、`shared_ptr`、`auto`、`lambda`、`move` 语义 |
| 3-4 | 内存对齐与高效分配 | `std::vector` 内存布局、`aligned_alloc`（AI 推理核心） |
| 5-6 | NDK 推理调用框架 | 用 CMake + NDK 写一个简单的 C++ 矩阵乘法，从 Java 调用 |
| 7 | 复习 JNI 接口设计 | 设计一个 `InferenceEngine` C++ 类并封装 JNI 接口 |

**学习资源：**
- 《现代C++教程》（GitHub 开源，中文）：https://github.com/changkun/modern-cpp-tutorial
- Android NDK 官方 Sample：https://github.com/android/ndk-samples

---

#### Week 3：深度学习架构认知（不用推公式，要懂结构）

**每天 2 小时，共 14 小时**

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | CNN 架构理解 | ResNet/MobileNet 结构，理解深度可分离卷积（端侧优化关键） |
| 3-4 | Transformer 架构 | Attention 机制、Self-Attention、Multi-Head Attention |
| 5-6 | LLM 推理流程 | Prefill vs Decode 阶段，KV Cache 是什么，为什么重要 |
| 7 | 端侧常见模型盘点 | MobileNet/EfficientNet/Qwen-1.5B/Phi-3-mini 规格对比 |

**学习资源：**
- [3Blue1Brown：神经网络可视化系列](https://www.youtube.com/watch?v=aircAruvnKk)
- [Andrej Karpathy：Let's build GPT（YouTube）](https://www.youtube.com/watch?v=kCc8FmEb1nY)（只需看前1小时）

---

### 第二阶段：端侧推理框架全链路打通（第 4-7 周）

**目标：** 从云端模型 → ONNX → 移动端推理，完整跑通一次；掌握 CPU/GPU/NPU 算力选择逻辑

---

#### Week 4：ONNX 格式与导出（面试必考）

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | ONNX 格式解析 | 了解 `.onnx` 文件结构（protobuf），用 **Netron** 可视化网络拓扑 |
| 3-4 | PyTorch → ONNX 导出 | `torch.onnx.export()` 导出 ResNet50，处理动态 batch size |
| 5 | ONNX 图优化 | 用 `onnx-simplifier` 对导出模型做图折叠优化 |
| 6-7 | ONNX Runtime CPU 推理 | Python 版 ONNX Runtime 跑推理，对比 PyTorch 推理结果 |

```python
# 核心代码示例：PyTorch → ONNX
import torch
import torchvision

model = torchvision.models.resnet50(pretrained=True)
model.eval()
dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model, dummy_input, "resnet50.onnx",
    input_names=["input"], output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}}
)
```

**学习资源：**
- ONNX 官方文档：https://onnx.ai/onnx/intro/
- Netron 可视化工具：https://netron.app

---

#### Week 5：TFLite 端侧部署

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | TFLite 格式转换 | ONNX → TFLite（通过 tf2onnx 或 ai-edge-torch） |
| 3-4 | TFLite Interpreter | C++ Interpreter API，了解 Delegate 机制（GPU/NNAPI Delegate） |
| 5-6 | Android 接入实战 | 把 .tflite 模型集成进 Android App，跑通图像分类 |
| 7 | 性能基准测试 | 使用 `TFLite Benchmark Tool` 测试延迟和内存 |

**学习资源：**
- TFLite 官方文档：https://www.tensorflow.org/lite/guide
- Google MediaPipe 示例：https://github.com/google-ai-edge/mediapipe

---

#### Week 6：ONNX Runtime 移动端 C++ 集成

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | ORT Mobile 下载与集成 | 下载 onnxruntime-android AAR，CMake 集成 |
| 3-5 | C++ 推理引擎实现 | 写一个完整的 `InferenceEngine` 类：加载模型、前处理、推理、后处理 |
| 6-7 | 跑通 YOLO 目标检测 | 参考开源项目 `ncnn-android-yolov8`，改造成 ONNX Runtime 版本 |

**里程碑：** 能在自己手机上本地运行一个完整的视觉 AI 模型，并打印出推理延迟数据

---

#### Week 7：CPU/GPU/NPU 硬件算力调度（字节 JD 第1、4条）

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | Android AI 加速生态 | NNAPI、GPU Delegate、高通 QNN、联发科 APU 原理 |
| 3-4 | iOS Core ML 与 ANE | Core ML 格式、Apple Neural Engine 调用路径 |
| 5 | GPU vs NPU 选型逻辑 | 什么场景用 GPU（大 batch）vs NPU（固定拓扑低延迟） |
| 6-7 | 接入 GPU Delegate | 在 Week 6 的项目中切换 GPU Delegate，对比延迟变化 |

**面试话术：** "我在端侧集成时会根据任务类型做 Delegate 选择——实时视频流用 GPU Delegate，固定结构的唤醒词检测用 NPU，避免初始化开销。"

---

### 第三阶段：模型量化与性能调优（第 8-10 周）

**目标：** 掌握 PTQ/QAT 量化技术，能用 torch profiler 定位性能瓶颈（字节/智元核心痛点）

---

#### Week 8：量化原理深挖（面试高频考题）

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | 浮点与整型数值表示 | FP32/FP16/BF16/INT8/INT4 的范围与精度损失 |
| 3-4 | PTQ 原理 | 校准集、最大值校准 vs KL散度校准，Scale/Zero-point 计算公式 |
| 5-6 | QAT 原理 | 伪量化节点（FakeQuantize），为何精度损失更小 |
| 7 | GGUF/AWQ/GPTQ 对比 | 当前 LLM 量化主流格式，能说清楚区别 |

**必背面试答案：**
> "PTQ 是训练后量化，不需要重新训练，速度快但精度损失稍大；QAT 是量化感知训练，在训练中模拟量化误差，精度损失更小但需要数据集。INT4 量化可以把 7B 模型从 14GB 压缩到约 4GB，配合 KV Cache 量化可以进一步降低内存占用。"

---

#### Week 9：动手量化实战（torchao + llama.cpp）

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | torchao 安装与使用 | 对 Qwen2.5-1.5B 做 INT4 量化：`torchao.quantize_(model, int4_weight_only())` |
| 3-4 | llama.cpp 编译与运行 | 用 llama.cpp 的 `quantize` 工具做 Q4_K_M 量化，跑推理测速 |
| 5-6 | 量化前后指标对比 | 体积（GB）、内存峰值（RSS）、首字延迟（TTFT）、tokens/s |
| 7 | 量化结果写入简历 | **整理数据**：如"INT4量化将1.5B模型体积从3.1GB降至0.9GB，推理速度提升2.3倍" |

**学习资源：**
- torchao：https://github.com/pytorch/ao
- llama.cpp：https://github.com/ggerganov/llama.cpp

---

#### Week 10：性能 Profiling 与图优化

| 天 | 学习内容 | 具体任务 |
|---|---|---|
| 1-2 | torch.profiler 使用 | 分析模型每层算子耗时，找出 Top 3 瓶颈层 |
| 3-4 | torch.compile 加速 | `torch.compile(model)` 的原理（TorchDynamo + Inductor），实测提升 |
| 5-6 | Android Studio Profiler | 用 CPU Profiler 和 Memory Profiler 分析 C++ 推理的调用栈 |
| 7 | 算子融合概念 | 理解 Fused Attention、Conv-BN-ReLU 融合，为什么能提速 |

```python
# torch.profiler 使用示例
import torch
from torch.profiler import profile, record_function, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
             record_shapes=True) as prof:
    with record_function("model_inference"):
        output = model(input_data)

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))
```

---

### 第四阶段：项目包装与面试突击（第 11-12 周）

---

#### Week 11：打造"杀手级"开源项目

**项目方案（任选其一）：**

**方案 A（推荐）：端侧本地 LLM 推理引擎**
- 技术栈：C++ + NDK + ONNX Runtime / ExecuTorch
- 模型：Qwen2.5-1.5B 做 INT4 量化
- 功能：Android App 本地 LLM 对话（无网络）
- 指标数据（必须写进简历）：
  - 模型体积：量化后 < 1GB
  - 内存峰值：< 1.5GB RSS
  - 首字延迟（TTFT）：< 500ms（骁龙 8 Gen 系列）
  - 生成速度：> 10 tokens/s

**方案 B：端侧实时视觉 AI Pipeline**
- 技术栈：C++ + ONNX Runtime + GPU Delegate
- 模型：YOLOv8n（检测）+ MobileNet（分类）
- 功能：摄像头实时检测，30FPS 流畅运行
- 指标数据：INT8 量化后延迟 < 50ms，内存 < 200MB

**GitHub README 必写内容：**
1. 架构图（端侧 AI 推理链路：模型转换 → 量化 → C++ 引擎 → JNI → UI）
2. 性能 Benchmark 表格
3. 与未量化版本的对比数据

---

#### Week 12：面试突击训练

**高频面试题清单：**

**基础原理类：**
1. INT8 量化的 Scale 和 Zero-point 是如何计算的？PTQ 和 QAT 有什么区别？
2. ONNX 是什么？为什么说它是端侧部署的中间层？
3. Transformer 的 Attention 复杂度是 O(n²)，在端侧如何优化长序列推理？
4. KV Cache 是什么原理？它能解决什么问题？
5. 为什么端侧推理偏向 INT4/INT8 而非 FP16？

**工程实践类：**
1. 你如何选择在 Android 上用 CPU/GPU/NPU 跑推理？
2. 模型从云端迁移到端侧，你会做哪些工程改造？
3. 推理延迟高，你会从哪些维度排查？（算子耗时 → 内存带宽 → 精度损失）
4. 描述一次你做性能优化的经历，量化了哪些指标？（用你的 Android 经验回答）

**开放题类（结合你的背景）：**
1. 你的移动端背景对端侧 AI 开发有哪些帮助？
   > 答：我理解 ARM 内存模型、线程优先级调度、OOM 处理机制，这些在集成 AI 推理引擎时直接复用——比如我知道用 `mmap` 加载大模型权重比 `malloc` 内存更高效，也清楚在 UI 线程调推理的风险。

---

## 四、学习资源汇总

### 必读书籍
| 书名 | 用途 | 优先级 |
|---|---|---|
| 《现代C++教程》（开源） | 激活 C++ 语法 | ⭐⭐⭐⭐⭐ |
| 《动手学深度学习》（李沐，开源） | 理解模型结构 | ⭐⭐⭐⭐ |
| 《LLM从入门到实践》 | LLM 推理机制 | ⭐⭐⭐ |

### 必刷项目（GitHub）
| 项目 | 学习点 |
|---|---|
| [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) | C++ 推理引擎设计，量化实现 |
| [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) | 工业级推理引擎 C++ API |
| [pytorch/executorch](https://github.com/pytorch/executorch) | Meta 官方端侧 PyTorch 方案 |
| [Tencent/ncnn](https://github.com/Tencent/ncnn) | 国内成熟端侧框架，C++ 实现 |
| [pytorch/ao](https://github.com/pytorch/ao) | torchao 量化工具（智元 JD 提到） |

### 视频课程
| 课程 | 平台 | 用途 |
|---|---|---|
| Andrej Karpathy - Zero to Hero | YouTube | 理解 LLM 原理 |
| MIT 6.5940 EfficientML | YouTube | 端侧 AI 专项（量化/剪枝/蒸馏） |
| 李沐《动手学深度学习》 | B站/YouTube | 中文深度学习入门 |

---

## 五、每周时间规划建议

```
平日（周一至周五）：
  07:00-08:00  理论学习（读文档/看视频）
  20:00-21:30  编码实践（每天必须有代码输出）

周末（周六周日）：
  09:00-12:00  项目实战（跑通完整 Demo）
  15:00-17:00  总结笔记 + GitHub 提交
  19:00-21:00  预习下周内容

每周必须产出：
  ✅ 1 个可运行的代码 Demo
  ✅ 1 篇技术总结笔记（掘金/知乎发布，积累影响力）
  ✅ GitHub commit 记录（面试时展示）
```

---

## 六、简历改造策略

### 标题改造
- 原来：高级移动端开发工程师（Android/iOS/RN）
- 改后：**端侧 AI 应用开发工程师 | Android/C++/ONNX Runtime**

### 核心技能改造
在技能栏加入：
- 推理框架：ONNX Runtime、TFLite、llama.cpp
- 模型优化：INT8/INT4 量化（PTQ/QAT）、模型压缩
- 硬件平台：ARM Cortex-A、Android NNAPI、Apple Core ML
- 工具：torch.profiler、Netron、Android Studio Profiler

### 工作经历改造
把过去 Android 工作经历中的性能优化点提炼出来，包装成 AI Infra 视角：
- "优化了 App 启动时 .so 库加载时序" → **"具备 Native 库按需加载经验，可类比优化端侧 AI 引擎的动态加载策略"**
- "解决了 RecyclerView 的内存泄漏" → **"掌握 Android 内存生命周期管理，可保障大模型推理时的内存安全"**

---

## 七、三个月后的目标自测

完成以下检查项即代表达到面试标准：

- [ ] 能从头将 PyTorch 模型导出 ONNX，并在 Android 上通过 C++ 跑通推理
- [ ] 能清晰解释 PTQ 和 QAT 的区别，说出 Scale/Zero-point 的计算方式
- [ ] 动手做过 INT4/INT8 量化实验，有量化前后性能对比数据
- [ ] 用过 torch.profiler 找到过模型的性能瓶颈层
- [ ] GitHub 上有一个完整的端侧 AI 推理项目，有 README 和 Benchmark 数据
- [ ] 能回答"为什么选 ONNX 而不是 TFLite"这类框架选型题
- [ ] 能用自己的 Android 经验类比解释端侧 AI Infra 工作的价值

---

*制定时间：2026年3月25日*  
*参考 JD：字节跳动端侧AI Infra开发工程师 / NIO蔚来端侧AI Infra架构师 / 智元机器人端侧AI infra工程师*
