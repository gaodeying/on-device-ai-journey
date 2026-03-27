# 端侧 AI → 具身智能机器人  
## 3 个月冲刺计划（完整版 v2.0）

> **作者背景**：终端全栈（Android / iOS / RN），33岁，15年本科  
> **阶段目标**：3个月内，可投 `端侧AI开发工程师` / `端侧推理优化工程师` / `AI SDK工程师`  
> **终极目标**：以手机端 AI 为跳板，进入具身智能机器人行业  
> **学习周期**：2026-03-30 → 2026-06-21（12周）  
> **制定时间**：2026年3月25日 | **Review版本**：v2.0

---

## 一、岗位层级与边界感

| 层级 | 代表岗位 | 3个月能否达到 | 说明 |
|------|---------|:----------:|------|
| 入门 | 端侧AI开发工程师（字节/中厂） | ✅ 可以 | 主攻目标 |
| 中级 | 端侧 AI Infra（推理优化/SDK） | ⚠️ 可冲击 | 3个月上限 |
| 高级 | 蔚来类 AI Infra 架构师（LLVM/CUDA管理） | ❌ 暂不适合 | 1-2年后 |
| 终极 | 具身智能机器人端侧工程师 | 🎯 半年后可投 | 本计划第11周开始铺垫 |

**结论**：先打 `字节/中厂端侧AI工程师` → 积累半年 AI Infra 真实经验 → 跳具身智能机器人。

---

## 二、你的核心优势（面试话术锚点）

这是你比纯算法工程师强的地方，面试时必须主动提：

- **ARM 架构理解**：多年 Android/iOS 开发对 ARM 内存布局、线程调度有实际认知
- **NDK/JNI 经验**：C++ 与业务层互通，直接复用到端侧推理引擎接入
- **移动端性能调优**：熟悉 Android Studio Profiler / Xcode Instruments，迁移 AI Infra 门槛极低
- **系统稳定性意识**：懂 OOM、ANR、低功耗，AI 模型上端后同样面临这些问题
- **双端落地能力**：能同时在 Android + iOS 上验证 AI 效果，这是很多纯 AI 同学做不到的

> 面试叙事定位：**"我不是转行新人，我是把 AI 落到端上的工程化专家。"**

---

## 三、技术栈选型（2026年最新）

> 以下选型已根据各框架官方最新状态确认，避免学习已废弃技术。

### 核心技术栈（必须掌握）

| 层次 | 选型 | 备注 |
|------|-----|------|
| AI 框架 | PyTorch（仅推理/导出） | 不学训练，只学推理和导出 |
| 中间格式 | ONNX | 端侧部署行业标准 |
| 主推理框架（Android） | **ONNX Runtime Mobile** | 工业级首选，C++ API 完善 |
| 主推理框架（iOS） | **Core ML + coremltools** | Apple 生态官方方案 |
| Google 端侧框架 | **LiteRT**（原 TFLite，2024年改名） | 需用新包名 `com.google.ai.edge.litert` |
| Meta 端侧框架 | **ExecuTorch** | PyTorch Mobile 已废弃，官方替代 |
| 国内端侧框架 | **ncnn**（腾讯开源） | 国内华为/vivo/OPPO 等大量使用，面试高频 |
| 量化工具 | **torchao** / **llama.cpp** | PTQ/INT4/INT8 实战 |
| 性能分析 | torch.profiler / Android Profiler / Instruments / Perfetto | 必须动手用过 |
| 机器人框架 | **LeRobot**（HuggingFace） + **ROS2 Humble** | 第11周重点 |

### 明确废弃，不要深学

> 以下三项在学习计划中**不会出现**，只作为"知道它们已过时"的背景知识，面试时能说出替代方案即可。

| 已废弃 | 状态 | 替代方案 |
|-------|------|--------|
| TensorFlow Lite（旧包名） | 2024年官方改名为 LiteRT | → 直接用 **LiteRT** |
| PyTorch Mobile | 已停止维护，官方声明废弃 | → 用 **ExecuTorch** |
| Android NNAPI | Android 15 起官方废弃 | → 用 **LiteRT GPU Delegate** / AICore |

---

## 四、12 周详细学习路线

### 总体节奏

```
平日（周一至周五）：
  07:00-08:00  理论学习（读文档/看视频）
  20:00-21:00  LeetCode 刷题 30min（从 W6 开始，大厂算法面必考）
  21:00-22:00  编码实践（每天必须有代码输出）

周末（周六周日）：
  09:00-12:00  项目实战（跑通完整 Demo）
  15:00-17:00  总结笔记 + GitHub 提交
  19:00-21:00  预习下周内容

每周必须产出：
  ✅ 1 个可运行的代码 Demo 或 Feature
  ✅ 1 份性能数据表（时延、内存、FPS 等）
  ✅ 1 篇技术总结（掘金/知乎发布，积累影响力）
  ✅ GitHub commit 记录（面试时展示）

LeetCode 刷题策略（W6起）：
  → 每天 1 题，中等难度为主
  → 优先：数组/字符串/链表/树/DP/滑动窗口
  → 目标：3个月共刷 50 题（量不求多，每题弄懂）
```

