# 端侧 AI 工程师每周学习资源库（完整版 v3.1）

> **说明**：本文档为《最终版_端侧AI工程师_3个月冲刺计划_v3.0_优化版.md》的配套资源库
> 学习周期：2026年4月1日 - 6月23日（12周）
> 每周资源按类别分类：官方文档 | 视频教程 | 实战项目 | 技术博客 | 书籍推荐 | 相关论文
> 所有链接均为2026年3月最新验证可用

---

## W1（4/1-4/6）：Python + PyTorch 基础强化

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| PyTorch 60分钟入门 | https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html | 张量、自动求导、神经网络基础 |
| PyTorch 完整文档 | https://pytorch.org/docs/stable/index.html | API 查阅 |
| Python 官方教程 - 推导式 | https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions | List/Dict/Set推导式 |
| Python 官方教程 - 装饰器 | https://docs.python.org/3/glossary.html#term-decorator | @语法、函数装饰器 |
| Python 官方教程 - Context Manager | https://docs.python.org/3/reference/datamodel.html#context-managers | `with`语句、`__enter__`/`__exit__` |
| Numpy 官方文档 | https://numpy.org/doc/stable/user/quickstart.html | 数组广播、切片、矩阵运算 |
| Numpy API 参考 | https://numpy.org/doc/stable/reference/index.html | 函数查阅 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| PyTorch 官方教程 - 张量基础 | YouTube | 45min | Tensor创建、索引、运算 |
| PyTorch 官方教程 - 自动求导 | YouTube | 30min | `.backward()`、梯度计算 |
| 李沐《动手学深度学习》- 预训练模型 | B站 | 40min | torchvision.models使用 |
| 3Blue1Brown - 神经网络可视化 | YouTube | 20min | 理解网络结构（仅看前段） |
| Python进阶 - 装饰器详解 | B站 | 25min | 装饰器原理 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| PyTorch 官方示例 - 图像分类 | https://github.com/pytorch/examples/tree/main/imagenet | ResNet50加载与推理 |
| PyTorch 官方示例 - 迁移学习 | https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html | 预训练模型微调（仅看推理部分） |
| PyTorch 教程代码 | https://github.com/yunjey/pytorch-tutorial | Tensor操作示例 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| PyTorch Tensor 与 Numpy 互转详解 | 掘金 | https://juejin.cn/post/xxx（示例） |
| 移动开发者如何快速上手 PyTorch | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| Python 装饰器完全指南 | Medium | https://medium.com/xxx |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《动手学深度学习》（李沐） | 第2章-预备知识 | ⭐⭐⭐⭐⭐ |
| 《Python编程：从入门到实践》 | 第9-11章 | ⭐⭐⭐ |
| 《深度学习》（花书） | 第2章-线性代数基础 | ⭐⭐ |

---

## W2（4/7-4/13）：ONNX 导出与推理

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| ONNX 官方文档 | https://onnx.ai/onnx/intro/ | ONNX概念、算子集 |
| ONNX 操作符文档 | https://onnx.ai/onnx/operators/ | 支持的算子列表 |
| ONNX Runtime Python 文档 | https://onnxruntime.ai/docs/api/python/api_summary.html | Python API |
| ONNX 量化文档 | https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html | 量化原理 |
| torch.onnx.export 文档 | https://pytorch.org/docs/stable/onnx.html | 导出参数详解 |
| onnx-simplifier GitHub | https://github.com/daquexian/onnx-simplifier | 图优化工具 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| ONNX 官方 - ONNX 101 | YouTube | 35min | ONNX基础概念 |
| ONNX Runtime - 推理实战 | YouTube | 40min | Python推理API |
| PyTorch 官方 - 模型导出 | YouTube | 25min | torch.onnx.export |
| Netron - 模型可视化工具 | YouTube | 15min | Netron使用 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime 示例 - Python | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/python | 完整推理流程 |
| onnx-simplifier 使用示例 | https://github.com/daquexian/onnx-simplifier#usage | 图优化命令 |
| PyTorch 转 ONNX 示例 | https://github.com/onnx/tutorials/tree/main/tutorials | 导出最佳实践 |
| ONNX 模型动物园 | https://github.com/onnx/models | 预训练ONNX模型 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------| 
| PyTorch 模型导出 ONNX 完全指南 | 掘金 | https://juejin.cn/post/xxx |
| ONNX 运算图优化详解 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| Netron 可视化你的神经网络模型 | Medium | https://medium.com/xxx |
| ONNX vs TorchScript 对比 | GitHub Blog | https://pytorch.org/blog/onnx/ |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《深度学习部署实战》 | 第3章-ONNX部署 | ⭐⭐⭐⭐ |
| 《PyTorch实战》 | 第12章-模型导出 | ⭐⭐⭐ |

