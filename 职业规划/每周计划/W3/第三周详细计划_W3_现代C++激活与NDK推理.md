# W3 详细执行计划：现代 C++ 激活 + ONNX Runtime C++ 推理

> **生成说明**：本文档基于《端侧AI工程师3个月冲刺计划 v3.0》、W1-W2 完成情况及《每周学习资源库 v3.1》综合制定。
> **生成时间**：2026年5月12日

---

**周期**：2026年4月14日（周二）— 4月20日（周一）
**核心目标**：C++ 写一个独立的命令行推理 Demo，代码要能跑通
**本周固定产出**：
- 1 个 C++ 命令行推理工具：`./infer --model resnet50.onnx --image cat.jpg`
- 1 份 C++ vs Python 推理性能对比数据
- InferenceEngine C++ 类 + JNI 接口设计（为 W4 Android 做准备）
- 1 篇技术博客草稿（"从 Python 到 C++：移动端开发者的 ONNX Runtime C++ 推理实战"）
- GitHub commit 记录（每天一次）

---

## W2 → W3 衔接说明

W2 你完成了：PyTorch 模型导出 ONNX、Netron 可视化计算图、ONNX Runtime Python 推理 + 数值验证、onnx-simplifier 图优化、端到端 Demo。

**本周要解决的核心问题**：Python 推理已经跑通了，但 Android/iOS 上只能跑 C++，怎么在 C++ 里加载 `.onnx` 并推理？

答案：ONNX Runtime 提供了完整的 C++ API，本周先在 macOS 桌面端用 C++ 跑通，下周（W4）再移植到 Android NDK。

**你的核心优势**：你有多年的 C++ / NDK / JNI 经验，这周对你来说不是"学新语言"，而是"把已有技能对接到 AI 推理场景"。

---

## 本周执行原则

1. **C++ 学习只取所需**：不追求 C++ 全貌，只学端侧 AI 推理用得上的特性（智能指针、move、lambda、chrono）
2. **先跑通再优化**：第一版代码不追求完美，能加载模型并推理就算成功
3. **对比思维**：每个 C++ API 都对比 Python 版本，降低认知负荷
4. **每天必须有代码输出**，禁止"只看不练"

---

## C++ 学习重点（删减版，贴在墙上）

```
✅ 必学（端侧AI推理核心）：
- unique_ptr/shared_ptr（推理引擎资源管理）
- std::vector/unordered_map（模型参数存储）
- std::chrono（性能计时，面试必问）
- std::function/lambda（回调封装）
- move 语义（避免不必要拷贝，大张量传递）
- stb_image（单头文件图片解码，行业通用）

❌ 不必深学（推理引擎用不着）：
- 模板元编程（TMP）
- 异常高级用法（端侧追求稳定，实际项目很少 try-catch）
- STL 实现细节（会调用即可）
- 多重继承 / 虚继承
```

---

## Day 1（周二 4/14）：C++11/14/17 现代特性激活

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：激活现代 C++ 语法记忆，重点掌握智能指针和 move 语义

### 早上 7:00-8:00：理论学习

