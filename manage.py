#!/usr/bin/env python3
"""Git_on-device-ai-journey 学习仓库管理脚本。

命令：
  scan      刷新学习索引
  status    学习进度概览
  plan      查看某周学习计划
  review    回顾某周产出
  distill   从某周提炼面试知识点/博客
  progress  对照12周计划显示整体进度
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent


# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def load_config() -> dict:
    cfg_path = ROOT / ".aijourney" / "config.json"
    if not cfg_path.exists():
        print("❌ 配置文件不存在：.aijourney/config.json")
        sys.exit(1)
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def find_week_dirs() -> list[Path]:
    """找到所有 Week* 目录，按数字排序。"""
    dirs = [d for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("Week")]
    dirs.sort(key=lambda p: int(p.name.replace("Week", "") or "0"))
    return dirs


def load_meta(week_dir: Path) -> dict | None:
    meta_path = week_dir / "META.yaml"
    if not meta_path.exists():
        return None
    return yaml.safe_load(meta_path.read_text(encoding="utf-8"))


def week_number(week_dir: Path) -> int:
    return int(week_dir.name.replace("Week", ""))


# ─── scan ─────────────────────────────────────────────────────────────────────

def cmd_scan():
    """刷新学习索引.md。"""
    cfg = load_config()
    week_dirs = find_week_dirs()
    side_tracks = cfg.get("side_tracks", [])

    lines = [
        "# 学习索引",
        "",
        f"> 端侧 AI 学习之旅 | 计划周期：{cfg['start_date']} → {cfg['end_date']}（{cfg['total_weeks']}周）",
        "",
        "---",
        "",
        "## 学习周进度",
        "",
        "| 周 | 主题 | 状态 | 开始 | 完成 | 关键产出 |",
        "|:--:|------|:----:|------|------|----------|",
    ]

    completed_count = 0
    for wd in week_dirs:
        meta = load_meta(wd)
        wn = week_number(wd)
        if meta:
            title = meta.get("title", "—")
            status = meta.get("status", "learning")
            started = meta.get("started", "—")
            finished = meta.get("finished", "—")
            outputs = meta.get("output", [])
            output_str = "、".join(outputs[:3]) if outputs else "—"
            status_icon = "✅" if status == "completed" else "📖"
            if status == "completed":
                completed_count += 1
        else:
            title = wd.name
            status_icon = "⬜"
            started = "—"
            finished = "—"
            output_str = "（无 META.yaml）"
        lines.append(f"| W{wn} | {title} | {status_icon} | {started} | {finished} | {output_str} |")

    lines.append("")
    lines.append(f"**进度**：{completed_count}/{len(week_dirs)} 周已完成")
    lines.append("")

    # 副线学习
    if side_tracks:
        lines.append("---")
        lines.append("")
        lines.append("## 副线学习")
        lines.append("")
        for track in side_tracks:
            track_dir = ROOT / track
            if track_dir.is_dir():
                file_count = len(list(track_dir.glob("*")))
                lines.append(f"- **{track}**（{file_count} 个文件）")
        lines.append("")

    # 产出目录
    output_dir = ROOT / cfg.get("output_dir", "output")
    if output_dir.is_dir():
        lines.append("---")
        lines.append("")
        lines.append("## 沉淀产出")
        lines.append("")
        for sub in sorted(output_dir.iterdir()):
            if sub.is_dir():
                md_count = len(list(sub.glob("*.md")))
                lines.append(f"- **{sub.name}/**（{md_count} 篇）")
        lines.append("")

    # 辅助资料
    lines.append("---")
    lines.append("")
    lines.append("## 辅助资料")
    lines.append("")
    lines.append("- [12周冲刺计划](职业规划/最终版_端侧AI工程师_3个月冲刺计划_v3.0_优化版.md)")
    lines.append("- [学习资源库](职业规划/端侧AI工程师_每周学习资源库_v3.1.md)")
    lines.append("- [每周详细计划](职业规划/每周计划/)")
    lines.append("")

    index_path = ROOT / "学习索引.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 学习索引已刷新 → 学习索引.md（{len(week_dirs)} 周，{completed_count} 已完成）")


# ─── status ───────────────────────────────────────────────────────────────────

def cmd_status():
    """学习进度概览。"""
    cfg = load_config()
    week_dirs = find_week_dirs()

    total = cfg["total_weeks"]
    completed = 0
    learning = 0
    current_week = None

    for wd in week_dirs:
        meta = load_meta(wd)
        if meta:
            status = meta.get("status", "learning")
            if status == "completed":
                completed += 1
            elif status == "learning":
                learning += 1
                current_week = wd

    # 计算时间进度
    start = datetime.strptime(cfg["start_date"], "%Y-%m-%d").date()
    end = datetime.strptime(cfg["end_date"], "%Y-%m-%d").date()
    today = date.today()
    total_days = (end - start).days
    elapsed_days = (today - start).days
    time_pct = min(100, max(0, int(elapsed_days / total_days * 100)))
    learn_pct = int(completed / total * 100) if total > 0 else 0

    print("╭─────────────────────────────────────────╮")
    print("│     端侧 AI 学习之旅 · 进度概览        │")
    print("╰─────────────────────────────────────────╯")
    print()
    print(f"  📅 计划周期：{cfg['start_date']} → {cfg['end_date']}")
    print(f"  ⏱  时间进度：{time_pct}%（已过 {elapsed_days}/{total_days} 天）")
    print(f"  📖 学习进度：{learn_pct}%（{completed}/{total} 周已完成）")
    print(f"  🔄 进行中：{learning} 周")
    print()

    if current_week:
        meta = load_meta(current_week)
        title = meta.get("title", current_week.name) if meta else current_week.name
        print(f"  📍 当前：{current_week.name} — {title}")

    # 进度条
    bar_len = 30
    filled = int(bar_len * completed / total)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"\n  [{bar}] {completed}/{total}")
    print()


# ─── plan ─────────────────────────────────────────────────────────────────────

def cmd_plan(week_num: int | None = None):
    """查看某周学习计划。"""
    cfg = load_config()
    plans_dir = ROOT / cfg.get("weekly_plans_dir", "职业规划/每周计划")

    if week_num is None:
        # 找当前进行中的周
        for wd in find_week_dirs():
            meta = load_meta(wd)
            if meta and meta.get("status") == "learning":
                week_num = week_number(wd)
                break
        if week_num is None:
            print("💡 未指定周数，且没有 status=learning 的周。用法：./aijourney plan 3")
            return

    # 查找计划文件
    target_dir = plans_dir / f"W{week_num}"
    if not target_dir.is_dir():
        print(f"❌ 未找到计划目录：{target_dir}")
        return

    plans = list(target_dir.glob("*.md"))
    if not plans:
        print(f"❌ {target_dir} 下没有 .md 文件")
        return

    # 优先选 CatDesk 版本
    chosen = plans[0]
    for p in plans:
        if "CatDesk" in p.name:
            chosen = p
            break

    print(f"📋 第 {week_num} 周学习计划：{chosen.name}")
    print("─" * 50)
    content = chosen.read_text(encoding="utf-8")
    # 只打印前 80 行
    for i, line in enumerate(content.splitlines()[:80]):
        print(line)
    if len(content.splitlines()) > 80:
        print(f"\n... 共 {len(content.splitlines())} 行，完整内容见：{chosen}")


# ─── review ───────────────────────────────────────────────────────────────────

def cmd_review(week_num: int | None = None):
    """回顾某周产出。"""
    if week_num is None:
        # 找最近完成的周
        for wd in reversed(find_week_dirs()):
            meta = load_meta(wd)
            if meta and meta.get("status") == "completed":
                week_num = week_number(wd)
                break
        if week_num is None:
            print("💡 未指定周数。用法：./aijourney review 2")
            return

    week_dir = ROOT / f"Week{week_num}"
    if not week_dir.is_dir():
        print(f"❌ 目录不存在：Week{week_num}")
        return

    meta = load_meta(week_dir)
    print(f"📝 Week{week_num} 回顾")
    print("─" * 50)

    if meta:
        print(f"  主题：{meta.get('title', '—')}")
        print(f"  状态：{meta.get('status', '—')}")
        print(f"  时间：{meta.get('started', '?')} → {meta.get('finished', '进行中')}")
        topics = meta.get("topics", [])
        if topics:
            print(f"  关键词：{', '.join(topics)}")
        outputs = meta.get("output", [])
        if outputs:
            print(f"\n  📦 产出（{len(outputs)} 项）：")
            for o in outputs:
                exists = "✓" if (week_dir / o).exists() else "✗"
                print(f"    [{exists}] {o}")
    else:
        print("  ⚠️  无 META.yaml，列出目录内容：")

    # 列出所有文件
    print(f"\n  📁 目录文件：")
    for f in sorted(week_dir.iterdir()):
        if f.name.startswith("."):
            continue
        if f.is_dir():
            sub_count = len(list(f.rglob("*")))
            print(f"    📂 {f.name}/ ({sub_count} 项)")
        else:
            size_kb = f.stat().st_size / 1024
            print(f"    📄 {f.name} ({size_kb:.1f} KB)")
    print()


# ─── distill ──────────────────────────────────────────────────────────────────

def cmd_distill(week_num: int | None = None):
    """提示用户进行知识提炼（实际提炼由 AI 完成）。"""
    if week_num is None:
        print("💡 用法：./aijourney distill 2")
        print("   将从 Week2 的学习内容中提炼面试知识点或博客。")
        return

    week_dir = ROOT / f"Week{week_num}"
    if not week_dir.is_dir():
        print(f"❌ 目录不存在：Week{week_num}")
        return

    meta = load_meta(week_dir)
    cfg = load_config()
    output_dir = ROOT / cfg.get("output_dir", "output")

    print(f"🧪 准备从 Week{week_num} 提炼知识")
    print("─" * 50)

    if meta:
        print(f"  主题：{meta.get('title', '—')}")
        topics = meta.get("topics", [])
        if topics:
            print(f"  关键词：{', '.join(topics)}")

    # 找到可提炼的内容
    md_files = list(week_dir.glob("*.md"))
    py_files = list(week_dir.glob("*.py")) + list(week_dir.glob("scripts/*.py"))
    cpp_files = list(week_dir.glob("*.cpp")) + list(week_dir.glob("scripts/*.cpp"))

    print(f"\n  可提炼素材：")
    print(f"    Markdown：{len(md_files)} 篇")
    print(f"    Python 脚本：{len(py_files)} 个")
    if cpp_files:
        print(f"    C++ 文件：{len(cpp_files)} 个")

    print(f"\n  📤 产出目录：{output_dir}")
    print(f"\n  💡 提炼类型：")
    print(f"    1. blog     → output/blogs/（技术博客）")
    print(f"    2. interview → output/interview/（面试知识点卡片）")
    print(f"    3. summary  → output/（阶段总结）")
    print(f"\n  请在 AI 对话中指定提炼方向，AI 将读取本周内容并生成产出。")


# ─── progress ─────────────────────────────────────────────────────────────────

def cmd_progress():
    """对照12周计划显示整体进度。"""
    cfg = load_config()
    total = cfg["total_weeks"]
    week_dirs = find_week_dirs()

    # 从计划文件读取每周主题（简化版：从 META.yaml 获取）
    print("📊 12 周学习进度总览")
    print("═" * 55)

    for wn in range(1, total + 1):
        week_dir = ROOT / f"Week{wn}"
        if week_dir.is_dir():
            meta = load_meta(week_dir)
            if meta:
                status = meta.get("status", "learning")
                title = meta.get("title", "—")
                if status == "completed":
                    icon = "✅"
                else:
                    icon = "📖"
            else:
                icon = "⬜"
                title = "（无 META）"
        else:
            icon = "⬜"
            title = "（未开始）"

        print(f"  {icon} W{wn:02d} │ {title}")

    print("═" * 55)

    completed = sum(
        1 for wd in week_dirs
        if (m := load_meta(wd)) and m.get("status") == "completed"
    )
    print(f"\n  完成率：{completed}/{total}（{int(completed/total*100)}%）")

    # 时间维度
    start = datetime.strptime(cfg["start_date"], "%Y-%m-%d").date()
    today = date.today()
    elapsed_weeks = (today - start).days // 7
    print(f"  时间周：第 {elapsed_weeks + 1} 周（共 {total} 周）")

    if completed < elapsed_weeks:
        gap = elapsed_weeks - completed
        print(f"  ⚠️  落后 {gap} 周，需要加速！")
    elif completed >= elapsed_weeks:
        print(f"  🎉 进度正常或超前！")
    print()


# ─── 命令分发 ─────────────────────────────────────────────────────────────────

COMMANDS = {
    "scan": (cmd_scan, "刷新学习索引"),
    "status": (cmd_status, "学习进度概览"),
    "plan": (cmd_plan, "查看某周学习计划"),
    "review": (cmd_review, "回顾某周产出"),
    "distill": (cmd_distill, "从某周提炼知识"),
    "progress": (cmd_progress, "12周整体进度"),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("用法：./aijourney <command> [args]")
        print()
        for name, (_, desc) in COMMANDS.items():
            print(f"  {name:12s} {desc}")
        sys.exit(0)

    cmd_name = sys.argv[1]
    if cmd_name not in COMMANDS:
        print(f"❌ 未知命令：{cmd_name}")
        print(f"   可用命令：{', '.join(COMMANDS.keys())}")
        sys.exit(1)

    func = COMMANDS[cmd_name][0]

    # 带参数的命令
    if cmd_name in ("plan", "review", "distill") and len(sys.argv) > 2:
        try:
            week_num = int(sys.argv[2])
            func(week_num)
        except ValueError:
            print(f"❌ 周数必须是数字，收到：{sys.argv[2]}")
            sys.exit(1)
    else:
        func()


if __name__ == "__main__":
    main()