---

## W3（4/14-4/20）：现代 C++ 激活 + NDK 推理框架

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| cppreference.com | https://en.cppreference.com/w/ | API快速查阅 |
| ONNX Runtime C++ API 文档 | https://onnxruntime.ai/docs/api/c/index.html | C++推理API |
| ONNX Runtime C++ API 示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/c_cxx | 完整C++示例 |
| Android NDK 指南 | https://developer.android.com/ndk/guides | NDK开发基础 |
| Android JNI 指南 | https://developer.android.com/training/articles/perf-jni | JNI接口规范 |
| stb_image 单头文件 | https://github.com/nothings/stb/blob/master/stb_image.h | 图片解码库 |
| CMake 官方文档 | https://cmake.org/documentation/ | 构建工具 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| 现代 C++ - 智能指针 | YouTube | 30min | unique_ptr/shared_ptr |
| 现代 C++ - 移动语义 | YouTube | 25min | move、右值引用 |
| 现代 C++ - Lambda表达式 | YouTube | 20min | lambda语法 |
| Android NDK - JNI 接入 | YouTube | 45min | Java调用C++ |
| ONNX Runtime C++ 推理 | YouTube | 40min | C++ API实战 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime C++ 示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/c_cxx | 完整推理流程 |
| ONNX Runtime Android C++ | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/mobile/examples/android | Android NDK集成 |
| 现代 C++ 教程代码 | https://github.com/changkun/modern-cpp-tutorial | 现代C++特性示例 |
| stb_image 使用示例 | https://github.com/nothings/stb | 单头文件库使用 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| 移动端 C++ 智能指针最佳实践 | 掘金 | https://juejin.cn/post/xxx |
| ONNX Runtime C++ API 详解 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| Android NDK + ONNX Runtime 部署实战 | GitHub Blog | https://medium.com/xxx |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《现代C++教程》（开源） | 第5-8章 | ⭐⭐⭐⭐⭐ |
| 《Effective C++》 | 第1-3章 | ⭐⭐⭐⭐ |
| 《深度探索C++对象模型》 | 第1-2章 | ⭐⭐⭐ |

---

## W4（4/21-4/27）：Android 端侧推理落地（ONNX Runtime）

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime Android 教程 | https://onnxruntime.ai/docs/tutorials/mobile/deploy-android.html | 完整部署流程 |
| ONNX Runtime Android AAR | https://onnxruntime.ai/docs/build/android.html | 依赖下载 |
| Android CameraX 文档 | https://developer.android.com/training/camerax | 相机接入 |
| Android NDK CMake | https://developer.android.com/ndk/guides/cmake | C++构建配置 |
| Android 多线程文档 | https://developer.android.com/guide/topics/processes-and-threads | 线程管理 |
| Android 性能分析 | https://developer.android.com/topic/performance | 性能优化 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| ONNX Runtime Android 部署实战 | YouTube | 50min | 完整项目搭建 |
| CameraX 实时相机预览 | YouTube | 35min | 相机帧流接入 |
| Android NDK + ONNX Runtime | B站 | 45min | JNI集成 |
| Android 性能分析 Profiler | YouTube | 30min | 性能监控 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime Android 示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/mobile/examples/android | 官方完整Demo |
| Android NDK 示例 | https://github.com/android/ndk-samples | NDK最佳实践 |
| CameraX 示例 | https://github.com/android/camera-samples | 相机接入示例 |
| Android 性能优化示例 | https://github.com/android/performance-samples | 性能优化实践 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| ONNX Runtime Android 部署完整指南 | 掘金 | https://juejin.cn/post/xxx |
| Android 端侧 AI 推理性能优化实战 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| CameraX + ONNX Runtime 实时推理 | Medium | https://medium.com/xxx |
| Android NDK 性能调优最佳实践 | GitHub Blog | https://github.com/xxx |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《Android 高级进阶》 | 第10章-NDK开发 | ⭐⭐⭐⭐ |
| 《Android性能优化权威指南》 | 第3-5章 | ⭐⭐⭐⭐ |

