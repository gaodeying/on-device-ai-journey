# Jupyter Notebook 与 JupyterLab 快速入门

面向「能跑 Python、想马上用起来」的读者：安装、启动、界面与常用操作一页通关。建议与 Conda 虚拟环境一起使用，避免污染系统 Python。

---

## 1. 它们是什么、有什么区别

| 项目 | Jupyter Notebook | JupyterLab |
|------|------------------|------------|
| 定位 | 经典单文档笔记本界面 | 下一代工作台：多标签、终端、编辑器等 |
| 文件格式 | 都是 `.ipynb`（JSON），可互相打开 | 同上 |
| 适用场景 | 单篇教程、演示、轻量探索 | 同时开多个笔记本/文件/终端 |

**结论**：学哪一个都行；习惯「一个窗口搞定多件事」优先用 **JupyterLab**。官方长期主推 Lab。

---

## 2. 环境准备（推荐 Conda）

若你已有 `conda` 与某个环境（例如 `pytorch`），可先激活：

```bash
conda activate <你的环境名>
```

### 2.1 安装 Jupyter 全家桶（Notebook + Lab）

```bash
conda install -c conda-forge jupyterlab notebook ipykernel
```

或仅用 pip（在**已激活**的虚拟环境中）：

```bash
pip install jupyterlab notebook ipykernel
```

### 2.2 让当前环境出现在内核列表里（可选）

在已激活环境中执行：

```bash
python -m ipykernel install --user --name <内核显示名> --display-name "Python (显示名)"
```

之后在笔记本右上角「内核」里可选该环境。

---

## 3. 启动方式

### 3.1 Jupyter Notebook（经典界面）

在项目目录下打开终端，执行：

```bash
jupyter notebook
```

浏览器会打开；界面以「文件树 + 单笔记本」为主。

### 3.2 JupyterLab（推荐）

```bash
jupyter lab
```

或指定端口、禁止自动开浏览器等：

```bash
jupyter lab --port 8889 --no-browser
```

终端里会打印带 `token` 的 URL，复制到浏览器即可。

### 3.3 指定工作目录

先 `cd` 到你想作为根目录的文件夹再启动，或在启动时指定：

```bash
jupyter lab --notebook-dir=/path/to/your/project
```

---

## 4. 界面速览

### 4.1 共有概念（Notebook 与 Lab 一致）

- **笔记本（.ipynb）**：由多个「单元格」组成。
- **单元格类型**
  - **Code**：写 Python（或其他已安装内核的语言），`Shift + Enter` 运行当前格并在下方插入新格（或聚焦下一格，视设置而定）。
  - **Markdown**：写说明文字、公式、列表等；运行后渲染为排版后的文档。
- **内核（Kernel）**：真正执行代码的进程。右上角可切换内核（不同 Conda 环境对应不同内核）。
- **执行顺序**：左侧 `In [1]`、`In [2]` 表示执行次序；**不要依赖**「从上往下一定等于执行顺序」，改代码后建议 **Kernel → Restart** 再从头跑一遍重要流程。

### 4.2 JupyterLab 多出来的能力

- 左侧 **文件浏览器**：打开多个 `.ipynb`、`.py`、图片等。
- **终端**：`File → New → Terminal`（或在启动器里选 Terminal）。
- **文本编辑器**：直接编辑仓库里的 `.py`、`.md` 等。
- **分屏**：拖动标签到左右/上下，对照代码与文档。

---

## 5. 必会操作清单

1. **新建笔记本**：启动器里选「Notebook」或「Python 3」等内核。
2. **切换单元格类型**：命令模式按 `Y`（Code）、`M`（Markdown）（见下节快捷键）。
3. **运行当前格**：`Shift + Enter`。
4. **仅运行不跳转**：部分配置下 `Ctrl + Enter`（macOS 上多为 `Control + Enter`）。
5. **保存**：`Ctrl + S` / `Cmd + S`；Lab 可开自动保存。
6. **中断运行**：工具栏「停止」或 `Kernel → Interrupt`。
7. **重启内核**：改了大量状态变量或 import 后，用 `Kernel → Restart` 避免「旧变量残留」。

---

## 6. 常用快捷键（命令模式 vs 编辑模式）

- **命令模式**：单元格边框为**蓝色**（未在单元格内打字）。按 `Esc` 进入。
- **编辑模式**：单元格边框为**绿色**，光标在格子里打字。按 `Enter` 进入。

| 操作 | 快捷键（常见默认） |
|------|-------------------|
| 运行本格并选中下一格 | `Shift + Enter` |
| 运行本格 | `Ctrl + Enter`（Mac 上常是 `Control + Enter`） |
| 命令模式：上方插入格 | `A` |
| 命令模式：下方插入格 | `B` |
| 命令模式：删除格 | `D` `D`（连按两次 D） |
| 命令模式：切为 Code | `Y` |
| 命令模式：切为 Markdown | `M` |
| 命令模式：显示快捷键帮助 | `H` |

> 不同版本/浏览器下极少数快捷键可能略有差异，以 `H` 弹出的说明为准。

---

## 7. Markdown 小抄（写笔记用）

在 Markdown 单元格里可使用：

- 标题：`#` `##` `###`
- 行内代码：`` `变量名` ``
- 代码块：三反引号包裹
- 列表：`-` 或 `1.`
- LaTeX 公式（若前端支持）：行内 `$...$`，块级 `$$...$$`

---

## 8. 与 PyTorch / 深度学习相关的实用习惯

- **设备与随机种子**：改 `device` 或 `torch.manual_seed` 后，若中间变量仍留在内存，建议 **Restart Kernel** 再跑，避免误判结果。
- **大图与显存**：长时间调试可 `plt.close()` 或不用时关图，减少偶发卡顿（主要仍取决于任务规模）。
- **长时间训练**：笔记本适合实验脚本；正式多 epoch 训练更常见做法是：在 `.py` + 终端或任务系统里跑，笔记本只做结果可视化。

---

## 9. 导出与分享

- **File → Save and Export Notebook As…**：可导出 HTML、PDF（需额外依赖）、`.py` 等。
- **Git**：`.ipynb` 是 JSON，**diff 会很长**。团队协作时可约定：关键逻辑同步维护一份 `.py`，或对笔记本做 `nbconvert` 导出再 review。

---

## 10. 常见问题

**Q：浏览器打不开或端口被占用**  
A：换端口 `jupyter lab --port 8890`；或使用 `--no-browser` 复制带 token 的链接。

**Q：`ModuleNotFoundError`**  
A：当前笔记本选用的**内核**不是你装包的那个环境。在右上角换内核，或在对应环境里 `pip/conda install` 该包。

**Q：卡在 `In [*]` 很久**  
A：可能是计算久或死锁；先 **Interrupt**，不行再 **Restart Kernel**。

**Q：想完全退出**  
A：在运行 `jupyter` 的终端按 `Ctrl + C`，按提示确认 shutdown。

---

## 11. 建议你这样选

- **跟教程、单文件演练**：Jupyter Notebook 或 JupyterLab 均可。  
- **同周还要改仓库里的脚本、开终端测 ONNX**：优先 **JupyterLab**，或 **Cursor / VS Code 打开 `.ipynb`**，与工程文件同一套编辑器。

---

## 12. 参考命令速查

```bash
# 安装
conda install -c conda-forge jupyterlab notebook ipykernel

# 启动 Lab（推荐）
jupyter lab

# 启动经典 Notebook
jupyter notebook

# 注册当前环境为可选内核
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

---

*文档版本：快速入门 v1，与 Week2 学习记录配套。*
