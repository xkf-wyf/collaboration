# -*- coding: utf-8 -*-
"""
协作看板生成器（零第三方依赖，仅标准库）
用法：python dashboard.py   →   生成 dashboard.html
数据源：本目录下的 pipeline-state.yaml、各子目录文件、git log
"""
import html
import os
import re
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dashboard.html")

DIRS = [
    ("00-inbox", "需求原文", "人类审核方输入，任何人不得修改"),
    ("01-spec", "规格与分析", "WorkBuddy 写，CodeBuddy 只读"),
    ("02-design", "技术方案", "WorkBuddy 写，CodeBuddy 只读"),
    ("03-tasks", "任务单与回报", "任务单 WorkBuddy 写；回报区 CodeBuddy 只追加"),
    ("04-accept", "验收清单", "WorkBuddy 定稿，只有人类能宣布通过"),
    ("kb", "CPT 知识库", "云端为准，人类更新，工具只读"),
]


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def parse_state():
    raw = read(os.path.join(ROOT, "pipeline-state.yaml"))
    state = {"stage": "?", "updated_at": "?", "gates": {}, "questions": [],
             "pending": [], "decisions": [], "title": "", "kb_snapshot": ""}
    m = re.search(r"^stage:\s*(\S+)", raw, re.M)
    if m:
        state["stage"] = m.group(1)
    m = re.search(r"^updated_at:\s*(\S+)", raw, re.M)
    if m:
        state["updated_at"] = m.group(1)
    m = re.search(r"^project:\s*(.+)$", raw, re.M)
    if m:
        state["title"] = m.group(1).strip()
    m = re.search(r"kb_snapshot:\s*(\S+)", raw)
    if m:
        state["kb_snapshot"] = m.group(1)
    for m in re.finditer(r"(G\d_\w+):\s*(\S+)", raw):
        state["gates"][m.group(1)] = m.group(2)
    m = re.search(r"title:\s*(.+)$", raw, re.M)
    if m:
        state["title"] = m.group(1).strip()
    # open_questions 与 pending_decisions 的列表项
    for sec, key in (("open_questions:", "questions"), ("pending_decisions:", "pending")):
        m = re.search(re.escape(sec) + r"\n((?:\s+- .+\n?)+)", raw)
        if m:
            items = re.findall(r"-\s+(.+)", m.group(1))
            state[key] = [i.strip().strip("'\"") for i in items]
    # decisions 记录
    for m in re.finditer(r"- date:\s*(\S+)\n\s+by:\s*(.+)\n\s+decision:\s*(.+)\n\s+impact:\s*(.+)", raw):
        state["decisions"].append(m.groups())
    return state


def list_dir(sub):
    d = os.path.join(ROOT, sub)
    if not os.path.isdir(d):
        return []
    out = []
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if os.path.isfile(p) and not name.startswith("."):
            size = os.path.getsize(p)
            out.append((name, size))
    return out


def task_reports():
    """从 03-tasks 提取执行回报块的状态摘要"""
    reports = []
    for name, _ in list_dir("03-tasks"):
        if not name.endswith(".md") or name == "TEMPLATE.md":
            continue
        text = read(os.path.join(ROOT, "03-tasks", name))
        for block in re.findall(r"###?\s*执行回报(.*?)(?=\n###?|\Z)", text, re.S):
            tid = re.search(r"任务[：:]\s*(\S+)", block)
            st = re.search(r"状态[：:]\s*(\S+)", block)
            br = re.search(r"分支[：:]\s*(\S+)", block)
            reports.append({
                "file": name,
                "task": tid.group(1) if tid else "?",
                "status": st.group(1) if st else "?",
                "branch": br.group(1) if br else "-",
            })
    return reports


def git_log(n=10):
    try:
        r = subprocess.run(
            ["git", "-C", ROOT, "log", "--pretty=format:%h|%ad|%s",
             "--date=format:%m-%d %H:%M", f"-{n}"],
            capture_output=True, text=True, timeout=15, encoding="utf-8")
        out = []
        for line in r.stdout.splitlines():
            parts = line.split("|", 2)
            if len(parts) == 3:
                out.append(parts)
        return out
    except Exception:
        return []