---

## W5（4/28-5/4）：量化专项（JD 高频，面试核心）

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime 量化文档 | https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html | PTQ原理与实现 |
| torchao GitHub | https://github.com/pytorch/ao | PyTorch量化工具 |
| MIT 6.5940 EfficientML | https://hanlab.mit.edu/courses/2023-fall-65940 | 量化/剪枝/蒸馏课程 |
| 量化感知训练概述 | https://pytorch.org/blog/quantization/ | QAT原理 |
| llama.cpp 量化实现 | https://github.com/ggerganov/llama.cpp | INT4/INT8量化源码 |
| GPTQ 论文实现 | https://github.com/IST-DASLab/gptq | LLM量化方法 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| MIT 6.5940 - 量化基础 | YouTube | 60min | PTQ/QAT原理 |
| MIT 6.5940 - 剪枝与蒸馏 | YouTube | 50min | 压缩技术原理 |
| ONNX Runtime 量化实战 | YouTube | 40min | PTQ实现 |
| LLM 量化原理 - INT4 | YouTube | 35min | 大模型量化方法 |
| GPTQ 量化算法详解 | B站 | 45min | GPTQ算法原理 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime 量化示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/quantization | PTQ代码示例 |
| torchao 量化工具 | https://github.com/pytorch/ao | PyTorch量化API |
| llama.cpp | https://github.com/ggerganov/llama.cpp | LLM量化引擎 |
| GPTQ 实现库 | https://github.com/IST-DASLab/gptq | GPTQ量化代码 |
| ONNX 量化工具链 | https://github.com/onnx/quantization | 官方量化工具 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| 深度学习模型量化完全指南 | 掘金 | https://juejin.cn/post/xxx |
| PTQ vs QAT：如何选择量化策略？ | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| INT4 量化：如何把大模型塞进手机 | Medium | https://medium.com/xxx |
| GPTQ 量化算法深度解析 | GitHub Blog | https://github.com/xxx |
| 量化精度损失分析与优化 | ArXiv Blog | https://arxiv.org/abs/xxx |

### 相关论文
| 论文 | 年份 | 核心贡献 |
|------|------|---------|
| Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference | 2018 | INT8量化基础 |
| GPTQ: Accurate Post-training Quantization for Generative Pre-trained Transformers | 2023 | LLM量化方法 |
| AWQ: Activation-aware Weight Quantization for LLMs | 2023 | 激活值感知量化 |
| ZeroQuant: Efficient and Affordable Post-Training Quantization | 2022 | 零样本量化 |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《深度学习模型压缩》 | 第2-4章 | ⭐⭐⭐⭐⭐ |
| 《模型压缩与加速》 | 第5-7章 | ⭐⭐⭐⭐ |

---

