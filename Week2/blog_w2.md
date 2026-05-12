# 《移动开发者的 ONNX 第一课：从 PyTorch 到端侧推理》

> 第二周学习总结（W2）：从“能导出”到“能跑通端到端”，把模型部署链路完整走一遍。

---

## 一、为什么移动开发者需要 ONNX？

做移动端 AI 落地时，经常会遇到这几个问题：

- 训练同学给的是 PyTorch 模型（`.pt/.pth`），端上直接跑不方便；
- Android / iOS / C++ 服务端希望共用同一份模型；
- 模型迭代很快，希望推理层尽量稳定，减少重复适配成本。

ONNX 的价值就在这里：它是训练框架和推理框架之间的“中间协议层”。

你可以把它理解为：

- PyTorch：擅长训练和实验；
- ONNX：负责模型表达与交换；
- ONNX Runtime：负责跨平台高性能推理。

对于移动开发者，这意味着：训练侧可以持续迭代，端侧只要按 ONNX 协议接入，就能稳定跟上模型版本。

---

## 二、本周我完成了什么？

我在项目里做了一条完整链路：

1. 加载 `ResNet50` 预训练模型；
2. 导出 ONNX（动态 batch）；
3. 用 ONNX Runtime 建立推理 Session；
4. 读取测试图片，做预处理，执行推理；
5. 输出 Top-5 类别结果；
6. 对比 PyTorch 与 ONNX Runtime 的耗时和结果误差。

对应脚本：`Week2/scripts/day6_end_to_end_demo.py`。

---

## 三、从 PyTorch 到 ONNX：核心导出代码

导出逻辑核心是 `torch.onnx.export`：

```python
torch.onnx.export(
    model, dummy, str(onnx_path),
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={
        "input": {0: "batch_size"},
        "output": {0: "batch_size"}
    },
    opset_version=18
)
```

其中最关键的两个参数：

- `dynamic_axes`：将 batch 维声明为动态，后续既可推理 `N=1`，也可推理 `N>1`；
- `opset_version`：算子标准版本。本周实践中使用 18，避免导出器降级转换带来的噪音日志。

---

## 四、我踩过的坑（真实排查记录）

### 坑 1：路径问题导致导出失败

现象：导出时报 `FileNotFoundError: ... .onnx.data`。  
原因：脚本在 `Week2/scripts` 目录下运行时，相对路径会被错误拼接。  
处理：

- 使用基于 `__file__` 的绝对路径；
- 导出前确保父目录存在：`mkdir(parents=True, exist_ok=True)`。

这一步非常关键，移动端工程里路径问题是高频坑。

### 坑 2：输入尺寸不匹配

现象：ORT 推理报错：

`INVALID_ARGUMENT: Got 256 Expected 224`

原因：图片预处理写成了 `CenterCrop(256)`，模型输入是 `224x224`。  
处理：改为 `Resize(256) + CenterCrop(224)`，与 ResNet 训练分布保持一致。

### 坑 3：日志里有 Traceback 但流程仍成功

现象：导出时有版本转换异常日志，但后续推理仍成功。  
原因：导出器先导出更高 opset，再尝试降级转换；降级失败时回退为可用模型。  
结论：这类日志不一定是致命错误，要看最终是否“导出成功 + 能推理”。

---

## 五、ONNX Runtime 推理核心 API（移动视角）

核心代码非常简洁：

```python
sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
ort_session = ort.InferenceSession(str(onnx_path), sess_options=sess_options)

input_name = ort_session.get_inputs()[0].name
output_name = ort_session.get_outputs()[0].name
result = ort_session.run([output_name], {input_name: input_np})[0]
```

几个要点：

- `InferenceSession` 是所有推理的入口；
- 输入必须是 numpy，shape 和 dtype 必须对齐模型；
- 先取 `input_name` / `output_name` 再喂数据，不要手写字符串硬编码。

这套调用方式和未来 C++ API 的思路非常接近（都是 Session + 输入输出张量），所以这周的 Python 实战其实已经在给下周 C++ 铺路。

---

## 六、PyTorch vs ONNX Runtime：本机真实数据

测试环境：本机 CPU，单张图片 `Week2/scripts/banana1.jpg`，ResNet50，50 次平均（10 次预热）。

| 指标 | PyTorch | ONNX Runtime |
|---|---:|---:|
| 平均推理耗时（ms） | 27.854 | 15.566 |

输出一致性：

- 最大绝对误差（`max_abs_diff`）= `0.000002`

结论：

- ORT 在该场景下约快 **44%**；
- 数值误差在可接受范围内，结果一致性良好。

> 说明：不同机器、线程数、provider（CPU/GPU/NNAPI）会影响绝对耗时，建议你在目标设备上复测。

---

## 七、这周我真正学到的 3 件事

1. **部署不是“导出就完事”**：路径、输入协议、opset、后处理每个环节都可能踩坑。  
2. **日志要分级看**：有 Traceback 不一定失败，要结合最终产物和推理结果判断。  
3. **工程化比单点代码更重要**：稳定路径、缓存标签、容错逻辑，才是端侧可交付代码的基础。

---

## 八、下周预告：从 Python ORT 到 C++ ORT

W3 计划是把这周导出的 ONNX 模型接到 C++ 推理程序里，做一个命令行版本：

```bash
./inference resnet50_dynamic_batch.onnx image.jpg
```

重点会放在：

- CMake + ONNX Runtime C++ SDK 集成；
- `Ort::Env`、`Ort::Session`、`Ort::Value` 的基本用法；
- Python vs C++ 推理速度对比与工程差异分析。

---

## 九、附：我本周的最小可复现清单

- ONNX 文件可成功导出（动态 batch）；
- ORT 可读取模型并成功推理；
- Top-5 可输出标签；
- PyTorch vs ORT 误差 `< 1e-4`；
- 性能对比数据可复现并已记录。

这篇算是我“ONNX 入门第一课”的完整闭环。  
如果你也在做移动端 AI，建议从一条最短链路开始：**先跑通，再优化**。

