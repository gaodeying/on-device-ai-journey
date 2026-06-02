# AGENTS — Git_on-device-ai-journey

本文件描述 **整个 Git 仓库** `Git_on-device-ai-journey`（`/Users/gaodeying/Desktop/Git_on-device-ai-journey`）。

## 仓库用途

端侧 AI 系统性学习仓库。按周推进，记录从 PyTorch 基础到端侧部署的完整学习历程，辅助作者从移动端全栈工程师转型为端侧 AI 工程师。

## 结构

```
Git_on-device-ai-journey/
├── aijourney              ← 命令入口（语义化 wrapper）
├── manage.py             ← 管理脚本（核心逻辑）
├── 学习索引.md            ← 打开即见（进度+产出全景）
├── .aijourney/config.json ← 配置
├── Week1/                ← 第1周：Python + PyTorch 基础
├── Week2/                ← 第2周：ONNX 导出与推理
├── Week3/                ← 第3周：C++ ORT 推理
├── ...                   ← 按周递增
├── 职业规划/              ← 12周冲刺计划、每周详细计划、资源库
├── 量化交易/              ← 副线学习（量化交易探索）
├── output/               ← 沉淀产出
│   ├── blogs/            ← 技术博客
│   ├── interview/        ← 面试知识点卡片
│   └── index.md          ← 产出索引
└── AGENTS.md
```

## 打开仓库先看

- [学习索引.md](学习索引.md) — 全仓学习地图

## 管理命令

```bash
./aijourney scan            # 刷新学习索引
./aijourney status          # 学习进度概览（当前周、完成率）
./aijourney plan [week]     # 查看某周学习计划
./aijourney review [week]   # 回顾某周产出，生成总结
./aijourney distill [week]  # 从某周提炼面试知识点/博客到 output/
./aijourney progress        # 对照12周计划，显示整体进度
```

## 每个 Week 目录

必须包含 `META.yaml`：

```yaml
title: 本周主题
week: 2
status: completed       # learning / completed
started: 2026-04-08
finished: 2026-04-14    # 完成时填写
topics: [ONNX, ORT]    # 本周涉及的技术关键词
output:                 # 本周产出清单
  - blog_w2.md
  - scripts/day6_end_to_end_demo.py
```

## 沉淀流程

学习完成后的标准流程：`review` 回顾产出 → `distill` 提炼面试知识点或博客 → 产出存入 `output/`。

沉淀类型：
- **blog**：技术博客（可发布到外部平台）
- **interview**：面试知识点卡片（简明 Q&A 格式）
- **summary**：阶段性学习总结

## 与 AiCoding 仓库的关系

本仓库专注于**个人学习**，不涉及工作需求管理。与 `Git_aicoding` 的区别：
- 驱动模式：学习计划驱动（按周） vs 需求驱动（按任务）
- 状态机：learning/completed（两态） vs active/paused/completed（三态）
- 沉淀方向：面试材料+博客（留在仓库内） vs 通用规范（发布到知识库）

## AI 协作约定

- AI 打开本仓库时，应先运行 `./aijourney status` 了解当前学习进度和所处阶段
- AI 辅助学习时，应参考 `职业规划/` 下的计划文档了解学习目标和节奏
- 每次学习 session 结束后，AI 应提醒更新 META.yaml 的 output 字段
- AI 生成的学习材料（代码示例、解释文档）直接放在对应 Week 目录下
- 面试知识点提炼时，格式为：问题 → 核心答案 → 代码示例 → 延伸追问
- 新开一周学习时，AI 应自动创建 `WeekN/META.yaml` 并设置 status 为 learning