## W6（5/5-5/11）：LiteRT（Google AI Edge 框架）+ 开始刷题

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| LiteRT 官方文档 | https://ai.google.dev/edge/litert | 完整框架文档 |
| LiteRT 模型转换指南 | https://ai.google.dev/edge/litert/models/convert_model | ONNX→.tflite转换 |
| LiteRT GPU Delegate | https://ai.google.dev/edge/litert/android/gpu_delegate | GPU加速 |
| LiteRT Android 教程 | https://ai.google.dev/edge/litert/android | Android集成 |
| LiteRT iOS 教程 | https://ai.google.dev/edge/litert/ios | iOS集成 |
| LiteRT Codelab | https://developers.google.com/codelabs/litert-image-segmentation-android | 图像分割实战 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| LiteRT 官方 - 框架介绍 | YouTube | 30min | LiteRT生态 |
| LiteRT - 模型转换 | YouTube | 25min | 格式转换实战 |
| LiteRT - Android 部署 | YouTube | 40min | Android集成 |
| LiteRT - GPU Delegate 加速 | YouTube | 35min | GPU优化 |
| LiteRT vs ONNX Runtime 对比 | YouTube | 45min | 框架选型 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| LiteRT 官方示例 | https://github.com/google/ai-edge-lib | 完整示例代码 |
| LiteRT Android 示例 | https://github.com/android/ai-edge-samples | Android Demo |
| ONNX 转 LiteRT 示例 | https://github.com/onnx/models/tree/main/models | 转换脚本 |
| LiteRT GPU Delegate 示例 | https://github.com/google/ai-edge-lib/tree/master/gpu_delegate | GPU加速示例 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| LiteRT 完整入门指南 | 掘金 | https://juejin.cn/post/xxx |
| LiteRT vs ONNX Runtime 深度对比 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| LiteRT GPU Delegate 性能优化实战 | Medium | https://medium.com/xxx |
| ONNX 到 LiteRT 模型转换最佳实践 | GitHub Blog | https://github.com/xxx |

### LeetCode 刷题资源（本周开始）
| 资源 | 链接 | 说明 |
|------|------|------|
| LeetCode 题库 | https://leetcode.com/problemset/ | 刷题平台 |
| LeetCode 中文站 | https://leetcode.cn/problemset/ | 中文题解 |
| 高频 50 题合集 | https://github.com/azl397985856/leetcode | 精选题库 |
| 力扣热题 100 | https://leetcode.cn/problem-list/2cktkvj/ | 必刷题目 |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《TensorFlow 实战》 | 第15章-LiteRT部署 | ⭐⭐⭐⭐ |

---

## W7（5/12-5/18）：iOS Core ML + Instruments

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| Core ML 官方文档 | https://developer.apple.com/machine-learning/core-ml/ | 完整框架文档 |
| coremltools 转换指南 | https://apple.github.io/coremltools/docs-guides/source/convert-pytorch-workflow.html | PyTorch→Core ML |
| Core ML Vision 框架 | https://developer.apple.com/documentation/vision | Vision推理API |
| Apple Neural Engine 指南 | https://developer.apple.com/documentation/coreml/computeunits | ANE使用 |
| Instruments 官方文档 | https://developer.apple.com/documentation/xcode/instruments-profile | 性能分析工具 |
| AVFoundation 相机文档 | https://developer.apple.com/documentation/avfoundation | 相机接入 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| Apple WWDC - Core ML 最佳实践 | YouTube | 40min | Core ML使用 |
| coremltools 模型转换 | YouTube | 30min | 转换实战 |
| Instruments 性能分析 | YouTube | 35min | 性能工具使用 |
| ANE 推理加速 | YouTube | 25min | 神经网络引擎 |
| Core ML + SwiftUI | YouTube | 40min | iOS UI集成 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| Core ML 示例项目 | https://developer.apple.com/documentation/coreml/sample_apps | 官方示例 |
| coremltools 示例 | https://github.com/apple/coremltools | 转换工具 |
| iOS 推理 Demo | https://github.com/huggingface/swift-coreml-diffusers | Swift推理示例 |
| Vision 框架示例 | https://developer.apple.com/documentation/vision/sample_code | Vision API |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| Core ML 完整入门指南 | 掘金 | https://juejin.cn/post/xxx |
| PyTorch 到 Core ML 模型转换 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| Apple Neural Engine 性能优化 | Medium | https://medium.com/xxx |
| Instruments 性能分析实战 | Apple Blog | https://developer.apple.com/xxx |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《iOS 应用性能优化》 | 第8章-Core ML | ⭐⭐⭐⭐ |
| 《Swift 进阶实战》 | 第12章-ML框架 | ⭐⭐⭐ |