GATE_LABEL = {
    "G1_analysis_review": "G1 规格审核",
    "G2_build_permit": "G2 开发放行",
    "G3_acceptance": "G3 验收",
}
GATE_COLOR = {"passed": "green", "pending": "amber", "blocked": "red"}
STATUS_COLOR = {"done": "green", "partial": "amber", "blocked": "red"}


def badge(text, color):
    bg = {"green": "#EAF3DE", "amber": "#FAEEDA", "red": "#FCEBEB",
          "gray": "#F1EFE8", "blue": "#E6F1FB"}[color]
    fg = {"green": "#3B6D11", "amber": "#854F0B", "red": "#A32D2D",
          "gray": "#5F5E5A", "blue": "#185FA5"}[color]
    return (f'<span style="background:{bg};color:{fg};padding:2px 10px;'
            f'border-radius:10px;font-size:12px">{html.escape(text)}</span>')


def main():
    st = parse_state()
    reports = task_reports()
    commits = git_log()

    gates_html = ""
    for gid, label in GATE_LABEL.items():
        val = st["gates"].get(gid, "pending")
        gates_html += (
            f'<div style="flex:1;background:#fff;border:0.5px solid #d3d1c7;'
            f'border-radius:8px;padding:10px 14px;display:flex;'
            f'justify-content:space-between;align-items:center">'
            f'<span style="font-size:13px">{label}</span>'
            f'{badge(val, GATE_COLOR.get(val, "gray"))}</div>')

    q_html = "".join(
        f'<li style="margin:4px 0">{html.escape(q)}</li>' for q in st["questions"]) or "<li>无</li>"
    p_html = "".join(
        f'<li style="margin:4px 0">{html.escape(p)}</li>' for p in st["pending"]) or "<li>无</li>"

    dec_rows = "".join(
        f'<tr><td style="padding:6px 8px;white-space:nowrap">{d[0]}</td>'
        f'<td style="padding:6px 8px;white-space:nowrap">{html.escape(d[1].strip())}</td>'
        f'<td style="padding:6px 8px">{html.escape(d[2].strip())}</td></tr>'
        for d in st["decisions"])
    dec_html = (f'<table style="border-collapse:collapse;width:100%;font-size:12px">'
                f'<tr><th style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #d3d1c7">日期</th>'
                f'<th style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #d3d1c7">裁决人</th>'
                f'<th style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #d3d1c7">决定</th></tr>'
                f'{dec_rows}</table>') if dec_rows else "<p style='color:#888780'>暂无</p>"

    rep_html = ""
    if reports:
        rows = "".join(
            f'<tr><td style="padding:6px 8px">{r["task"]}</td>'
            f'<td style="padding:6px 8px">{badge(r["status"], STATUS_COLOR.get(r["status"], "gray"))}</td>'
            f'<td style="padding:6px 8px;font-family:monospace">{html.escape(r["branch"])}</td>'
            f'<td style="padding:6px 8px;color:#888780">{html.escape(r["file"])}</td></tr>'
            for r in reports)
        rep_html = (f'<h3 style="font-size:14px;margin:18px 0 8px">CodeBuddy 执行回报</h3>'
                    f'<table style="border-collapse:collapse;width:100%;font-size:12px">'
                    f'<tr><th style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #d3d1c7">任务</th>'
                    f'<th style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #d3d1c7">状态</th>'
                    f'<th style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #d3d1c7">分支</th>'
                    f'<th style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #d3d1c7">回报文件</th></tr>'
                    f'{rows}</table>')
    else:
        rep_html = (f'<h3 style="font-size:14px;margin:18px 0 8px">CodeBuddy 执行回报</h3>'
                    f'<p style="color:#888780;font-size:13px">暂无回报——CodeBuddy 尚未执行首单（当前仅完成契约握手）。'
                    f'回报将出现在 03-tasks/ 各任务单末尾。</p>')

    cols_html = ""
    for sub, label, note in DIRS:
        items = list_dir(sub)
        lis = "".join(
            f'<li style="margin:3px 0;font-size:12px;word-break:break-all">{html.escape(n)}'
            f'<span style="color:#b4b2a9"> ({s}B)</span></li>'
            for n, s in items) or '<li style="color:#b4b2a9;font-size:12px">（空）</li>'
        cols_html += (
            f'<div style="flex:1;min-width:180px;background:#fff;border:0.5px solid #d3d1c7;'
            f'border-radius:8px;padding:12px">'
            f'<div style="font-size:13px;font-weight:500">{label}'
            f'<span style="color:#b4b2a9;font-weight:400;font-size:11px"> {sub}/</span></div>'
            f'<div style="color:#888780;font-size:11px;margin:2px 0 8px">{note}</div>'
            f'<ul style="padding-left:16px;margin:0">{lis}</ul></div>')

    commit_html = "".join(
        f'<li style="margin:4px 0;font-size:12px;font-family:monospace">'
        f'<span style="color:#185FA5">{c[0]}</span> '
        f'<span style="color:#888780">{c[1]}</span> {html.escape(c[2])}</li>'
        for c in commits) or "<li>git 不可用</li>"

    page = f"""<!DOCTYPE html>
<html lang="zh">
<head><meta charset="utf-8"><title>协作看板 · {html.escape(st['title'])}</title></head>
<body style="margin:0;background:#F1EFE8;font-family:'Segoe UI','Microsoft YaHei',sans-serif;color:#2C2C2A">
<div style="max-width:1080px;margin:0 auto;padding:24px 20px">
  <h1 style="font-size:18px;margin:0 0 4px">协作看板 · {html.escape(st['title'])}</h1>
  <p style="margin:0 0 16px;color:#888780;font-size:12px">
    生成时间 {datetime.now().strftime('%Y-%m-%d %H:%M')} ·
    状态阶段 <b>{html.escape(st['stage'])}</b> ·
    状态更新于 {html.escape(st['updated_at'])} ·
    kb 快照 {html.escape(st['kb_snapshot'] or '未标注')} ·
    再生成：<code>python dashboard.py</code></p>

  <div style="display:flex;gap:10px;margin-bottom:16px">{gates_html}</div>

  <div style="display:flex;gap:10px;margin-bottom:16px">
    <div style="flex:1;background:#fff;border:0.5px solid #d3d1c7;border-radius:8px;padding:12px 16px">
      <h3 style="font-size:14px;margin:0 0 8px;color:#A32D2D">待你裁决（阻塞项）</h3>
      <ul style="padding-left:16px;margin:0;font-size:13px">{p_html}</ul>
    </div>
    <div style="flex:1;background:#fff;border:0.5px solid #d3d1c7;border-radius:8px;padding:12px 16px">
      <h3 style="font-size:14px;margin:0 0 8px;color:#185FA5">开放问题</h3>
      <ul style="padding-left:16px;margin:0;font-size:13px">{q_html}</ul>
    </div>
  </div>

  {rep_html}

  <h3 style="font-size:14px;margin:18px 0 8px">人类裁决记录</h3>
  {dec_html}

  <h3 style="font-size:14px;margin:18px 0 8px">目录一览（文件总线）</h3>
  <div style="display:flex;gap:10px;flex-wrap:wrap">{cols_html}</div>

  <h3 style="font-size:14px;margin:18px 0 8px">Git 提交（github.com/xkf-wyf/collaboration）</h3>
  <ul style="padding-left:16px;margin:0">{commit_html}</ul>

  <p style="margin:20px 0 0;color:#b4b2a9;font-size:11px">
    本页面由 dashboard.py 从目录状态自动生成，只读展示；三方写入仍走文件总线与 Git。</p>
</div>
</body></html>"""

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"已生成 {OUT}")


if __name__ == "__main__":
    sys.exit(main())
