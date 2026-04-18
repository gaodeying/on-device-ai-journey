# Conda 通俗介绍与快速入门（给端侧 AI 学习者）

> 适用人群：有开发经验，但刚接触 Python/AI 环境管理  
> 阅读时间：15-20 分钟  
> 目标：看完就能独立创建、使用、删除 Conda 环境，并安装 PyTorch

---

## 1. Conda 是什么？一句话解释

**Conda 就像“项目专属工具箱管理器”**。

你可以把它理解成：
- 每个项目都配一个独立工具箱（独立 Python 版本 + 独立依赖包）
- 项目 A 用 Python 3.10，项目 B 用 Python 3.12，互不影响
- 不会再出现“我昨天装了个包，今天另一个项目崩了”的情况

---

## 2. 为什么你现在就该用 Conda？

你后面会学 `PyTorch / ONNX / coremltools / onnxruntime`，这些库对版本比较敏感。  
如果不用环境隔离，常见问题是：

- A 项目要求 `numpy==1.x`，B 项目要求 `numpy==2.x`，冲突
- 系统 Python 被污染，升级后一堆脚本报错
- 教程复制命令后跑不通，不知道是代码问题还是环境问题

**用 Conda 的核心收益**：把“环境问题”变成“可重复、可回滚”的工程问题。

---

## 3. 关键概念（必须懂）

### `base` 环境
- Conda 安装后默认有一个 `base`
- 建议：**不要在 `base` 里安装业务依赖**
- `base` 只保留 Conda 自身和少量通用工具

### 虚拟环境（env）
- 每个项目一个环境，例如 `ondevice-ai`
- 环境里有自己独立的 Python 和包

### 激活（activate）
- 激活后，你的终端就“切换进这个工具箱”
- 后续 `python` / `pip` 都作用在当前环境

---

## 4. 安装 Conda（Mac）

推荐安装 **Miniconda**（轻量，够用）：
- 官方地址：[https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

安装后重开终端，执行：

```bash
conda --version
```

看到版本号表示安装成功。

如果命令找不到，执行：

```bash
source ~/.zshrc
```

---

## 5. 5 分钟快速上手（可直接复制）

## Step 1：创建环境

```bash
conda create -n ondevice-ai python=3.10 -y
```

说明：
- `-n ondevice-ai`：环境名
- `python=3.10`：指定 Python 版本

## Step 2：激活环境

```bash
conda activate ondevice-ai
```

激活后，终端前面通常会出现 `(ondevice-ai)`。

## Step 3：检查 Python 路径（确认隔离成功）

```bash
which python
python --version
```

你会看到路径指向 Conda 环境目录，而不是系统 Python。

## Step 4：安装本周要用的包

```bash
pip install torch torchvision numpy matplotlib pillow
```

> 说明：在 Conda 环境里用 `pip` 安装完全没问题。  
> 原则是：**先激活环境，再安装包**。

## Step 5：验证安装

```bash
python -c "import torch, numpy; print(torch.__version__, numpy.__version__)"
```

能输出版本号就 OK。

---

## 6. 日常高频命令速查

```bash
# 查看所有环境
conda env list

# 查看当前环境已安装的包
conda list

# 退出当前环境
conda deactivate

# 删除环境（彻底清理）
conda remove -n ondevice-ai --all -y

# 导出环境（给同学/未来自己复现）
conda env export > environment.yml

# 根据配置文件恢复环境
conda env create -f environment.yml
```

---

## 7. 推荐工作流（避免踩坑）

每开始一个新项目，固定 4 步：

1. `conda create -n 项目名 python=版本`
2. `conda activate 项目名`
3. 安装依赖（`pip install ...`）
4. `conda env export > environment.yml`（留存）

这样你以后换电脑、换系统、回滚版本都很稳。

---

## 8. 常见问题（新手高频）

### Q1：`conda activate` 报错，怎么办？

先执行：

```bash
conda init zsh
source ~/.zshrc
```

然后重开终端再试。

### Q2：我能不能只用 `pip`，不用 Conda？

可以，但对你当前目标（端侧 AI 多库切换）不推荐。  
`pip` 管包很好，**Conda 的优势是“环境管理”**。

### Q3：`base` 环境里已经装了一堆包，要不要清理？

不用折腾历史包，**从现在开始新项目都在新环境里做**即可。

### Q4：Conda 和 venv 有什么区别？

- `venv`：只管 Python 虚拟环境（轻量）
- `Conda`：环境 + 包管理一体化，跨平台和复杂依赖更稳

对你的学习阶段，Conda 更省心。

---

## 9. 结合你 W1 学习计划的最小命令集

每天基本就这几条：

```bash
# 进入学习环境
conda activate ondevice-ai

# 跑脚本
python week1/day4_pytorch_tensor.py

# 装新依赖（例如后面会用到）
pip install onnx onnxruntime netron

# 结束学习
conda deactivate
```

---

## 10. 一句话总结

**Conda 不是 AI 技术本身，但它能把你从“环境地狱”里救出来，让你把精力放在模型和工程能力上。**

---

*创建时间：2026-03-26*  
*建议放置位置：职业规划/W1*  