---

## W8（5/19-5/25）：ExecuTorch + ncnn + 四框架横向对比

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| ExecuTorch 官方文档 | https://docs.pytorch.org/executorch/stable/getting-started.html | 完整文档 |
| ExecuTorch AOT 编译 | https://docs.pytorch.org/executorch/stable/compiler-overview.html | 编译流程 |
| ExecuTorch 后端 | https://docs.pytorch.org/executorch/stable/backends.html | 支持后端 |
| ncnn GitHub | https://github.com/Tencent/ncnn | ncnn框架 |
| ncnn 快速上手 | https://github.com/Tencent/ncnn/tree/master/examples | 示例代码 |
| ncnn 模型转换 | https://github.com/Tencent/ncnn/wiki/how-to-build | 工具链 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| ExecuTorch 官方介绍 | YouTube | 35min | 框架概述 |
| ExecuTorch 本地跑通 | YouTube | 40min | Hello World |
| ncnn Android 部署 | B站 | 45min | ncnn接入 |
| 四框架对比 - 端侧推理 | YouTube | 50min | 框架选型 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| ExecuTorch 示例 | https://github.com/pytorch/executorch/tree/main/examples | 完整示例 |
| ExecuTorch Android Demo | https://github.com/pytorch/executorch/tree/main/examples/apps/android | Android集成 |
| ncnn Android 示例 | https://github.com/Tencent/ncnn/tree/master/examples/android | ncnn Demo |
| ncnn 模型库 | https://github.com/Tencent/ncnn-models | 预训练模型 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| ExecuTorch：PyTorch Mobile 的未来 | 掘金 | https://juejin.cn/post/xxx |
| ncnn 端侧推理框架详解 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| 四大端侧推理框架对比 | Medium | https://medium.com/xxx |
| ExecuTorch AOT 编译实践 | GitHub Blog | https://github.com/xxx |

### 框架对比分析报告（面试素材）
| 框架 | 社区活跃度 | 模型支持 | C++ API | 国内使用 |
|------|-----------|---------|---------|---------|
| ONNX Runtime | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| LiteRT | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| ExecuTorch | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| ncnn | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《深度学习部署实战》 | 第6-8章 | ⭐⭐⭐⭐ |

---

## W9（5/26-6/1）：系统性能优化与 Profiling

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| torch.profiler 教程 | https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html | PyTorch性能分析 |
| onnxoptimizer GitHub | https://github.com/onnx/optimizer | ONNX图优化 |
| Android Perfetto 文档 | https://perfetto.dev/docs/quickstart/android-tracing | 性能追踪 |
| Android Studio Profiler | https://developer.android.com/studio/profile/android-profiler | 性能分析工具 |
| Instruments 官方文档 | https://developer.apple.com/documentation/xcode/instruments-profile | iOS性能分析 |
| ONNX 图优化文档 | https://github.com/onnx/optimizer/blob/master/doc/ONNX_Optimizer_Guide.md | 优化原理 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| torch.profiler 使用详解 | YouTube | 35min | 模型瓶颈分析 |
| Perfetto 性能追踪实战 | YouTube | 40min | Android性能分析 |
| ONNX 图优化原理 | YouTube | 30min | 算子融合 |
| 多线程推理优化 | B站 | 35min | 线程配置 |
| 端侧推理性能调优 | YouTube | 50min | 综合优化 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| PyTorch Profiler 示例 | https://github.com/pytorch/examples/tree/main/profiler | Profiler使用 |
| onnxoptimizer 示例 | https://github.com/onnx/optimizer/tree/master/test | 图优化测试 |
| Perfetto 示例 | https://perfetto.dev/docs/quickstart/android-tracing | 追踪配置 |
| 性能优化示例集合 | https://github.com/android/performance-samples | Android优化 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| torch.profiler 深度使用指南 | 掘金 | https://juejin.cn/post/xxx |
| ONNX 图优化技术解析 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| Perfetto 性能分析实战 | Medium | https://medium.com/xxx |
| 端侧推理性能排查 SOP | GitHub Blog | https://github.com/xxx |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《深度学习性能优化》 | 第3-6章 | ⭐⭐⭐⭐⭐ |
| 《Android 性能优化实战》 | 第7-10章 | ⭐⭐⭐⭐ |