---

### 第1阶段：重塑 AI 技术栈基础（W1-W3）

**阶段目标**：具备用 Python + PyTorch 加载/导出模型的基本能力，重激活现代 C++，理解 AI 关键架构

---

#### W1（3/30-4/5）：Python + PyTorch + ONNX 推理打通

> **核心目标**：`PyTorch 加载模型 → ONNX 导出 → Python 推理` 最小闭环跑通

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | 环境搭建 | 安装 Conda、PyTorch、onnxruntime；配置 venv；确认 Python 3.10+ |
| 周二 | Python 扫盲 | Numpy 基础、Tensor 操作、`FP32/FP16/INT8` 数据类型含义 |
| 周三 | 加载预训练模型 | `torchvision.models.resnet50(weights='DEFAULT')` 跑推理，打印层结构 |
| 周四 | ONNX 导出 | `torch.onnx.export()` 导出 ResNet50，用 **Netron** 可视化网络拓扑 |
| 周五 | ONNX Runtime 推理 | Python 版 `onnxruntime` 跑推理，对比 PyTorch 输出是否一致 |
| 周六 | 图优化 | 用 `onnx-simplifier` 做图折叠，观察节点数变化；`onnxoptimizer` 了解 |
| 周日 | 复盘 + 写笔记 | 整理"ONNX 格式是什么、为什么是端侧标准"，发掘金/知乎 |

**本周产出**：`加载→导出→推理` 完整 Python 脚本 + 第一篇技术博客