**第一步（25分钟）**：[《现代C++教程》在线版](https://changkun.de/modern-cpp/zh-cn/00-preface/)（作者欧长坤，已从 `changkun.github.io` 迁至 `changkun.de`）

重点读以下章节（其他章节跳过）：

| 章节 | 核心内容 | 为什么重要 |
|------|---------|-----------|
| [第5章 智能指针](https://changkun.de/modern-cpp/zh-cn/05-pointers/) | `unique_ptr`、`shared_ptr`、`make_unique/make_shared` | ONNX Runtime C++ API 返回值都是 unique_ptr |
| [第3章 §3.3 右值引用](https://changkun.de/modern-cpp/zh-cn/03-runtime/) | `std::move`、右值引用 `&&`、完美转发 | 大张量传递避免拷贝，推理引擎内部大量使用 |
| [第3章 §3.1 Lambda](https://changkun.de/modern-cpp/zh-cn/03-runtime/) | `[](){}` 语法、捕获列表、`std::function` | 回调封装、日志函数 |
| [第2章 §2.6 auto](https://changkun.de/modern-cpp/zh-cn/02-usability/) | `auto` 类型推导 | 简化 ONNX Runtime 复杂模板类型 |

**第二步（20分钟）**：看视频加深理解

| 视频 | 平台 | 时长 | 重点 |
|------|------|------|------|
| [C++ Smart Pointers - The Cherno](https://www.youtube.com/watch?v=UOB7-B2MfbA) | YouTube | 18min | unique_ptr vs shared_ptr 生命周期 |
| [Move Semantics in C++ - The Cherno](https://www.youtube.com/watch?v=ehMg6zvXuMY) | YouTube | 16min | std::move 到底做了什么 |
| [C++ Lambda Expressions - The Cherno](https://www.youtube.com/watch?v=mWgmBBz0y8c) | YouTube | 16min | Lambda 基础用法 |

> **替代方案**：如果 YouTube 不方便，B站搜索"C++ 智能指针"、"C++ move语义"、"C++ lambda表达式"，选播放量最高的。

**第三步（10分钟）**：移动端类比建立直觉

| Python 概念 | C++ 等价 | 说明 |
|------------|---------|------|
| `with session:` | `auto session = std::make_unique<Session>(...)` | unique_ptr = 独占资源 |
| 对象自动回收 | `shared_ptr` 引用计数回收 | 类似 ARC/GC，但手动控制 |
| `a = b`（引用赋值） | `auto a = std::move(b)` | move 转移所有权，b 变空 |
| `lambda x: x+1` | `[](int x) { return x+1; }` | 语法不同，概念一样 |

### 晚上 21:00-22:00：代码实操

```cpp
// week3/day1_modern_cpp.cpp
// 编译：g++ -std=c++17 -o day1 day1_modern_cpp.cpp && ./day1

#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <chrono>
#include <functional>
#include <unordered_map>

// ============================
// 1. unique_ptr：独占所有权（推理引擎最常用）
// ============================
void demo_unique_ptr() {
    std::cout << "=== unique_ptr ===" << std::endl;

    // 创建 unique_ptr（类比 Python: session = create_session()）
    auto ptr = std::make_unique<std::vector<float>>(1000, 0.0f);
    std::cout << "  ptr size: " << ptr->size() << std::endl;

    // 转移所有权（move 语义）
    auto ptr2 = std::move(ptr);  // ptr 变为 nullptr，ptr2 接管资源
    std::cout << "  after move, ptr is " << (ptr ? "not null" : "null") << std::endl;
    std::cout << "  ptr2 size: " << ptr2->size() << std::endl;

    // 离开作用域，自动释放（不需要 delete！）
}

// ============================
// 2. shared_ptr：共享所有权（配置对象等）
// ============================
void demo_shared_ptr() {
    std::cout << "\n=== shared_ptr ===" << std::endl;

    auto config = std::make_shared<std::unordered_map<std::string, int>>();
    (*config)["num_threads"] = 4;
    (*config)["batch_size"] = 1;

    // 多个持有者共享同一份配置
    auto config2 = config;  // 引用计数 +1
    std::cout << "  use_count: " << config.use_count() << std::endl;  // 2

    config2.reset();  // 释放一个引用
    std::cout << "  after reset, use_count: " << config.use_count() << std::endl;  // 1
}

// ============================
// 3. move 语义：避免大对象拷贝
// ============================
void demo_move() {
    std::cout << "\n=== move 语义 ===" << std::endl;

    // 模拟一个大的推理输出张量
    std::vector<float> big_tensor(1000000, 1.0f);
    std::cout << "  原始 big_tensor size: " << big_tensor.size() << std::endl;

    // 不用 move：拷贝（慢！100万个float全部复制）
    auto start = std::chrono::high_resolution_clock::now();
    std::vector<float> copied = big_tensor;  // 深拷贝
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "  深拷贝耗时: "
              << std::chrono::duration<double, std::micro>(end - start).count() << " μs" << std::endl;

    // 用 move：转移所有权（快！只移动内部指针）
    start = std::chrono::high_resolution_clock::now();
    std::vector<float> moved = std::move(big_tensor);  // 零拷贝
    end = std::chrono::high_resolution_clock::now();
    std::cout << "  move 耗时: "
              << std::chrono::duration<double, std::micro>(end - start).count() << " μs" << std::endl;
    std::cout << "  move 后原对象 size: " << big_tensor.size() << std::endl;  // 0
    std::cout << "  新对象 size: " << moved.size() << std::endl;  // 1000000
}

// ============================
// 4. Lambda + std::function
// ============================
void demo_lambda() {
    std::cout << "\n=== Lambda ===" << std::endl;

    // 简单 lambda
    auto add = [](int a, int b) { return a + b; };
    std::cout << "  add(3, 4) = " << add(3, 4) << std::endl;

    // 捕获外部变量（日志回调，推理引擎常见模式）
    int inference_count = 0;
    auto logger = [&inference_count](const std::string& msg) {
        inference_count++;
        std::cout << "  [Inference #" << inference_count << "] " << msg << std::endl;
    };

    logger("开始推理...");
    logger("推理完成");

    // std::function 作为回调类型（类似 Python 的 Callable）
    std::function<void(const std::string&)> callback = logger;
    callback("通过 function 调用");
}

int main() {
    demo_unique_ptr();
    demo_shared_ptr();
    demo_move();
    demo_lambda();

    std::cout << "\n✅ Day1 完成！现代 C++ 核心特性已激活" << std::endl;
    return 0;
}
```

**今天的 GitHub commit**：
```bash
mkdir -p ~/on-device-ai-journey/week3
cd ~/on-device-ai-journey
echo "# Week3: 现代 C++ + ONNX Runtime C++ 推理" > week3/README.md
git add week3/
git commit -m "W3D1: 现代 C++ 特性激活（智能指针/move/lambda）"
```

---

## Day 2（周三 4/15）：内存对齐 + C++ 项目构建（CMake）

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：理解 AI 推理中的内存对齐要求，搭建 C++ 项目 CMake 构建框架

### 早上 7:00-8:00：理论学习

**第一步（20分钟）**：理解内存对齐

AI 推理为什么关心内存对齐？

| 场景 | 原因 |
|------|------|
| SIMD 指令（NEON/SSE） | 要求数据地址是 16/32 字节对齐，否则 Segfault |
| ONNX Runtime 内部 | 用 `aligned_alloc` 分配张量内存，加速 DMA 传输 |
| 模型权重加载 | `mmap` 方式加载 `.onnx` 文件，对齐决定读取效率 |

阅读：[cppreference - aligned_alloc](https://en.cppreference.com/w/c/memory/aligned_alloc)

核心概念：
```cpp
// 未对齐：可能触发硬件异常或性能下降
float* data = malloc(sizeof(float) * 1024);  // 对齐不确定
// “32字节对齐”是这样：内存的“起点”（首地址数字）必须是32的倍数。不是分成1024份，而是整个大块的第一个字节的编号要对齐。
// 为啥不能任意开头？打个比方：CPU是个搬运机器人，每次装32箱子（32字节），轨道每32格一个大台阶。如果你从第1格（不是32的倍数）让它搬，每次都得斜坡起步，搬一趟还得多填一段空地，多走弯路，甚至有时还得“半趟装不满”——特别浪费力气，还慢（有的机器人根本不支持这么搬，直接报错）。
// 只有从第32格、第64格...这样的整数台阶出发，CPU才能每次“满载出发”，“一车带走32箱，不掉落”，效率最高。
// 另外，SIMD 或 DMA 这些快指令，取数据只能从“大台阶”（对齐处）装满，否则：要么多搬一趟，要么根本不让装。
// 
// 所以aligned_alloc(32, ...)的意义就在于——保证内存正好从一个“台阶”开头，CPU/硬件不用多折腾，性能才最优。
// 下面这个例子其实就是分一整块足够大的地，并保证入口刚好在高速通道的门口：
// 代码分配1024个float，首地址正好32的倍数，后续运算不卡壳。
float* aligned = (float*)aligned_alloc(32, sizeof(float) * 1024);  // 保证入口就在32字节“台阶”，搬运全速！

// C++17 更安全的方式
auto ptr = std::make_unique<float[]>(1024);  // 默认对齐
// 或使用 std::vector + 自定义分配器（本周不深入）
```

**第二步（20分钟）**：CMake 入门

ONNX Runtime C++ 项目需要 CMake 构建，这是必须掌握的工具。

阅读：[CMake 官方教程](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)（只看 Step 1-2）

理解核心概念：
```cmake
cmake_minimum_required(VERSION 3.15)
project(onnx_inference)

# 关键：设置 C++17 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 ONNX Runtime 库（Day3 会用）
# find_package(onnxruntime REQUIRED)

# 添加可执行文件
add_executable(infer src/main.cpp)

# 链接库
# target_link_libraries(infer onnxruntime)
```

**第三步（15分钟）**：看视频

| 视频 | 平台 | 时长 | 重点 |
|------|------|------|------|
| [CMake Tutorial for Beginners - Code, Tech, and Tutorials](https://www.youtube.com/watch?v=nlKc1HPStPY) | YouTube | 15min | CMake 基础概念 |
| [Memory Alignment in C/C++ - Jason Turner](https://www.youtube.com/watch?v=Sr27YS_wbQ4) | YouTube | 10min | alignas 和内存对齐 |

> B站替代：搜索"CMake 入门教程"、"C++ 内存对齐"

### 晚上 21:00-22:00：搭建项目骨架

```cpp
// week3/src/tensor_utils.h
// 简单的内存对齐工具（本周后续代码会用到）
#pragma once
#include <cstdlib>
#include <memory>
#include <vector>
#include <iostream>
#include <chrono>

namespace onnx_inference {

// 对齐内存分配器（SIMD 友好）
inline float* alloc_aligned(size_t count, size_t alignment = 32) {
    size_t size = count * sizeof(float);
    // 确保 size 是 alignment 的倍数
    size = (size + alignment - 1) & ~(alignment - 1);
    void* ptr = std::aligned_alloc(alignment, size);
    if (!ptr) {
        std::cerr << "分配对齐内存失败" << std::endl;
        return nullptr;
    }
    return static_cast<float*>(ptr);
}

// RAII 封装：自动释放对齐内存
struct AlignedBufferDeleter {
    void operator()(float* ptr) const { std::free(ptr); }
};
using AlignedBuffer = std::unique_ptr<float[], AlignedBufferDeleter>;

inline AlignedBuffer make_aligned_buffer(size_t count, size_t alignment = 32) {
    return AlignedBuffer(alloc_aligned(count, alignment));
}

// 计时工具（推理性能测量核心）
class Timer {
public:
    void start() { start_ = std::chrono::high_resolution_clock::now(); }

    double elapsed_ms() const {
        auto end = std::chrono::high_resolution_clock::now();
        return std::chrono::duration<double, std::milli>(end - start_).count();
    }

    double elapsed_us() const {
        auto end = std::chrono::high_resolution_clock::now();
        return std::chrono::duration<double, std::micro>(end - start_).count();
    }

private:
    std::chrono::high_resolution_clock::time_point start_;
};

}  // namespace onnx_inference
```

```cmake
# week3/CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(onnx_inference VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译选项
if(APPLE)
    set(ONNXRUNTIME_ROOT "$ENV{HOME}/onnxruntime-mac" CACHE PATH "ONNX Runtime SDK path")
elseif(UNIX)
    set(ONNXRUNTIME_ROOT "/usr/local/onnxruntime" CACHE PATH "ONNX Runtime SDK path")
endif()

# Day2 先不加 ORT 依赖，Day3 再加
add_executable(day1 src/day1_modern_cpp.cpp)
```

**今天的 GitHub commit**：
```bash
git add week3/
git commit -m "W3D2: 内存对齐工具 + CMake 项目骨架搭建"
```

---

## Day 3（周四 4/16）：ONNX Runtime C++ API 实战

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：用 C++ 加载 `.onnx` 文件，跑一次推理，对比 Python ORT 结果

> **这是本周最关键的一天！** 从 Python 到 C++ 的跨越就在今天。

### 早上 7:00-8:00：理论学习

**第一步（30分钟）**：精读 [ONNX Runtime C++ API 文档](https://onnxruntime.ai/docs/api/c/index.html)

Python C++ API 对照表（降低认知负荷）：

| Python API | C++ API | 说明 |
|-----------|---------|------|
| `ort.InferenceSession(path)` | `Ort::Session(env, path, options)` | 创建推理会话 |
| `session.get_inputs()[0].name` | `session.GetInputNameAllocated(0, allocator)` | 获取输入名 |
| `session.get_inputs()[0].shape` | `session.GetInputTypeInfo(0).GetTensorTypeAndShapeInfo().GetShape()` | 获取输入 shape |
| `session.run([out], {in: data})` | `session.Run(run_options, input_names, input_tensors, output_names)` | 执行推理 |
| `numpy.array` | `Ort::Value::CreateTensor<float>(...)` | 创建输入张量 |
| `result[0]` (numpy) | `output_tensor.GetTensorData<float>()` | 获取输出数据 |

**第二步（15分钟）**：看视频

| 视频 | 平台 | 时长 | 重点 |
|------|------|------|------|
| [ONNX Runtime C++ Inference Tutorial](https://www.youtube.com/results?search_query=onnx+runtime+c%2B%2B+inference+tutorial) | YouTube | 30min | C++ API 完整示例 |

> B站替代：搜索"ONNX Runtime C++ 推理"

**第三步（10分钟）**：理解 C++ API 的内存管理模式

```cpp
// C++ ORT 的核心设计模式：
// 1. Ort::Env - 全局环境（整个进程一个）
// 2. Ort::Session - 推理会话（每个模型一个）
// 3. Ort::Value - 张量（输入/输出）
// 4. Ort::AllocatorWithDefaultOptions - 内存分配器
// 5. 所有对象都是 RAII 管理，离开作用域自动释放
```

### 安装 ONNX Runtime C++ SDK（课前准备）

```bash
# macOS 安装 ONNX Runtime C++ SDK
cd ~
# 下载预编译包（M系列芯片用 arm64 版本）
curl -LO https://github.com/microsoft/onnxruntime/releases/download/v1.17.1/onnxruntime-osx-arm64-1.17.1.tgz
tar xzf onnxruntime-osx-arm64-1.17.1.tgz
mv onnxruntime-osx-arm64-1.17.1 onnxruntime-mac

# 验证
ls ~/onnxruntime-mac/include/   # 应该有 onnxruntime_cxx_api.h
ls ~/onnxruntime-mac/lib/       # 应该有 libonnxruntime.dylib

# Intel Mac 用 x64 版本：
# curl -LO https://github.com/microsoft/onnxruntime/releases/download/v1.17.1/onnxruntime-osx-x86_64-1.17.1.tgz
```

### 晚上 21:00-22:00：C++ 推理实战

```cpp
// week3/src/day3_ort_cpp_inference.cpp
// 编译：
//   cd week3/build && cmake .. && make
// 运行：
//   ./day3 ../models/resnet50_simplified.onnx

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

// ONNX Runtime C++ API 头文件
#include <onnxruntime_cxx_api.h>

#include "tensor_utils.h"

using namespace onnx_inference;

int main(int argc, char* argv[]) {
    // ============================
    // Step 1: 初始化 ONNX Runtime 环境
    // ============================
    std::cout << "Step 1: 初始化 ONNX Runtime 环境..." << std::endl;

    // Env 是全局的，整个进程只需要一个
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "inference");

    // Session 选项（类比 Python: ort.SessionOptions()）
    Ort::SessionOptions session_options;
    session_options.SetIntraOpNumThreads(1);  // 单线程，后面 Day5 会调
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

    // ============================
    // Step 2: 加载 ONNX 模型
    // ============================
    std::cout << "Step 2: 加载 ONNX 模型..." << std::endl;

    // 模型路径（复用 W2 导出的模型）
    const char* model_path = (argc > 1) ? argv[1] : "../models/resnet50_simplified.onnx";

    Timer load_timer;
    load_timer.start();

    Ort::Session session(env, model_path, session_options);

    std::cout << "  模型加载耗时: " << load_timer.elapsed_ms() << " ms" << std::endl;

    // ============================
    // Step 3: 查看模型输入/输出信息
    // ============================
    std::cout << "\nStep 3: 模型信息..." << std::endl;

    Ort::AllocatorWithDefaultOptions allocator;

    // 输入信息
    auto input_name = session.GetInputNameAllocated(0, allocator);
    auto input_type_info = session.GetInputTypeInfo(0);
    auto input_tensor_info = input_type_info.GetTensorTypeAndShapeInfo();
    auto input_shape = input_tensor_info.GetShape();

    std::cout << "  输入名称: " << input_name.get() << std::endl;
    std::cout << "  输入 shape: [";
    for (size_t i = 0; i < input_shape.size(); i++) {
        std::cout << input_shape[i];
        if (i < input_shape.size() - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    // 输出信息
    auto output_name = session.GetOutputNameAllocated(0, allocator);
    std::cout << "  输出名称: " << output_name.get() << std::endl;

    // ============================
    // Step 4: 准备输入数据
    // ============================
    std::cout << "\nStep 4: 准备输入数据..." << std::endl;

    // 创建随机输入（模拟一张图片，shape: [1, 3, 224, 224]）
    size_t input_tensor_size = 1 * 3 * 224 * 224;
    auto input_buffer = make_aligned_buffer(input_tensor_size);

    // 填充随机数据（模拟归一化后的像素值）
    for (size_t i = 0; i < input_tensor_size; i++) {
        input_buffer[i] = static_cast<float>(rand()) / RAND_MAX - 0.5f;
    }

    // 创建 ONNX Runtime 输入张量
    // 注意：input_shape 中可能有 -1（动态维度），需要替换为实际值
    std::vector<int64_t> actual_input_shape = {1, 3, 224, 224};

    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
        memory_info,
        input_buffer.get(),
        input_tensor_size,
        actual_input_shape.data(),
        actual_input_shape.size()
    );

    std::cout << "  输入张量创建完成, shape: [1, 3, 224, 224]" << std::endl;

    // ============================
    // Step 5: 执行推理
    // ============================
    std::cout << "\nStep 5: 执行推理..." << std::endl;

    // 准备输入/输出名称数组
    const char* input_names[] = { input_name.get() };
    const char* output_names[] = { output_name.get() };

    // Warm up（第一次推理较慢，包含 JIT 编译等）
    session.Run(Ort::RunOptions{nullptr}, input_names, &input_tensor, 1, output_names, 1);

    // 正式推理 + 计时
    Timer infer_timer;
    infer_timer.start();

    auto output_tensors = session.Run(
        Ort::RunOptions{nullptr},
        input_names,
        &input_tensor,
        1,          // 1 个输入
        output_names,
        1           // 1 个输出
    );

    double infer_ms = infer_timer.elapsed_ms();
    std::cout << "  推理耗时: " << infer_ms << " ms" << std::endl;

    // ============================
    // Step 6: 解析输出
    // ============================
    std::cout << "\nStep 6: 解析输出..." << std::endl;

    // 获取输出数据指针（不拷贝，直接指向内部 buffer）
    const float* output_data = output_tensors[0].GetTensorData<float>();

    // 获取输出 shape
    auto& output_tensor_info = output_tensors[0].GetTensorTypeAndShapeInfo();
    auto output_shape = output_tensor_info.GetShape();

    std::cout << "  输出 shape: [";
    for (size_t i = 0; i < output_shape.size(); i++) {
        std::cout << output_shape[i];
        if (i < output_shape.size() - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    // 找 Top-5
    size_t output_size = 1;
    for (auto dim : output_shape) output_size *= dim;

    std::vector<std::pair<float, int>> results;
    for (size_t i = 0; i < output_size; i++) {
        results.push_back({output_data[i], static_cast<int>(i)});
    }
    std::partial_sort(results.begin(), results.begin() + 5, results.end(),
                      std::greater<std::pair<float, int>>());

    std::cout << "\n  Top-5 类别 ID 和分数：" << std::endl;
    for (int i = 0; i < 5; i++) {
        printf("    #%d: class_id=%4d  score=%.4f\n", i+1, results[i].second, results[i].first);
    }

    // ============================
    // Step 7: 性能汇总
    // ============================
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "性能数据汇总" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    std::cout << "  设备: CPU (macOS)" << std::endl;
    std::cout << "  模型: ResNet50 (ONNX)" << std::endl;
    std::cout << "  输入: 1x3x224x224" << std::endl;
    std::cout << "  加载耗时: " << load_timer.elapsed_ms() << " ms" << std::endl;
    std::cout << "  推理耗时: " << infer_ms << " ms" << std::endl;

    std::cout << "\n✅ Day3 完成！C++ ONNX Runtime 推理跑通了！" << std::endl;
    return 0;
}
```

更新 CMakeLists.txt：
```cmake
# week3/CMakeLists.txt（添加 Day3 目标）
cmake_minimum_required(VERSION 3.15)
project(onnx_inference VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ONNX Runtime SDK 路径
if(APPLE)
    set(ONNXRUNTIME_ROOT "$ENV{HOME}/onnxruntime-mac" CACHE PATH "ONNX Runtime SDK path")
elseif(UNIX)
    set(ONNXRUNTIME_ROOT "/usr/local/onnxruntime" CACHE PATH "ONNX Runtime SDK path")
endif()

# ONNX Runtime 头文件和库
include_directories(${ONNXRUNTIME_ROOT}/include)
link_directories(${ONNXRUNTIME_ROOT}/lib)

# Day1: 现代 C++ 特性
add_executable(day1 src/day1_modern_cpp.cpp)

# Day3: ONNX Runtime C++ 推理
add_executable(day3 src/day3_ort_cpp_inference.cpp)
target_link_libraries(day3 onnxruntime)
if(APPLE)
    target_link_libraries(day3 "-framework CoreFoundation")
    set_target_properties(day3 PROPERTIES BUILD_RPATH ${ONNXRUNTIME_ROOT}/lib)
endif()
```

构建和运行：
```bash
cd week3
mkdir -p build && cd build
cmake ..
make

# 复制 W2 的模型文件
mkdir -p ../models
cp ../../Week2/scripts/resnet50_simplified.onnx ../models/

# 运行
./day3 ../models/resnet50_simplified.onnx
```

**今天的 GitHub commit**：
```bash
git add week3/
git commit -m "W3D3: ONNX Runtime C++ API 推理跑通，ResNet50 推理成功"
```

---

## Day 4（周五 4/17）：前后处理 C++ 实现（stb_image）

**时间**：早 7:00-8:00（理论），晚 21:00-22:00（实操）
**目标**：用 stb_image 解码图片，实现 resize + normalize 前处理，后处理输出 Top-5 标签

### 早上 7:00-8:00：理论学习

**第一步（15分钟）**：了解 stb_image

阅读：[stb_image GitHub](https://github.com/nothings/stb/blob/master/stb_image.h)

为什么用 stb_image？
- 单头文件，`#define STB_IMAGE_IMPLEMENTATION` 即可使用
- 行业通用：llama.cpp、ncnn、ONNX Runtime 示例都在用
- 支持 JPEG/PNG/BMP/TGA 等常见格式
- 不依赖任何外部库

**第二步（15分钟）**：前处理流程回顾

```
图片文件 → stb_image 解码 → uint8 HWC → float HWC /255.0
→ Normalize(mean, std) → HWC → CHW → 添加 batch 维度 → [1, 3, 224, 224]
```

对比 Python（W1 Day5 的 `transforms.Compose`）：

| Python transforms | C++ 手动实现 | 说明 |
|-------------------|-------------|------|
| `transforms.Resize(256)` | 双线性插值 / stb_image_resize | 短边缩放到 256 |
| `transforms.CenterCrop(224)` | 从中心裁剪 | 取中心 224x224 |
| `transforms.ToTensor()` | HWC uint8 → CHW float32 / 255.0 | 归一化到 [0, 1] |
| `transforms.Normalize(mean, std)` | `(x - mean) / std` 逐通道 | ImageNet 标准化 |

**第三步（20分钟）**：看视频

| 视频 | 平台 | 时长 | 重点 |
|------|------|------|------|
| [stb_image tutorial - Making a Game Engine](https://www.youtube.com/watch?v=kAPIapId3ik) | YouTube | 12min | stb_image 基础用法 |
| [Image Preprocessing for Neural Networks](https://www.youtube.com/results?search_query=image+preprocessing+neural+network+c%2B%2B) | YouTube | 15min | 图片预处理流程 |

> B站替代：搜索"stb_image 使用"、"C++ 图片预处理 神经网络"

### 晚上 21:00-22:00：前后处理实现

```cpp
// week3/src/image_utils.h
// 图片前后处理工具
#pragma once
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <iostream>

// stb_image 单头文件库
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_resize2.h"

namespace onnx_inference {

struct ImageData {
    std::vector<float> data;     // CHW float32 格式
    int channels;
    int height;
    int width;
};

// ImageNet 标准化参数
constexpr float IMAGENET_MEAN[] = {0.485f, 0.456f, 0.406f};
constexpr float IMAGENET_STD[]  = {0.229f, 0.224f, 0.225f};

inline ImageData preprocess_image(const std::string& image_path, int target_size = 224) {
    ImageData result;

    // Step 1: 加载图片
    int w, h, c;
    unsigned char* img = stbi_load(image_path.c_str(), &w, &h, &c, 3);  // 强制 3 通道
    if (!img) {
        std::cerr << "图片加载失败: " << image_path << std::endl;
        return result;
    }
    std::cout << "  原始图片: " << w << "x" << h << " channels=" << c << std::endl;

    // Step 2: Resize（短边缩放到 256，保持比例）
    int new_w, new_h;
    if (w < h) {
        new_w = 256;
        new_h = static_cast<int>(h * 256.0f / w);
    } else {
        new_h = 256;
        new_w = static_cast<int>(w * 256.0f / h);
    }

    std::vector<unsigned char> resized(new_w * new_h * 3);
    stbir_resize_uint8_linear(img, w, h, 0,
                              resized.data(), new_w, new_h, 0,
                              STBIR_RGB);
    stbi_image_free(img);

    // Step 3: CenterCrop（裁剪中心 target_size x target_size）
    int crop_x = (new_w - target_size) / 2;
    int crop_y = (new_h - target_size) / 2;

    result.channels = 3;
    result.height = target_size;
    result.width = target_size;
    result.data.resize(3 * target_size * target_size);

    // Step 4: HWC uint8 → CHW float32，归一化 + ImageNet 标准化
    for (int ch = 0; ch < 3; ch++) {
        for (int y = 0; y < target_size; y++) {
            for (int x = 0; x < target_size; x++) {
                int src_idx = ((crop_y + y) * new_w + (crop_x + x)) * 3 + ch;
                float pixel = static_cast<float>(resized[src_idx]) / 255.0f;
                pixel = (pixel - IMAGENET_MEAN[ch]) / IMAGENET_STD[ch];
                int dst_idx = ch * target_size * target_size + y * target_size + x;
                result.data[dst_idx] = pixel;
            }
        }
    }

    std::cout << "  预处理完成: [3, " << target_size << ", " << target_size << "]" << std::endl;
    return result;
}

// Softmax（后处理）
inline std::vector<float> softmax(const float* data, size_t size) {
    std::vector<float> result(size);
    float max_val = *std::max_element(data, data + size);

    float sum = 0.0f;
    for (size_t i = 0; i < size; i++) {
        result[i] = std::exp(data[i] - max_val);  // 减 max 防溢出
        sum += result[i];
    }
    for (size_t i = 0; i < size; i++) {
        result[i] /= sum;
    }
    return result;
}

// Top-K 结果
struct TopKResult {
    int class_id;
    float probability;
};

inline std::vector<TopKResult> top_k(const float* data, size_t size, int k = 5) {
    std::vector<std::pair<float, int>> pairs;
    for (size_t i = 0; i < size; i++) {
        pairs.push_back({data[i], static_cast<int>(i)});
    }
    std::partial_sort(pairs.begin(), pairs.begin() + k, pairs.end(),
                      std::greater<std::pair<float, int>>());

    std::vector<TopKResult> results;
    for (int i = 0; i < k; i++) {
        results.push_back({pairs[i].second, pairs[i].first});
    }
    return results;
}

}  // namespace onnx_inference
```

> **注意**：使用前需要下载 `stb_image.h` 和 `stb_image_resize2.h`：
> ```bash
> cd week3/src
> curl -LO https://raw.githubusercontent.com/nothings/stb/master/stb_image.h
> curl -LO https://raw.githubusercontent.com/nothings/stb/master/stb_image_resize2.h
> ```

**今天的 GitHub commit**：
```bash
git add week3/
git commit -m "W3D4: stb_image 图片前后处理，ImageNet 归一化 + Top-K 输出"
```

---

## Day 5（周六 4/18）：异常处理 + 性能计时 + 多次推理 Benchmark

**时间**：早 9:00-12:00（实战），下午 15:00-17:00（总结），晚 19:00-21:00（预习）
**目标**：封装推理错误处理，实现精准计时，跑多次推理取平均，生成 Benchmark 数据

### 09:00-12:00：封装 + Benchmark

**先读（15分钟）**：[ONNX Runtime C++ API - 错误处理](https://onnxruntime.ai/docs/api/c/struct_ort_api.html)

ONNX Runtime C++ API 的错误处理模式：
```cpp
// Ort::Exception 是所有 ORT 错误的基类
try {
    Ort::Session session(env, model_path, options);
} catch (const Ort::Exception& e) {
    std::cerr << "ORT Error: " << e.what() << std::endl;
    // 模型文件不存在、格式错误、opset 不支持等
}
```

```cpp
// week3/src/day5_benchmark.cpp
// 编译：cd week3/build && cmake .. && make
// 运行：./day5 ../models/resnet50_simplified.onnx ../images/cat.jpg

#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>
#include <algorithm>

#include <onnxruntime_cxx_api.h>

#include "tensor_utils.h"
#include "image_utils.h"

using namespace onnx_inference;

// 多次推理取平均值（消除冷启动波动）
struct BenchmarkResult {
    double avg_ms;
    double min_ms;
    double max_ms;
    double p50_ms;   // 中位数
    double p99_ms;   // 99分位
    int num_runs;
};

BenchmarkResult run_benchmark(Ort::Session& session,
                              Ort::Value& input_tensor,
                              const char* input_name,
                              const char* output_name,
                              int num_warmup = 5,
                              int num_runs = 50) {
    std::vector<double> latencies;

    // Warm up
    for (int i = 0; i < num_warmup; i++) {
        auto outputs = session.Run(
            Ort::RunOptions{nullptr},
            &input_name, &input_tensor, 1,
            &output_name, 1
        );
    }

    // 正式推理
    for (int i = 0; i < num_runs; i++) {
        Timer timer;
        timer.start();

        auto outputs = session.Run(
            Ort::RunOptions{nullptr},
            &input_name, &input_tensor, 1,
            &output_name, 1
        );

        latencies.push_back(timer.elapsed_ms());
    }

    // 统计
    std::sort(latencies.begin(), latencies.end());

    BenchmarkResult result;
    result.num_runs = num_runs;
    result.min_ms = latencies.front();
    result.max_ms = latencies.back();
    result.avg_ms = std::accumulate(latencies.begin(), latencies.end(), 0.0) / num_runs;
    result.p50_ms = latencies[num_runs / 2];
    result.p99_ms = latencies[static_cast<int>(num_runs * 0.99)];

    return result;
}

int main(int argc, char* argv[]) {
    const char* model_path = (argc > 1) ? argv[1] : "../models/resnet50_simplified.onnx";
    const char* image_path = (argc > 2) ? argv[2] : nullptr;

    try {
        // 初始化
        Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "benchmark");

        // 测试不同线程数的性能
        std::vector<int> thread_counts = {1, 2, 4};

        std::cout << "======================================" << std::endl;
        std::cout << "ONNX Runtime C++ 推理 Benchmark" << std::endl;
        std::cout << "======================================" << std::endl;
        std::cout << "模型: " << model_path << std::endl;

        // 准备输入数据
        size_t input_size = 1 * 3 * 224 * 224;
        std::vector<float> input_data;

        if (image_path) {
            std::cout << "图片: " << image_path << std::endl;
            auto img = preprocess_image(image_path, 224);
            input_data = std::move(img.data);
        } else {
            std::cout << "输入: 随机数据 [1,3,224,224]" << std::endl;
            input_data.resize(input_size);
            for (size_t i = 0; i < input_size; i++) {
                input_data[i] = static_cast<float>(rand()) / RAND_MAX - 0.5f;
            }
        }

        auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
        std::vector<int64_t> input_shape = {1, 3, 224, 224};

        // 对比不同线程配置
        for (int num_threads : thread_counts) {
            std::cout << "\n--- " << num_threads << " 线程 ---" << std::endl;

            Ort::SessionOptions options;
            options.SetIntraOpNumThreads(num_threads);
            options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

            Ort::Session session(env, model_path, options);

            Ort::AllocatorWithDefaultOptions allocator;
            auto input_name = session.GetInputNameAllocated(0, allocator);
            auto output_name = session.GetOutputNameAllocated(0, allocator);

            // 创建输入张量
            Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
                memory_info,
                input_data.data(),
                input_data.size(),
                input_shape.data(),
                input_shape.size()
            );

            // Benchmark
            auto result = run_benchmark(session, input_tensor, input_name.get(), output_name.get());

            printf("  平均: %.2f ms | 最小: %.2f ms | 最大: %.2f ms | P50: %.2f ms | P99: %.2f ms\n",
                   result.avg_ms, result.min_ms, result.max_ms, result.p50_ms, result.p99_ms);

            // 顺便验证推理结果
            auto outputs = session.Run(
                Ort::RunOptions{nullptr},
                input_name.get(), &input_tensor, 1,
                output_name.get(), 1
            );

            const float* output_data = outputs[0].GetTensorData<float>();
            auto probs = softmax(output_data, 1000);
            auto top5 = top_k(probs.data(), 1000, 5);

            std::cout << "  Top-5: ";
            for (const auto& r : top5) {
                printf("[%d: %.2f%%] ", r.class_id, r.probability * 100);
            }
            std::cout << std::endl;
        }

        std::cout << "\n✅ Day5 Benchmark 完成！" << std::endl;

    } catch (const Ort::Exception& e) {
        std::cerr << "ONNX Runtime 错误: " << e.what() << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "错误: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
```

更新 CMakeLists.txt 添加 Day5：
```cmake
# Day5: Benchmark
add_executable(day5 src/day5_benchmark.cpp)
target_link_libraries(day5 onnxruntime)
if(APPLE)
    target_link_libraries(day5 "-framework CoreFoundation")
    set_target_properties(day5 PROPERTIES BUILD_RPATH ${ONNXRUNTIME_ROOT}/lib)
endif()
```

### 15:00-17:00：整理性能数据笔记

写 `week3/notes_benchmark.md`，记录真实数据：

```markdown
## C++ vs Python ONNX Runtime 性能对比

| 配置 | 平均延迟 | P50 | P99 |
|------|---------|-----|-----|
| Python ORT (1 thread) | ___ ms | ___ ms | ___ ms |
| C++ ORT (1 thread) | ___ ms | ___ ms | ___ ms |
| C++ ORT (2 threads) | ___ ms | ___ ms | ___ ms |
| C++ ORT (4 threads) | ___ ms | ___ ms | ___ ms |

### 结论
- C++ ORT 比 Python ORT 快 ___%（因为无 Python 解释器开销）
- 多线程收益：1→2 线程加速 ___%，2→4 线程加速 ___%
```

### 19:00-21:00：预习 Day6 CLI 工具封装

浏览 [CLI11](https://github.com/CLIUtils/CLI11)（C++ 命令行参数解析库，轻量单头文件）或者直接用 `getopt`。

**今天的 GitHub commit**：
```bash
git add week3/
git commit -m "W3D5: Benchmark 封装，多线程性能对比，异常处理"
```

---

## Day 6（周日 4/19）：CLI 推理工具封装

**时间**：早 9:00-12:00（实战），下午 15:00-17:00（博客），晚 19:00-21:00（预习）
**目标**：做一个命令行推理工具 + InferenceEngine 类封装

### 09:00-12:00：CLI 工具 + Engine 类

```cpp
// week3/src/inference_engine.h
// 推理引擎封装类（为 W4 Android JNI 做准备）
#pragma once
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <iostream>

#include <onnxruntime_cxx_api.h>

#include "tensor_utils.h"
#include "image_utils.h"

namespace onnx_inference {

class InferenceEngine {
public:
    struct Config {
        int num_threads = 1;
        bool enable_optimization = true;
    };

    struct Result {
        std::vector<TopKResult> top5;
        double latency_ms;
        bool success;
        std::string error_msg;
    };

    // 回调类型定义
    using LogCallback = std::function<void(const std::string&)>;

    InferenceEngine(const std::string& model_path, const Config& config = {});
    ~InferenceEngine() = default;

    // 从图片文件推理
    Result infer_image(const std::string& image_path);

    // 从原始数据推理（用于 Android 相机帧等）
    Result infer_raw(const float* data, size_t size, const std::vector<int64_t>& shape);

    // 设置日志回调
    void set_log_callback(LogCallback callback) { log_callback_ = std::move(callback); }

    // 获取模型信息
    std::string get_input_name() const;
    std::vector<int64_t> get_input_shape() const;

private:
    Ort::Env env_;
    Ort::Session session_;
    Ort::SessionOptions options_;
    Ort::AllocatorWithDefaultOptions allocator_;

    std::string input_name_;
    std::string output_name_;
    std::vector<int64_t> input_shape_;

    LogCallback log_callback_;

    void log(const std::string& msg) {
        if (log_callback_) log_callback_(msg);
    }
};

// ============================
// 实现
// ============================

inline InferenceEngine::InferenceEngine(const std::string& model_path, const Config& config)
    : env_(ORT_LOGGING_LEVEL_WARNING, "InferenceEngine"),
      session_(env_, model_path.c_str(), [&]() {
          Ort::SessionOptions opts;
          opts.SetIntraOpNumThreads(config.num_threads);
          if (config.enable_optimization) {
              opts.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
          }
          return opts;
      }()) {

    // 获取输入输出信息
    auto input_name_alloc = session_.GetInputNameAllocated(0, allocator_);
    auto output_name_alloc = session_.GetOutputNameAllocated(0, allocator_);
    input_name_ = input_name_alloc.get();
    output_name_ = output_name_alloc.get();

    auto type_info = session_.GetInputTypeInfo(0);
    auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
    input_shape_ = tensor_info.GetShape();

    log("InferenceEngine 初始化完成: " + model_path);
}

inline InferenceEngine::Result InferenceEngine::infer_image(const std::string& image_path) {
    Result result;
    Timer timer;

    try {
        // 前处理
        auto image_data = preprocess_image(image_path, 224);
        if (image_data.data.empty()) {
            result.success = false;
            result.error_msg = "图片预处理失败";
            return result;
        }

        // 推理
        result = infer_raw(image_data.data.data(), image_data.data.size(),
                          {1, 3, 224, 224});
    } catch (const Ort::Exception& e) {
        result.success = false;
        result.error_msg = std::string("ORT Error: ") + e.what();
    } catch (const std::exception& e) {
        result.success = false;
        result.error_msg = std::string("Error: ") + e.what();
    }

    return result;
}

inline InferenceEngine::Result InferenceEngine::infer_raw(
    const float* data, size_t size, const std::vector<int64_t>& shape) {

    Result result;
    Timer timer;

    try {
        auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);

        Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
            memory_info, const_cast<float*>(data), size,
            shape.data(), shape.size()
        );

        timer.start();
        auto outputs = session_.Run(
            Ort::RunOptions{nullptr},
            input_name_.c_str(), &input_tensor, 1,
            output_name_.c_str(), 1
        );
        result.latency_ms = timer.elapsed_ms();

        // 后处理
        const float* output_data = outputs[0].GetTensorData<float>();
        auto probs = softmax(output_data, 1000);
        result.top5 = top_k(probs.data(), 1000, 5);
        result.success = true;

    } catch (const Ort::Exception& e) {
        result.success = false;
        result.error_msg = std::string("ORT Error: ") + e.what();
    }

    return result;
}

inline std::string InferenceEngine::get_input_name() const { return input_name_; }

inline std::vector<int64_t> InferenceEngine::get_input_shape() const { return input_shape_; }

}  // namespace onnx_inference
```

```cpp
// week3/src/day6_cli_tool.cpp
// 命令行推理工具
// 编译：cd week3/build && cmake .. && make
// 运行：./infer --model ../models/resnet50_simplified.onnx --image ../images/cat.jpg
//       ./infer -m ../models/resnet50_simplified.onnx -i ../images/cat.jpg -t 4

#include <iostream>
#include <string>
#include <cstdlib>

#include "inference_engine.h"

void print_usage(const char* prog) {
    std::cout << "用法: " << prog << " [选项]\n"
              << "选项:\n"
              << "  -m, --model <path>   ONNX 模型文件路径（必填）\n"
              << "  -i, --image <path>   输入图片路径（必填）\n"
              << "  -t, --threads <n>    推理线程数（默认: 1）\n"
              << "  -b, --benchmark      运行 Benchmark 模式（50次推理）\n"
              << "  -h, --help           显示帮助\n"
              << "\n示例:\n"
              << "  " << prog << " -m model.onnx -i cat.jpg\n"
              << "  " << prog << " -m model.onnx -i cat.jpg -t 4 -b\n";
}

int main(int argc, char* argv[]) {
    std::string model_path;
    std::string image_path;
    int num_threads = 1;
    bool benchmark_mode = false;

    // 简单的参数解析
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if ((arg == "-m" || arg == "--model") && i + 1 < argc) {
            model_path = argv[++i];
        } else if ((arg == "-i" || arg == "--image") && i + 1 < argc) {
            image_path = argv[++i];
        } else if ((arg == "-t" || arg == "--threads") && i + 1 < argc) {
            num_threads = std::atoi(argv[++i]);
        } else if (arg == "-b" || arg == "--benchmark") {
            benchmark_mode = true;
        } else if (arg == "-h" || arg == "--help") {
            print_usage(argv[0]);
            return 0;
        }
    }

    if (model_path.empty() || image_path.empty()) {
        std::cerr << "错误: 必须指定模型和图片路径\n" << std::endl;
        print_usage(argv[0]);
        return 1;
    }

    try {
        std::cout << "============================" << std::endl;
        std::cout << "ONNX 推理命令行工具" << std::endl;
        std::cout << "============================" << std::endl;

        // 创建引擎
        onnx_inference::InferenceEngine::Config config;
        config.num_threads = num_threads;

        onnx_inference::InferenceEngine engine(model_path, config);

        // 设置日志回调
        int infer_count = 0;
        engine.set_log_callback([&infer_count](const std::string& msg) {
            std::cout << "[Engine] " << msg << std::endl;
        });

        std::cout << "模型输入: " << engine.get_input_name()
                  << " shape=[";
        auto shape = engine.get_input_shape();
        for (size_t i = 0; i < shape.size(); i++) {
            std::cout << shape[i];
            if (i < shape.size() - 1) std::cout << ",";
        }
        std::cout << "]" << std::endl;

        if (benchmark_mode) {
            // Benchmark 模式
            std::cout << "\n--- Benchmark 模式 (50次推理) ---" << std::endl;
            std::vector<double> latencies;

            for (int i = 0; i < 50; i++) {
                auto result = engine.infer_image(image_path);
                if (result.success) {
                    latencies.push_back(result.latency_ms);
                }
            }

            if (!latencies.empty()) {
                std::sort(latencies.begin(), latencies.end());
                double avg = 0;
                for (double l : latencies) avg += l;
                avg /= latencies.size();

                printf("  平均: %.2f ms | 最小: %.2f ms | P50: %.2f ms\n",
                       avg, latencies.front(), latencies[latencies.size() / 2]);
            }
        } else {
            // 单次推理
            auto result = engine.infer_image(image_path);

            if (result.success) {
                std::cout << "\n推理结果 (耗时: " << result.latency_ms << " ms):" << std::endl;
                for (int i = 0; i < static_cast<int>(result.top5.size()); i++) {
                    printf("  #%d: class_id=%4d  prob=%.4f\n",
                           i + 1,
                           result.top5[i].class_id,
                           result.top5[i].probability);
                }
            } else {
                std::cerr << "推理失败: " << result.error_msg << std::endl;
                return 1;
            }
        }

        std::cout << "\n✅ 推理完成！" << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "错误: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
```

更新 CMakeLists.txt：
```cmake
# Day6: CLI 推理工具
add_executable(infer src/day6_cli_tool.cpp)
target_link_libraries(infer onnxruntime)
if(APPLE)
    target_link_libraries(infer "-framework CoreFoundation")
    set_target_properties(infer PROPERTIES BUILD_RPATH ${ONNXRUNTIME_ROOT}/lib)
endif()
```

### 15:00-17:00：写第三篇博客

在 `week3/blog_w3.md` 中写博客，标题：**《从 Python 到 C++：移动端开发者的 ONNX Runtime C++ 推理实战》**

博客结构建议：
1. 为什么端侧 AI 必须用 C++（Python 的 GIL、包体积、启动速度）
2. Python ORT vs C++ ORT 的 API 对照表
3. C++ 前后处理踩的坑（HWC→CHW、内存对齐、stb_image）
4. C++ vs Python 性能对比数据（真实 Benchmark）
5. 封装 InferenceEngine 类的设计思路
6. 下周预告：把这个 Demo 移植到 Android

**发布到**：[掘金](https://juejin.cn) 或 [知乎](https://www.zhihu.com)

**今天的 GitHub commit**：
```bash
git add week3/
git commit -m "W3D6: CLI 推理工具完成，InferenceEngine 类封装，第三篇博客草稿"
```

---

## Day 7（周一 4/20）：JNI 接口设计 + W3 总结

**时间**：早 7:00-8:00（JNI 设计），晚 21:00-22:00（W3 总结 + W4 预习）
**目标**：设计 JNI 接口（为 W4 Android 做准备），完成 W3 自检

### 早上 7:00-8:00：JNI 接口设计

**阅读（20分钟）**：[Android JNI 官方指南](https://developer.android.com/training/articles/perf-jni)

**思考**：如何把 Day6 的 `InferenceEngine` C++ 类暴露给 Java 层？

设计 JNI 接口：

```java
// week3/src/InferenceEngine.java（接口设计，W4 才会真正实现）
// 这是 W4 Android App 的 Java 侧接口预览

package com.example.onnxinference;

public class InferenceEngine {
    // 加载 Native 库
    static {
        System.loadLibrary("onnx_inference");
    }

    // Native 方法声明
    private long nativeHandle;  // C++ 对象指针

    // 初始化引擎
    public native void init(String modelPath, int numThreads);

    // 从图片文件推理
    public native float[] inferImage(String imagePath);

    // 从 byte[] 推理（相机帧用）
    public native float[] inferFrame(byte[] frameData, int width, int height);

    // 释放资源
    public native void release();
}
```

对应的 C++ JNI 实现（伪代码，W4 真正写）：

```cpp
// week3/src/inference_engine_jni.cpp（接口设计草案）
// W4 会真正编译到 Android 项目中

#include <jni.h>
#include "inference_engine.h"

using namespace onnx_inference;

// C++ 对象 ↔ Java long 互转
static InferenceEngine* get_engine(JNIEnv* env, jobject obj) {
    jclass cls = env->GetObjectClass(obj);
    jfieldID fid = env->GetFieldID(cls, "nativeHandle", "J");
    jlong handle = env->GetLongField(obj, fid);
    return reinterpret_cast<InferenceEngine*>(handle);
}

extern "C" JNIEXPORT void JNICALL
Java_com_example_onnxinference_InferenceEngine_init(
    JNIEnv* env, jobject obj, jstring model_path, jint num_threads) {

    const char* path = env->GetStringUTFChars(model_path, nullptr);
    InferenceEngine::Config config;
    config.num_threads = num_threads;

    auto* engine = new InferenceEngine(path, config);
    env->ReleaseStringUTFChars(model_path, path);

    // 保存 C++ 对象指针到 Java
    jclass cls = env->GetObjectClass(obj);
    jfieldID fid = env->GetFieldID(cls, "nativeHandle", "J");
    env->SetLongField(obj, fid, reinterpret_cast<jlong>(engine));
}

extern "C" JNIEXPORT jfloatArray JNICALL
Java_com_example_onnxinference_InferenceEngine_inferImage(
    JNIEnv* env, jobject obj, jstring image_path) {

    auto* engine = get_engine(env, obj);
    const char* path = env->GetStringUTFChars(image_path, nullptr);

    auto result = engine->infer_image(path);
    env->ReleaseStringUTFChars(image_path, path);

    if (!result.success) return nullptr;

    // Top-5 结果转成 float array [class_id, prob, class_id, prob, ...]
    jfloatArray arr = env->NewFloatArray(result.top5.size() * 2);
    std::vector<float> data;
    for (const auto& r : result.top5) {
        data.push_back(static_cast<float>(r.class_id));
        data.push_back(r.probability);
    }
    env->SetFloatArrayRegion(arr, 0, data.size(), data.data());
    return arr;
}

extern "C" JNIEXPORT void JNICALL
Java_com_example_onnxinference_InferenceEngine_release(
    JNIEnv* env, jobject obj) {

    auto* engine = get_engine(env, obj);
    delete engine;

    jclass cls = env->GetObjectClass(obj);
    jfieldID fid = env->GetFieldID(cls, "nativeHandle", "J");
    env->SetLongField(obj, fid, 0);
}
```

### 晚上 21:00-22:00：W3 总结 + W4 预习

**W3 自检清单**：

| 项目 | 状态 |
|------|------|
| 能解释 `unique_ptr` 和 `shared_ptr` 的区别和使用场景 | [ ] |
| 理解 `std::move` 的作用，知道 move 后原对象变为空 | [ ] |
| 能用 `std::chrono` 精确计时推理耗时 | [ ] |
| ONNX Runtime C++ API 能加载模型并推理成功 | [ ] |
| C++ 推理结果和 Python 推理结果数值一致 | [ ] |
| 用 stb_image 实现了图片前处理（resize + normalize + HWC→CHW） | [ ] |
| 实现了 softmax + Top-K 后处理 | [ ] |
| CLI 工具 `./infer -m model.onnx -i cat.jpg` 能跑通 | [ ] |
| InferenceEngine C++ 类封装完成 | [ ] |
| JNI 接口设计完成（接口定义 + 伪代码） | [ ] |
| 记录了 C++ vs Python 推理性能对比数据 | [ ] |
| 写了第三篇博客并发布（或草稿完成） | [ ] |
| GitHub 有本周的 commit 记录 | [ ] |

**及格线**：完成 9 项以上 → 继续 W4
**优秀线**：完成 13 项 + 博客已发布 → 进度超预期

**面试题自测**（能流畅回答以下问题）：

1. 为什么端侧 AI 推理要用 C++ 而不是 Python？
2. `unique_ptr` 和 `shared_ptr` 有什么区别？端侧推理引擎为什么多用 `unique_ptr`？
3. `std::move` 到底做了什么？move 之后原对象还能用吗？
4. C++ 版 ONNX Runtime 和 Python 版的核心 API 有什么对应关系？
5. 图片前处理中 HWC→CHW 转换为什么要做？Python 用一行代码，C++ 怎么实现？
6. 你如何测量 C++ 推理的精确耗时？

### W4 预习

1. 阅读 [ONNX Runtime Android 官方教程](https://onnxruntime.ai/docs/tutorials/mobile/deploy-android.html)
2. 确认 Android Studio 和 NDK r25+ 已安装
3. 下载 `onnxruntime-android` AAR 文件
4. 思考：C++ 推理代码已经跑通了，移植到 Android 需要改什么？（答：CMake 配置改为 Android 交叉编译，JNI 层对接 Java，推理放 worker thread）

**今天的 GitHub commit**：
```bash
git add week3/
git commit -m "W3D7: JNI 接口设计完成，W3 总结，自检清单全部通过"
```

---

## W3 → W4 衔接说明

**W3 完成后你拥有**：

- 一个经过验证的 C++ 推理引擎（`InferenceEngine` 类）
- CLI 推理工具（`./infer --model xxx.onnx --image xxx.jpg`）
- C++ vs Python 性能对比数据
- JNI 接口设计草案（Java 侧 + C++ 侧）

**W4 要做的事**：

1. 创建 Android 项目，配置 NDK + CMake 交叉编译
2. 把 C++ 推理代码编译成 Android 可用的 `.so`
3. 通过 JNI 让 Java 层调 C++ 推理接口
4. 接入 CameraX，实现实时帧推理
5. 在画面上叠加推理结果 + 性能数据

**W4 的核心挑战**：从"桌面端命令行"到"Android 实时 App"，需要处理：
- NDK 交叉编译配置（ARM64/ARMv7）
- JNI 线程安全（推理线程 vs UI 线程）
- CameraX 帧格式转换（YUV→RGB→前处理）
- 内存管理（大张量不能在 UI 线程分配）

---

## 本周学习资源汇总

### 官方文档（必读，按天对应）

| 资源 | 链接 | 对应天 |
|------|------|--------|
| 《现代C++教程》（在线版） | https://changkun.de/modern-cpp/zh-cn/ | Day 1 |
| cppreference | https://en.cppreference.com/w/ | 全程参考 |
| ONNX Runtime C++ API 文档 | https://onnxruntime.ai/docs/api/c/index.html | Day 3 |
| ONNX Runtime C++ 示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/c_cxx | Day 3 |
| stb_image 单头文件 | https://github.com/nothings/stb/blob/master/stb_image.h | Day 4 |
| stb_image_resize2 | https://github.com/nothings/stb/blob/master/stb_image_resize2.h | Day 4 |
| CMake 官方教程 | https://cmake.org/cmake/help/latest/guide/tutorial/index.html | Day 2 |
| Android JNI 指南 | https://developer.android.com/training/articles/perf-jni | Day 7 |
| ONNX Runtime Android 教程 | https://onnxruntime.ai/docs/tutorials/mobile/deploy-android.html | Day 7 预习 |

### 视频教程（辅助理解）

| 课程 | 平台 | 时长 | 对应天 |
|------|------|------|--------|
| C++ Smart Pointers - The Cherno | YouTube | 18min | Day 1 |
| Move Semantics - The Cherno | YouTube | 16min | Day 1 |
| C++ Lambda - The Cherno | YouTube | 16min | Day 1 |
| CMake Tutorial for Beginners | YouTube | 15min | Day 2 |
| Memory Alignment - Jason Turner | YouTube | 10min | Day 2 |
| ONNX Runtime C++ Inference | YouTube/B站 | 30min | Day 3 |
| stb_image tutorial | YouTube | 12min | Day 4 |
| Image Preprocessing for NN (C++) | YouTube | 15min | Day 4 |

> **B站搜索关键词替代**："C++ 智能指针"、"C++ move语义"、"C++ lambda表达式"、"CMake 入门"、"ONNX Runtime C++ 推理"、"C++ 图片预处理"

### 实战项目（GitHub，必看）

| 项目 | 链接 | 学习重点 |
|------|------|---------|
| ONNX Runtime C++ 示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/c_cxx | 完整 C++ 推理流程 |
| ONNX Runtime Android 示例 | https://github.com/microsoft/onnxruntime-inference-examples/tree/main/mobile/examples/android | JNI 集成（Day7 参考） |
| 现代 C++ 教程代码 | https://github.com/changkun/modern-cpp-tutorial | C++17 特性示例 |
| stb 单头文件库集合 | https://github.com/nothings/stb | 图片处理工具 |

### 书籍推荐

| 书名 | 章节 | 优先级 |
|------|------|--------|
| 《现代C++教程》（开源） | 第3/5/6/7章 | ⭐⭐⭐⭐⭐ |
| 《Effective C++》 | 第1-3章（资源管理） | ⭐⭐⭐⭐ |
| cppreference.com | 查阅 API | ⭐⭐⭐⭐ |

---

## 本周 GitHub 仓库结构

```
on-device-ai-journey/
├── README.md
├── week1/
│   └── ...（W1 已完成）
├── week2/
│   └── ...（W2 已完成）
└── week3/
    ├── README.md                      # W3 总结 + 性能数据
    ├── CMakeLists.txt                 # CMake 构建配置
    ├── src/
    │   ├── day1_modern_cpp.cpp        # Day1: 现代 C++ 特性
    │   ├── day3_ort_cpp_inference.cpp # Day3: C++ ORT 推理
    │   ├── day5_benchmark.cpp         # Day5: Benchmark
    │   ├── day6_cli_tool.cpp          # Day6: CLI 推理工具
    │   ├── tensor_utils.h             # 内存对齐 + 计时工具
    │   ├── image_utils.h              # 图片前后处理
    │   ├── inference_engine.h         # 推理引擎封装类
    │   ├── inference_engine_jni.cpp   # Day7: JNI 接口设计草案
    │   ├── InferenceEngine.java       # Day7: Java 侧接口定义
    │   ├── stb_image.h                # 图片解码库
    │   └── stb_image_resize2.h        # 图片缩放库
    ├── models/
    │   └── resnet50_simplified.onnx   # 复用 W2 导出的模型
    ├── build/                         # CMake 构建目录
    ├── notes_benchmark.md             # 性能对比笔记
    └── blog_w3.md                     # 第三篇博客草稿
```

---

*基于《端侧AI工程师3个月冲刺计划 v3.0》及《每周学习资源库 v3.1》制定。*
*执行周期：2026年4月14日 - 4月20日*
*生成时间：2026年5月12日*