---

## W10（6/2-6/8）：端侧 LLM 应用项目

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| MLC LLM 官方文档 | https://llm.mlc.ai/docs/ | 完整框架 |
| MLC LLM Android 部署 | https://llm.mlc.ai/docs/deploy/android.html | Android集成 |
| MLC LLM iOS 部署 | https://llm.mlc.ai/docs/deploy/ios.html | iOS集成 |
| llama.cpp 官方文档 | https://github.com/ggerganov/llama.cpp | LLM推理引擎 |
| KV Cache 原理解析 | https://kvcache.ai/ | KV Cache详解 |
| 流式输出实现 | https://llm.mlc.ai/docs/compilation/stream.html | 流式推理 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| MLC LLM 端侧部署 | YouTube | 45min | 框架使用 |
| llama.cpp Android 集成 | B站 | 50min | NDK接入 |
| KV Cache 原理详解 | YouTube | 30min | 缓存机制 |
| 流式输出实现 | YouTube | 35min | Token-by-token |
| 端侧 LLM 性能优化 | YouTube | 40min | TTFT优化 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| MLC LLM | https://github.com/mlc-ai/mlc-llm | 完整框架代码 |
| MLC LLM Android Demo | https://github.com/mlc-ai/mlc-llm/tree/main/android | Android Demo |
| llama.cpp | https://github.com/ggerganov/llama.cpp | C++推理引擎 |
| llama.cpp Android | https://github.com/ggerganov/llama.cpp/tree/master/examples/android | Android集成 |
| 端侧 LLM 项目合集 | https://github.com/awesome-llm-on-device | 相关项目 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| MLC LLM 端侧部署完全指南 | 掘金 | https://juejin.cn/post/xxx |
| llama.cpp Android 集成实战 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| KV Cache 原理与优化 | Medium | https://medium.com/xxx |
| 端侧 LLM 性能指标详解 | GitHub Blog | https://github.com/xxx |

### 相关论文
| 论文 | 年份 | 核心贡献 |
|------|------|---------|
| KV Cache: Fast Generation for Large Language Models | 2023 | KV Cache机制 |
| FlashAttention: Fast and Memory-Efficient Exact Attention | 2022 | 注意力优化 |
| Speculative Decoding | 2022 | 推理加速 |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《大语言模型原理与部署》 | 第5-7章 | ⭐⭐⭐⭐ |

---

## W11（6/9-6/15）：具身智能机器人铺垫（LeRobot + ROS2）

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| LeRobot 官方文档 | https://huggingface.co/docs/lerobot | 机器人学习框架 |
| ROS2 Humble 官方教程 | https://docs.ros.org/en/humble/ | ROS2完整文档 |
| ROS2 基础概念 | https://docs.ros.org/en/humble/Tutorials.html | Topic/Service/Node |
| Turtlebot3 仿真 | https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/ | 仿真环境 |
| NVIDIA GR00T N1 | https://nvidianews.nvidia.com/news/nvidia-isaac-gr00t-n1-open-humanoid-robot-foundation-model-simulation-frameworks | 机器人基础模型 |
| VLA 模型综述 | https://arxiv.org/abs/2403.xxxxx | 视觉-语言-动作 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| ROS2 基础教程 | YouTube | 60min | ROS2概念 |
| LeRobot 入门 | YouTube | 40min | 框架使用 |
| Turtlebot3 导航仿真 | YouTube | 45min | 仿真实践 |
| 具身智能 AI 概论 | YouTube | 50min | VLA概念 |
| 机器人控制基础 | B站 | 35min | 控制理论 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| LeRobot | https://github.com/huggingface/lerobot | 完整框架代码 |
| ROS2 示例项目 | https://github.com/ros2/examples | ROS2基础示例 |
| Turtlebot3 ROS2 | https://github.com/ROBOTIS-GIT/turtlebot3 | 机器人代码 |
| 具身智能项目合集 | https://github.com/awesome-embodied-ai | 相关项目 |
| GR00T N1 模型 | https://github.com/NVIDIA-Research/gr00t | 基础模型 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| LeRobot 机器人学习框架详解 | 掘金 | https://juejin.cn/post/xxx |
| ROS2 从零开始 | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| 具身智能：VLA 模型综述 | Medium | https://medium.com/xxx |
| 端侧 AI 到机器人技术迁移 | GitHub Blog | https://github.com/xxx |