**学习资源**：
- [PyTorch 60分钟入门](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
- [ONNX 官方文档](https://onnx.ai/onnx/intro/)
- [Netron 可视化工具](https://netron.app)

---

#### W2（4/6-4/12）：现代 C++ 激活 + NDK 推理框架

> **核心目标**：C++ 写一个独立的命令行推理 Demo，代码要能跑通，不强求不依赖任何库

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | C++11/14/17 现代特性 | `unique_ptr`、`shared_ptr`、`auto`、`lambda`、`move` 语义复习 |
| 周二 | 内存对齐与高效分配 | `std::vector` 内存布局、`aligned_alloc`（AI 推理核心基础） |
| 周三 | ONNX Runtime C++ API | 加载 `.onnx` 文件，设置 `SessionOptions`，跑一次推理 |
| 周四 | 前后处理 C++ 实现 | 图片解码用 **stb_image**（单头文件，工程常用），写 resize/normalize |
| 周五 | 异常处理与性能计时 | `std::chrono` 计时，try-catch 封装推理错误 |
| 周六 | 封装 CLI 工具 | 做一个命令行：`./infer --model xxx.onnx --image xxx.jpg` |
| 周日 | JNI 接口设计 | 设计 `InferenceEngine` C++ 类并封装 JNI 接口，为下周 Android 做准备 |

> **说明**：前后处理推荐使用 stb_image（行业通用轻量方案），实际工程中不需要从零实现图片解码。

**本周产出**：C++ 命令行推理 Demo（README + 性能计时输出）

**学习资源**：
- [《现代C++教程》（开源，中文）](https://github.com/changkun/modern-cpp-tutorial)
- [ONNX Runtime C++ API 文档](https://onnxruntime.ai/docs/api/c/index.html)
- [stb_image 单头文件图片库](https://github.com/nothings/stb/blob/master/stb_image.h)

---

#### W3（4/13-4/19）：AI 架构认知（不推公式，只懂结构）

> **核心目标**：能解释 Transformer、CNN、KV Cache；了解业界端侧 AI 产品现状

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | CNN 架构 | ResNet/MobileNet 结构，深度可分离卷积（端侧优化关键） |
| 周二 | Transformer 架构 | Attention 机制、Self-Attention、Multi-Head Attention |
| 周三 | LLM 推理流程 | Prefill vs Decode 阶段，KV Cache 是什么，为什么重要 |
| 周四 | 端侧常见模型盘点 | MobileNet/EfficientNet/Qwen-1.5B/Phi-3-mini 规格对比表 |
| 周五 | 业界端侧AI产品调研 | 调研华为小艺/Apple Intelligence/高通 AI Hub/联发科 APU 的实际落地，记录技术方案 |
| 周六 | 复盘输出 | 整理"端侧模型对比表"（体积、参数量、推理框架支持情况） |
| 周日 | 预习 Android 接入 | 阅读 ONNX Runtime Mobile 官方文档 Android 部分 |

> **说明**：VLA/具身智能是高阶内容，放到 W11 集中学习，此阶段先打牢基础认知。

**本周产出**：端侧模型对比表 + 业界端侧 AI 产品调研笔记

**学习资源**：
- [3Blue1Brown 神经网络可视化](https://www.youtube.com/watch?v=aircAruvnKk)
- [Andrej Karpathy Let's build GPT（只看前1小时）](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- [Qualcomm AI Hub 模型库](https://aihub.qualcomm.com/)

---

### 第2阶段：双端推理落地（W4-W7）

**阶段目标**：Android + iOS 双端各自跑通完整推理 App，掌握主流端侧框架，量化已有实战数据

---

#### W4（4/20-4/26）：Android 端侧推理落地（ONNX Runtime）

> **核心目标**：在 Android 真机上跑起来，能实时帧推理，有性能数据

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | Android 环境准备 | 配置 NDK r25+，下载 `onnxruntime-android` AAR |
| 周二 | JNI/NDK 接入 ORT | CMake 集成 ONNX Runtime，Java 层调 C++ 推理接口 |
| 周三 | CameraX 实时推理 | 接入相机帧流，做帧采样 + 推理 |
| 周四 | 线程与内存优化 | 推理放 worker thread，避免 ANR；监控内存泄漏 |
| 周五 | 打点统计 | FPS、单帧推理延迟、内存 RSS 打印到 logcat |
| 周六 | UI 展示 + 整理性能报告 | 在画面上叠加推理结果，整理性能表格 |
| 周日 | 录屏 + 提交 GitHub | 推 README + demo.gif + 性能数据表 |

**本周产出**：可演示的 Android 实时推理 App（含性能数据表格）

**里程碑**：你已经具备初级端侧 AI 工程师的面试资格。

**学习资源**：
- [ONNX Runtime Android 官方教程](https://onnxruntime.ai/docs/tutorials/mobile/deploy-android.html)
- [Android NDK Samples](https://github.com/android/ndk-samples)

---

#### W5（4/27-5/3）：量化专项（JD 高频，面试核心）

> **核心目标**：做过 INT8/INT4 量化实验，有真实对比数据，能讲清原理；了解剪枝/蒸馏概念

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | 量化理论 | PTQ vs QAT，FP32/FP16/BF16/INT8/INT4 精度与范围；剪枝/蒸馏概念了解（不动手） |
| 周二 | PTQ 动态量化实践 | `onnxruntime.quantization.quantize_dynamic()` 对 W4 的视觉模型量化 |
| 周三 | PTQ 静态量化 | 校准集 + 最大值校准 vs KL 散度校准，Scale/Zero-point 计算；对比动态 vs 静态结果 |
| 周四 | 端上实测量化模型 | 在 W4 的 Android App 中切换量化前后模型，记录延迟/内存/精度 |
| 周五 | LLM 量化实践 | 用 `torchao.quantize_(model, int4_weight_only())` 对 Qwen2.5-1.5B 做 INT4 量化，测速 |
| 周六 | 写量化实验报告 | 对比表：模型体积、内存峰值、延迟、精度损失（CV 模型 + LLM 模型各一组） |
| 周日 | 面试题演练 | 口述"PTQ 和 QAT 的区别""剪枝/蒸馏是什么"，背 Scale/Zero-point 公式 |

> **说明**：量化顺序设计为"先 CV 小模型打基础 → 再 LLM 大模型验证"，避免第一天就卡在环境/内存问题。  
> **剪枝/蒸馏**：面试会考概念，但 3 个月内不需要动手实现，知道定义和应用场景即可。

**必背面试答案**：
> "PTQ（训练后量化）不需要重训练，速度快但精度损失稍大；QAT（量化感知训练）在训练中模拟量化误差，精度损失更小但需要数据集和重训练。非对称 INT8 量化的 Scale 计算公式是 `scale = (max - min) / 255`，Zero-point 用来将浮点零点映射到整型区间。INT4 量化可以把 7B 模型从 14GB 压缩到约 4GB。剪枝是稀疏化权重减少计算量，蒸馏是用大模型的输出来监督训练小模型。"

**本周产出**：量化实验报告（CV + LLM 各一组，含精度-速度-内存三维对比）

**学习资源**：
- [ONNX Runtime 量化文档](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)
- [torchao GitHub](https://github.com/pytorch/ao)
- [MIT 6.5940 EfficientML（量化/剪枝/蒸馏专项）](https://hanlab.mit.edu/courses/2023-fall-65940)

---

#### W6（5/4-5/10）：LiteRT（Google AI Edge 框架）+ 开始刷题

> **核心目标**：LiteRT 从零接入 Android，会使用 GPU Delegate 加速；**本周起每天 LeetCode 30min**

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | LiteRT 生态认知 | 了解 LiteRT 定位：多框架统一端侧运行时（PyTorch/JAX/Keras 均支持转换接入） |
| 周二 | 模型格式转换 | 用 `ai-edge-litert` converter 把 W1 的 ONNX 模型转为 `.tflite` 格式（LiteRT 使用的模型文件格式） |
| 周三 | LiteRT Android 接入 | 新建 Demo：引入 `com.google.ai.edge.litert` 依赖，加载 `.tflite` 模型跑推理 |
| 周四 | GPU Delegate 实测 | 接入 `GpuDelegateFactory`，对比 CPU vs GPU 延迟，记录数据 |
| 周五 | 官方 Codelab | 跑通官方 image segmentation codelab，理解 Interpreter API 完整生命周期 |
| 周六 | 整理框架选型对比 | 整理 ONNX Runtime vs LiteRT：接入复杂度、模型格式要求、硬件加速支持 |
| 周日 | 复盘 + 预习 iOS | 整理 LiteRT 接入 checklist；阅读 Core ML 官方概览 |

> **说明**：LiteRT 的模型文件格式仍是 `.tflite`（格式不变，只改框架名称和包名）。因此接入前必须先完成 ONNX → `.tflite` 的格式转换，这一步在之前的计划中缺失。

**本周产出**：LiteRT Android Demo + ONNX Runtime vs LiteRT 框架选型对比表

**学习资源**：
- [LiteRT 官方文档](https://ai.google.dev/edge/litert)
- [LiteRT 模型转换指南](https://ai.google.dev/edge/litert/models/convert_model)
- [LiteRT Codelab（图像分割）](https://developers.google.com/codelabs/litert-image-segmentation-android)

---

#### W7（5/11-5/17）：iOS Core ML + Instruments

> **核心目标**：iOS 侧跑通推理 Demo，用 Instruments 做性能分析，完成双端性能横向对比

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | Core ML 框架认知 | 了解 Core ML 格式（`.mlpackage`），Apple Neural Engine 调用路径 |
| 周二 | coremltools 转换 | `ct.convert()` 把 PyTorch 模型转为 Core ML 格式，用 Xcode 预览模型结构 |
| 周三 | iOS 相机推理 | AVFoundation 接帧 + Core ML Vision 推理 + SwiftUI 展示 |
| 周四 | Instruments 性能分析 | 用 Instruments Time Profiler + Allocations 分析推理耗时和内存 |
| 周五 | Core ML 性能优化 | 开启 ANE（`computeUnits: .all`），对比 CPU-only / GPU / ANE 三种延迟 |
| 周六 | 双端性能对比表 | Android（ONNX Runtime）vs iOS（Core ML）：延迟/内存/功耗横向对比 |
| 周日 | 复盘 + 提交 | iOS Demo 推 GitHub，整理双端对比笔记，准备写博客 |

**本周产出**：iOS 实时推理 Demo + 双端跨平台性能对比表（重要简历素材）

**学习资源**：
- [Core ML 官方文档](https://developer.apple.com/machine-learning/core-ml/)
- [coremltools 转换指南](https://apple.github.io/coremltools/docs-guides/source/convert-pytorch-workflow.html)

---

### 第3阶段：深度优化与框架补位（W8-W9）

**阶段目标**：系统性能分析能力，了解 ExecuTorch 和 ncnn，具备"四框架选型"讲述能力

---

#### W8（5/18-5/24）：ExecuTorch + ncnn + 四框架横向对比

> **核心目标**：完成四框架（ONNX Runtime / LiteRT / ExecuTorch / ncnn）对比报告；**本周开始准备简历**

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | ExecuTorch 定位认知 | 了解 ExecuTorch 是 PyTorch Mobile 的官方替代；支持 AOT 编译，适合 Meta/PyTorch 生态 |
| 周二 | ExecuTorch 本地跑通 | 在 **macOS 桌面端**跑通 ExecuTorch Hello World（先跑通再说，移动端接入留作了解） |
| 周三 | ncnn 认知与接入 | 了解 ncnn（腾讯开源，国内华为/vivo/OPPO 大量使用）；跑通 ncnn Android demo |
| 周四 | 四框架生态对比 | 社区活跃度、模型支持范围、C++ API 易用性、国内外公司使用现状 |
| 周五 | 统一抽象层设计 | 思考：如果你设计跨框架推理 SDK，API 层和后端切换怎么实现 |
| 周六 | 写对比报告 | 四框架对比表：适用场景、优劣势、框架状态 |
| 周日 | 简历初稿 + 面试话术 | **开始写简历初稿**（参考第七章简历改造策略）；准备"你如何选推理框架"的完整回答 |

> **ExecuTorch 说明**：ExecuTorch 在 Android/iOS 上的接入配置相当复杂，需要编译工具链，一天内跑通移动端不现实。先在 macOS 桌面端跑通理解原理，能说清楚选型逻辑就够了。  
> **ncnn 重要性**：国内大厂（华为、荣耀、vivo、OPPO）内部项目很多用 ncnn，面试时提到会加分。

**必备面试回答**：
> "端侧推理框架我的选型逻辑：跨平台最通用选 ONNX Runtime（C++ API 完善，支持 Windows/Android/iOS/Linux）；Google 生态（Pixel 设备/Android TV）优先 LiteRT；需要 PyTorch 原生导出体验用 ExecuTorch；国内移动端项目很多用 ncnn（轻量、无依赖、国内优化好）。PyTorch Mobile 已废弃不再推荐，NNAPI 在 Android 15 后废弃，现在用 LiteRT GPU Delegate。"

**本周产出**：四框架横向对比报告（技术博客）+ 简历初稿

**学习资源**：
- [ExecuTorch 入门文档](https://docs.pytorch.org/executorch/stable/getting-started.html)
- [ncnn GitHub](https://github.com/Tencent/ncnn)
- [ncnn Android 快速上手](https://github.com/Tencent/ncnn/tree/master/examples)

---

#### W9（5/25-5/31）：系统性能优化与 Profiling

> **核心目标**：用工具找到真实性能瓶颈，做出"优化前后"的量化对比故事

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | ARM/GPU/NPU 架构梳理 | CPU/GPU/NPU 各自擅长的场景，NPU 延迟低但算子支持有限的原因 |
| 周二 | torch.profiler 使用 | 分析模型每层算子耗时，找出 Top 3 瓶颈层（用于 PC 端调试模型，再部署端侧） |
| 周三 | ONNX 图优化深挖 | 用 `onnxoptimizer` 做 Conv-BN 融合、常量折叠；对比优化前后节点数和推理速度 |
| 周四 | Android Perfetto 实战 | 用 Perfetto 分析 C++ 推理调用栈，找 CPU 占用热点；与 Android Studio Profiler 对比 |
| 周五 | 算子融合与 Delegate 选择 | Fused Attention、Conv-BN-ReLU 融合原理；GPU Delegate vs CPU 在不同模型结构下的选型 |
| 周六 | 多线程推理优化 | 设置 ORT `intra_op_num_threads`，测试不同线程数对延迟和功耗的影响 |
| 周日 | 写"性能优化手册" | 整理一份"我的端侧推理性能排查 SOP"，面试时可直接讲 |

```python
# torch.profiler 使用示例（PC 端调试模型结构瓶颈）
import torch
from torch.profiler import profile, record_function, ProfilerActivity

with profile(
    activities=[ProfilerActivity.CPU],
    record_shapes=True
) as prof:
    with record_function("model_inference"):
        output = model(input_data)

print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))
```

> **说明**：`torch.compile` 是服务端训练/推理加速工具，端侧部署通常是导出静态图后用推理引擎执行，不用 `torch.compile`。端侧性能优化的重点是 ONNX 图优化 + Delegate 选型 + 线程调度。

**本周产出**：优化前后量化对比数据 + 性能排查 SOP（可作为面试案例）

**学习资源**：
- [torch.profiler 官方教程](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)
- [onnxoptimizer GitHub](https://github.com/onnx/optimizer)
- [Android Perfetto 性能追踪](https://perfetto.dev/docs/quickstart/android-tracing)

---

### 第4阶段：项目深化与机器人铺垫（W10-W11）

**阶段目标**：完成端侧 LLM 项目（强化大模型标签），铺垫机器人方向知识，简历基本定稿

---

#### W10（6/1-6/7）：端侧 LLM 应用项目

> **核心目标**：在手机上跑起来一个小模型，证明你能做"大模型端侧应用"；简历本周定稿

**推荐方案（优先选 B，降低工程量）**：

**方案 B（推荐）：MLC LLM 快速接入**
- 工具：[MLC LLM](https://llm.mlc.ai/docs/deploy/android.html)（已帮你处理了绝大部分工程细节）
- Android + iOS 都跑通
- 重点：性能记录和优化，而不是从零工程化
- 指标目标：首字延迟（TTFT）< 1s，生成速度 > 5 tokens/s

**方案 A（进阶）：端侧本地 LLM 引擎（工程量较大，量力而行）**
- 技术栈：C++ + NDK + llama.cpp
- 模型：Qwen2.5-1.5B 做 INT4 量化（体积 <1GB）
- 功能：Android App 本地 LLM 对话，无网络，流式输出

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | 选方案 + 环境准备 | 根据自己进度选 A 或 B；配置依赖，下载量化模型 |
| 周二 | 本地推理接入 | Android 接入，验证模型可跑 |
| 周三 | 流式输出 | 实现 token-by-token 流式显示（类 ChatGPT 效果） |
| 周四 | KV Cache 理解 + 性能采集 | 理解 KV Cache 原理；记录 TTFT、tokens/s、内存峰值 |
| 周五 | README + Benchmark 表格 | 写 GitHub README，包含架构图 + 性能数据 + 使用说明 |
| 周六 | **简历定稿** | 把两个项目（W4 视觉推理 + W10 LLM）写进简历，确认指标数据 |
| 周日 | 博客发布 | 发布"如何在 Android 上跑通本地 LLM"技术博客 |

**本周产出**：端侧 LLM Demo（手机可跑，含性能报告）+ **简历定稿版**

**学习资源**：
- [MLC LLM Android 部署](https://llm.mlc.ai/docs/deploy/android.html)
- [MLC LLM iOS 部署](https://llm.mlc.ai/docs/deploy/ios.html)
- [llama.cpp GitHub（方案A）](https://github.com/ggerganov/llama.cpp)

---

#### W11（6/8-6/14）：具身智能机器人铺垫（LeRobot + ROS2）

> **核心目标**：建立具身智能基础认知，跑通 ROS2 仿真链路；这是你与其他端侧 AI 候选人的最大差异化

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | 具身智能概念建立 | 了解 VLA（Vision-Language-Action）、策略网络、具身 AI 全链路（感知→决策→控制） |
| 周二 | LeRobot 入门 | 阅读 HuggingFace LeRobot 文档，理解数据格式（LeRobotDataset）和预训练策略模型 |
| 周三 | ROS2 环境搭建 | 安装 ROS2 Humble，跑通 talker/listener 示例；了解 Topic/Service/Node 基本概念 |
| 周四 | ROS2 + Gazebo 仿真 | 用 **Gazebo Classic**（非 Isaac Sim）跑通 Turtlebot3 仿真，导航一个简单场景 |
| 周五 | 端侧推理与机器人的连接点 | 思考：手机端侧 AI 的推理能力，如何迁移到 Jetson/RK3588 等机器人控制器 |
| 周六 | 机器人公司 JD 调研 | 调研智元/宇树/银河通用/大疆的端侧工程师 JD，整理技能差距清单 |
| 周日 | 写方向规划文章 | 整理"从手机端 AI 到具身智能机器人"的技术路径文章（博客发布） |

> **说明**：Isaac Sim 需要高端 NVIDIA GPU 和大量硬盘空间，不适合本地开发环境。ROS2 + Gazebo Classic 是仿真入门的标准组合，资源消耗合理。

**本周产出**：ROS2 仿真 PoC（录屏）+ 机器人公司技能差距清单 + 技术路径博客

**学习资源**：
- [LeRobot 官方文档](https://huggingface.co/docs/lerobot)
- [ROS2 Humble 官方教程](https://docs.ros.org/en/humble/)
- [Turtlebot3 ROS2 仿真](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/)
- [NVIDIA GR00T N1 机器人基础模型](https://nvidianews.nvidia.com/news/nvidia-isaac-gr00t-n1-open-humanoid-robot-foundation-model-simulation-frameworks)

---

### 第5阶段：面试冲刺与投递（W12）

**阶段目标**：从"会做"变成"能拿 offer"

---

#### W12（6/15-6/21）：面试冲刺 + 批量投递

> 简历应在 W10 已定稿，本周不再改简历，只做面试强化和投递。

| 天 | 内容 | 具体任务 |
|----|------|---------|
| 周一 | 项目讲解稿打磨 | 每个项目准备 3 分钟口头讲解稿（背景、选型、难点、数据、收获） |
| 周二 | 高频八股强化 | 集中过下方"高频面试题"，能流利口述，不看稿 |
| 周三 | 系统设计题 | 练习"如何设计一个跨端 AI 推理 SDK"的系统设计题；练习"端侧 LLM 推理延迟优化" |
| 周四 | LeetCode 专项冲刺 | 集中刷 10 题高频题（数组/链表/树），复盘之前错题 |
| 周五 | 模拟面试 | 找朋友或录视频做 Mock Interview（1.5小时，含算法题+技术题+项目讲解） |
| 周六 | 定向投递 | 投递 20+ 目标岗位（字节/华为/荣耀/vivo/商汤/智元/宇树/百度/小米） |
| 周日 | 复盘迭代 | 根据面试反馈，补短板，调整投递策略 |

**注意**：第 8 周简历初稿出来后就可以开始投递，不要等 W12。边面边学，面试反馈是最好的学习信号。

---

## 五、高频面试题清单

### 基础原理类

1. INT8 量化的 Scale 和 Zero-point 是如何计算的？对称量化和非对称量化有什么区别？
2. PTQ 和 QAT 有什么区别？什么情况下必须用 QAT？
3. 剪枝和蒸馏分别是什么原理？与量化的应用场景有什么不同？
4. ONNX 是什么？为什么说它是端侧部署的中间格式标准？
5. Transformer 的 Attention 复杂度是 O(n²)，在端侧如何优化长序列推理？
6. KV Cache 是什么原理？能解决什么问题？为什么会占用大量内存？
7. 为什么端侧推理偏向 INT4/INT8 而非 FP16？
8. PyTorch Mobile 和 ExecuTorch 有什么关系？为什么要迁移？
9. NNAPI 被废弃后，Android 上的 AI 加速应该用什么？

### 工程实践类

1. 你如何选择在 Android 上用 CPU/GPU/NPU 跑推理？决策依据是什么？
2. ONNX Runtime、LiteRT、ExecuTorch、ncnn 四者如何选型？各自适合什么场景？
3. 模型从云端迁移到端侧，你会做哪些工程改造？
4. 推理延迟高，你会从哪些维度排查？（算子耗时 → 内存带宽 → Delegate 选择 → 线程配置）
5. ONNX 图优化有哪些常见手段？Conv-BN 融合的原理是什么？
6. 描述一次你做性能优化的经历，量化了哪些指标？（用你的 Android 经验回答）

### 开放题（结合你的背景）

1. 你的移动端背景对端侧 AI 开发有哪些帮助？  
   > 参考答案：我理解 ARM 内存模型、线程优先级调度、OOM 处理机制，这些在集成 AI 推理引擎时直接复用——用 `mmap` 加载大模型权重比 `malloc` 内存更高效，在 UI 线程调推理的风险我很清楚，ANR 的防护方式也是现成经验。

2. 你未来想往机器人方向发展，端侧 AI 和具身智能的技术连接点是什么？  
   > 参考答案：具身智能机器人的感知/决策/控制推理，同样需要在资源受限的嵌入式设备（如 Jetson/RK3588）上高效执行，本质和手机端侧 AI 是同一套工程问题：模型压缩、量化、延迟优化、实时性保障。手机端的 ONNX Runtime、量化、Profiling 经验可以直接迁移到机器人控制器，学习曲线远低于纯算法背景的人。

---

## 六、学习资源汇总

### 必读书籍

| 书名 | 用途 | 优先级 |
|------|------|:------:|
| 《现代C++教程》（开源，中文） | 激活 C++ 语法 | ⭐⭐⭐⭐⭐ |
| 《动手学深度学习》（李沐，开源） | 理解模型结构 | ⭐⭐⭐⭐ |

### 必刷 GitHub 项目

| 项目 | 学习点 |
|------|-------|
| [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) | C++ 推理引擎设计，量化实现 |
| [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) | 工业级推理引擎 C++ API |
| [pytorch/executorch](https://github.com/pytorch/executorch) | Meta 官方端侧 PyTorch 方案 |
| [Tencent/ncnn](https://github.com/Tencent/ncnn) | 国内成熟端侧框架，面试高频 |
| [pytorch/ao](https://github.com/pytorch/ao) | torchao 量化工具 |
| [onnx/optimizer](https://github.com/onnx/optimizer) | ONNX 图优化工具 |
| [huggingface/lerobot](https://github.com/huggingface/lerobot) | 机器人策略学习框架 |

### 视频课程

| 课程 | 平台 | 用途 |
|------|------|------|
| Andrej Karpathy - Zero to Hero | YouTube | 理解 LLM 原理 |
| MIT 6.5940 EfficientML | YouTube | 端侧 AI 专项（量化/剪枝/蒸馏） |
| 李沐《动手学深度学习》 | B站/YouTube | 中文深度学习入门 |

---

## 七、简历改造策略

### 标题改造

```
原来：高级移动端开发工程师（Android/iOS/RN）
改后：端侧 AI 应用开发工程师 | Android/iOS/C++/ONNX Runtime
```

### 核心技能加入

```
推理框架：ONNX Runtime、LiteRT、ncnn、ExecuTorch（了解）、llama.cpp
模型优化：INT8/INT4 量化（PTQ/QAT）、ONNX 图优化、模型压缩、KV Cache
硬件平台：ARM Cortex-A、Android GPU Delegate、Apple Core ML/ANE
工具链：torch.profiler、Netron、onnxoptimizer、Android Studio Profiler、Instruments、Perfetto
机器人方向：LeRobot、ROS2（了解）
```

### 工作经历改造（取自你的 Android 背景）

| 原描述 | AI 化改写 |
|--------|---------|
| "优化了 App 启动时 .so 库加载时序" | "具备 Native 库按需加载经验，可类比优化端侧 AI 引擎的动态加载策略" |
| "解决了内存泄漏问题" | "掌握 Android 内存生命周期管理，可保障大模型推理时的内存安全" |
| "优化 App 性能，减少 ANR" | "掌握多线程与主线程隔离，端侧推理引擎接入时直接复用该经验" |
| "接入过第三方 SDK" | "具备 C++ 推理库 JNI 封装经验（AAR/Framework 形式），理解端侧 SDK 接入全流程" |

### 项目描述模板

```
项目名称：端侧实时视觉推理 App（Android/iOS 双端）
技术栈：C++ / NDK / ONNX Runtime / LiteRT / Core ML
核心成果：
  · 实现 Android/iOS 双端本地 AI 推理，无需网络请求
  · 通过 INT8 PTQ 量化将模型体积降低 75%，推理延迟从 180ms 降至 52ms
  · 接入 GPU Delegate，帧率从 8fps 提升至 28fps
  · 使用 Perfetto + Android Profiler 定位并修复 3 处推理热点
```

---

## 八、投递策略

| 策略 | 说明 |
|------|------|
| 主投岗位 | `端侧AI开发工程师`、`端侧推理优化工程师`、`AI SDK工程师`、`移动端AI工程师` |
| 目标公司（手机端/AI） | 字节跳动、华为、荣耀、vivo、OPPO、小米（澎湃AI）、百度、商汤、旷视 |
| 目标公司（机器人） | 智元机器人、宇树科技、大疆、银河通用、傅利叶智能、追觅科技 |
| 暂缓投递 | 编译器类、AI Infra 架构师类（10年+管理岗） |
| 投递时机 | **第 8 周**简历初稿出来后就开始投，不等 W12 |
| 简历叙事主线 | "我不是转行新人，我是把 AI 落到端上的工程化专家" |
| 人脉建设 | 加入端侧AI/机器人相关社区（GitHub issue 参与、掘金/知乎活跃）；面试官可能就是你博客的读者 |

---

## 九、三个月后自测清单

完成以下所有检查项，即达到面试竞争力：

**技术能力**
- [ ] 能从头将 PyTorch 模型导出 ONNX，并在 Android 上通过 C++ 跑通推理
- [ ] 能清晰解释 PTQ 和 QAT 的区别，说出 Scale/Zero-point 的计算方式
- [ ] 知道剪枝和蒸馏的定义和应用场景（无需动手实现）
- [ ] 动手做过 INT8/INT4 量化实验，有 CV 模型和 LLM 各一组对比数据
- [ ] 用过 torch.profiler 找到模型瓶颈层；用过 Perfetto 分析 Android C++ 热点
- [ ] iOS 侧用 Core ML 跑通过推理，能说出 ANE / GPU / CPU 的区别
- [ ] 能说清楚 ONNX Runtime / LiteRT / ExecuTorch / ncnn 四者的定位和选型理由
- [ ] 知道 PyTorch Mobile 已废弃（→ ExecuTorch），NNAPI 已废弃（→ LiteRT GPU Delegate）
- [ ] 了解 ONNX 图优化常见手段（Conv-BN 融合、常量折叠）

**项目产出**
- [ ] GitHub 上有端侧视觉推理项目（Android/iOS，含 README 和 Benchmark 数据）
- [ ] GitHub 上有端侧 LLM 项目（含首字延迟 TTFT、tokens/s、内存数据）
- [ ] 发布过至少 3 篇端侧 AI 技术博客（掘金/知乎）
- [ ] LeetCode 累计做题 50 题，掌握高频题型

**求职准备**
- [ ] 简历标题和技能栏已 AI 化，工作经历已用端侧 AI 视角重新表述
- [ ] 每个项目准备好 3 分钟口头讲解稿（背景/选型/难点/数据）
- [ ] 准备好"为什么适合端侧AI"和"未来怎么进机器人行业"的完整回答
- [ ] 了解 ROS2 基础，能解释具身智能和端侧 AI 的技术连接点

---

## 十、风险缓冲机制

> 任何计划都会遇到卡壳，提前想好处理方案。

| 风险场景 | 处理方案 |
|---------|---------|
| W4 Android 接入卡住超过 2 天 | 先用 Python ONNX Runtime Demo 代替，Android 接入降级为"了解级"，继续推进 W5 |
| W5 Qwen2.5-1.5B 量化内存不足 | 改用 Phi-3-mini-4k（更小），或直接用 llama.cpp 的预量化模型跳过量化步骤 |
| W7 iOS 真机证书/环境问题 | 用模拟器替代真机，延迟数据标注为"模拟器测试"，面试时说明 |
| W8 ExecuTorch 接入卡住 | 降级为"阅读源码 + 理解架构"，不强求本地跑通 |
| W11 ROS2 仿真环境跑不起来 | 改为"LeRobot 数据集和策略网络的概念理解 + 录屏 Demo 代替仿真" |
| 某周任务做了 50% 没完成 | 不要拖到下周，标记完成状态，继续推进。**完成 80% 的计划远好于推迟 100% 的计划** |

---

## 十一、从端侧 AI 到具身智能机器人：进阶路线图

```
当前（2026年3月）
  ↓  3个月
[端侧AI工程师]  ← 3个月目标：拿到手机端 AI offer
  ↓  6-12个月实战经验
[端侧AI Infra 工程师]  ← 积累真实优化案例 + 机器人认知
  ↓  结合机器人方向经验
[具身智能机器人端侧工程师]  ← 终极目标
  （感知推理 / 嵌入式部署 / VLA 模型落地）
```

**从手机 AI 到机器人 AI，技术迁移点**：

| 手机端 AI | 机器人端 AI | 迁移难度 |
|---------|-----------|:-------:|
| ONNX Runtime / LiteRT / ncnn 推理 | 嵌入式 SoC（Jetson/RK3588）上的推理引擎 | 低 |
| INT8/INT4 量化 | 机器人感知模型量化（视觉/点云/多模态） | 低 |
| CPU/GPU/NPU 调度优化 | Jetson GPU / 高通 QCM 等边缘 AI 芯片调度 | 中 |
| 内存/延迟优化 | 实时控制环路（< 10ms）延迟优化 | 中 |
| 端侧 LLM 推理 | VLA（视觉-语言-动作）模型推理 | 中高 |
| Android/iOS 工程化 | ROS2 节点工程化 | 中高 |

---

*制定时间：2026年3月25日*  
*版本：v2.0（职业规划师完整 Review 版）*  
*目标岗位：端侧AI开发工程师 → 具身智能机器人端侧工程师*