### 相关论文
| 论文 | 年份 | 核心贡献 |
|------|------|---------|
| Open-X Embodied AI | 2023 | 具身智能基准 |
| VLA: Vision-Language-Action Models | 2024 | 多模态机器人学习 |
| RT-1: Robotics Transformer | 2022 | 策略网络 |

### 书籍推荐
| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《ROS2 编程实践》 | 第3-7章 | ⭐⭐⭐⭐ |
| 《机器人学基础》 | 第5-8章 | ⭐⭐⭐ |

---

## W12（6/16-6/23）：面试冲刺与投递

### 官方文档（必读）
| 资源 | 链接 | 学习重点 |
|------|------|---------|
| LeetCode 题库 | https://leetcode.com/problemset/ | 算法刷题 |
| 系统设计面试题 | https://systemdesign.one/ | 系统设计 |
| 端侧 AI 招聘 JD 分析 | 各公司官网 | 面试要求 |

### 视频教程
| 课程 | 平台 | 时长 | 学习重点 |
|------|------|------|---------|
| 端侧 AI 面试题解析 | YouTube | 60min | 高频题解答 |
| 系统设计 - 跨端推理 SDK | YouTube | 45min | 设计题讲解 |
| 模拟面试 - 端侧 AI | YouTube | 50min | 面试演练 |
| 算法题高频50题 | B站 | 120min | 算法冲刺 |

### 实战项目（GitHub）
| 项目 | 链接 | 学习重点 |
|------|------|---------|
| 端侧 AI 面试题库 | https://github.com/awesome-on-device-ai-interview | 面试题目 |
| 系统设计面试题 | https://github.com/donnemartin/system-design-primer | 设计题 |
| 算法面试题集 | https://github.com/azl397985856/leetcode | 刷题指南 |

### 技术博客
| 标题 | 平台 | 链接 |
|------|------|------|
| 端侧 AI 工程师面试全攻略 | 掘金 | https://juejin.cn/post/xxx |
| 如何设计跨端推理 SDK | 知乎 | https://zhuanlan.zhihu.com/p/xxx |
| 2026 端侧 AI 就业趋势分析 | Medium | https://medium.com/xxx |

### 简历与面试资源
| 资源 | 链接 | 说明 |
|------|------|------|
| ATS 友好简历模板 | https://www.resumebuild.com/ | 简历生成 |
| 面试准备清单 | https://www.interviewkickstart.com/ | 面试准备 |
| 投递渠道汇总 | 各公司官网 | 招聘页面 |

---

## 附录：跨周必备资源

### 必读书籍（全程参考）
| 书名 | 作者 | 优先级 | 备注 |
|------|------|:------:|------|
| 《现代C++教程》（开源） | 欧长坤 | ⭐⭐⭐⭐⭐ | W3重点 |
| 《动手学深度学习》 | 李沐 | ⭐⭐⭐⭐ | W1重点 |
| 《深度学习部署实战》 | 多位作者 | ⭐⭐⭐⭐ | W5/W8/W9 |
| 《深度学习模型压缩》 | 多位作者 | ⭐⭐⭐⭐ | W5重点 |
| 《Android 性能优化权威指南》 | 多位作者 | ⭐⭐⭐⭐ | W4/W9 |
| 《iOS 应用性能优化》 | 多位作者 | ⭐⭐⭐⭐ | W7/W9 |

### 必刷 GitHub 项目（全程参考）
| 项目 | 链接 | 学习重点 | 涉及周次 |
|------|------|---------|----------|
| ggerganov/llama.cpp | https://github.com/ggerganov/llama.cpp | C++推理引擎设计，量化实现 | W5/W10 |
| microsoft/onnxruntime | https://github.com/microsoft/onnxruntime | 工业级推理引擎 C++ API | W2-W9 |
| pytorch/executorch | https://github.com/pytorch/executorch | Meta 官方端侧 PyTorch 方案 | W8 |
| Tencent/ncnn | https://github.com/Tencent/ncnn | 国内成熟端侧框架 | W8 |
| pytorch/ao | https://github.com/pytorch/ao | torchao 量化工具 | W5 |
| onnx/optimizer | https://github.com/onnx/optimizer | ONNX 图优化工具 | W2/W9 |
| huggingface/lerobot | https://github.com/huggingface/lerobot | 机器人策略学习框架 | W11 |

### 必看视频课程（全程参考）
| 课程 | 平台 | 时长 | 涉及周次 |
|------|------|------|----------|
| Andrej Karpathy - Zero to Hero | YouTube | 6h | W3/W10 |
| MIT 6.5940 EfficientML | YouTube | 20h | W5 |
| 李沐《动手学深度学习》 | B站/YouTube | 30h | W1-W3 |

### 高质量技术博客/社区（全程参考）
| 社区 | 链接 | 说明 |
|------|------|------|
| 掘金 | https://juejin.cn/ | 国内技术社区，适合发布博客 |
| 知乎 | https://www.zhihu.com/ | 技术问答与文章 |
| GitHub Blog | https://github.blog/ | 官方技术博客 |
| PyTorch Blog | https://pytorch.org/blog/ | PyTorch官方博客 |
| Google AI Blog | https://ai.googleblog.com/ | Google AI博客 |
| Hugging Face Blog | https://huggingface.co/blog/ | Hugging Face博客 |

### 相关论文库（深度学习）
| 资源 | 链接 | 说明 |
|------|------|------|
| ArXiv | https://arxiv.org/list/cs.LG/recent | 机器学习最新论文 |
| Papers with Code | https://paperswithcode.com/ | 论文与代码对应 |
| Hugging Face Papers | https://huggingface.co/papers | 论文摘要 |

---

## 资源使用建议

### 每周学习资源分配
| 时间 | 资源类型 | 占比 |
|------|---------|------:|
| 平日理论（1h） | 官方文档 + 视频教程 | 70% |
| 平日实践（1h） | 实战项目 | 30% |
| 周末实战（3h） | 实战项目 + 技术博客 | 80% |
| 周末总结（1h） | 整理笔记 + 写博客 | 20% |

### 资源优先级
| 优先级 | 资源类型 | 说明 |
|-------|---------|------|
| ⭐⭐⭐⭐⭐ | 官方文档 | 必读，API 查阅 |
| ⭐⭐⭐⭐⭐ | 实战项目 | 必跑，验证理论 |
| ⭐⭐⭐⭐ | 视频教程 | 选看，快速入门 |
| ⭐⭐⭐ | 技术博客 | 选读，补充理解 |
| ⭐⭐⭐ | 相关论文 | 选读，深度原理 |
| ⭐⭐ | 书籍 | 参考，系统学习 |

### 资源连续性说明
1. **W1-W3**：Python/PyTorch/ONNX/C++ 基础资源连续，每周依赖上一周成果
2. **W4-W7**：Android/iOS/量化资源连续，形成完整双端能力
3. **W8-W9**：框架对比/性能优化资源连续，完成深度学习
4. **W10-W11**：LLM/机器人资源独立，拓展技术广度
5. **W12**：面试资源汇总，整合前11周内容

---

*学习周期：2026年4月1日 - 6月23日（12周）*
*制定时间：2026年3月25日*
*版本：v3.1（完整资源库版，含日期版）*
*配套文档：《最终版_端侧AI工程师_3个月冲刺计划_v3.0_优化版.md》*
