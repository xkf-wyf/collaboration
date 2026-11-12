# -*- coding: utf-8 -*-
"""
协作平台本地服务（零第三方依赖，仅 Python 标准库）
用法：python platform/server.py   →   浏览器打开 http://localhost:8765
数据源：协作根目录（本脚本上级目录），平台只做展示与写入，文件总线仍是唯一真相。
"""
import json
import os
import re
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORM_DIR = os.path.join(ROOT, "platform")
PORT = 8765
DIRS = ["00-inbox", "01-spec", "02-design", "03-tasks", "04-accept", "kb"]
GATE_LABEL = {
    "G1_analysis_review": "G1 规格审核",
    "G2_build_permit": "G2 开发放行",
    "G3_acceptance": "G3 验收",
}


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def git(*args, timeout=30):
    try:
        r = subprocess.run(
            ["git", "-C", ROOT,
             "-c", "user.name=xkf-wyf", "-c", "user.email=xkf0114@163.com", *args],
            capture_output=True, text=True, timeout=timeout, encoding="utf-8")
        return r.returncode == 0
    except Exception:
        return False


def git_commit_push(msg):
    git("add", "-A")
    ok = git("commit", "-m", msg)
    git("push", timeout=60)
    return ok


def parse_state():
    raw = read_text(os.path.join(ROOT, "pipeline-state.yaml"))
    st = {"stage": "inbox", "updated_at": "", "title": "协作平台",
          "kb_snapshot": "", "gates": {}, "pending": [], "questions": [], "decisions": []}
    m = re.search(r"^project:\s*(.+)$", raw, re.M)
    if m:
        st["title"] = m.group(1).strip()
    m = re.search(r"^stage:\s*(\S+)", raw, re.M)
    if m:
        st["stage"] = m.group(1)
    m = re.search(r"^updated_at:\s*(\S+)", raw, re.M)
    if m:
        st["updated_at"] = m.group(1)
    m = re.search(r"kb_snapshot:\s*(\S+)", raw)
    if m:
        st["kb_snapshot"] = m.group(1)
    for m in re.finditer(r"(G\d_\w+):\s*(\S+)", raw):
        st["gates"][m.group(1)] = m.group(2)
    for sec, key in (("open_questions:", "questions"), ("pending_decisions:", "pending")):
        m = re.search(re.escape(sec) + r"\n((?:\s+- .+\n?)+)", raw)
        if m:
            st[key] = [i.strip().strip("'\"") for i in re.findall(r"-\s+(.+)", m.group(1))]
    for m in re.finditer(
            r"- date:\s*(\S+)\n\s+by:\s*(.+)\n\s+decision:\s*(.+)\n\s+impact:\s*(.+)", raw):
        st["decisions"].append(
            {"date": m.group(1), "by": m.group(2).strip(),
             "decision": m.group(3).strip(), "impact": m.group(4).strip()})
    return st


def parse_tasks():
    tasks = []
    tdir = os.path.join(ROOT, "03-tasks")
    if not os.path.isdir(tdir):
        return tasks
    for name in sorted(os.listdir(tdir)):
        if not name.endswith(".md") or name == "TEMPLATE.md":
            continue
        text = read_text(os.path.join(tdir, name))
        parts = re.split(r"(?m)^##\s+(T-\d+[^\n]*)$", text)
        for i in range(1, len(parts) - 1, 2):
            header, body = parts[i].strip(), parts[i + 1]
            tid = header.split()[0]
            title = header[len(tid):].strip() or "(未命名)"
            reports = []
            for rb in re.split(r"(?m)^###?\s*执行回报\s*$", body)[1:]:
                st = re.search(r"状态[：:]\s*(\S+)", rb)
                br = re.search(r"分支[：:]\s*(\S+)", rb)
                reports.append({
                    "status": st.group(1) if st else "?",
                    "branch": br.group(1).strip() if br else "",
                    "excerpt": rb.strip()[:260],
                })
            tasks.append({
                "id": tid, "title": title, "file": name,
                "status": reports[-1]["status"] if reports else "待认领",
                "reports": reports,
            })
    return tasks


def list_dir_files():
    out = {}
    for d in DIRS:
        p = os.path.join(ROOT, d)
        out[d] = sorted(os.listdir(p)) if os.path.isdir(p) else []
    return out


def recent_commits(n=8):
    try:
        r = subprocess.run(
            ["git", "-C", ROOT, "log", "--pretty=format:%h|%ad|%s",
             "--date=format:%m-%d %H:%M", f"-{n}"],
            capture_output=True, text=True, timeout=15, encoding="utf-8")
        return [{"hash": a, "date": b, "msg": c}
                for a, b, c in (l.split("|", 2) for l in r.stdout.splitlines())]
    except Exception:
        return []


def load_decisions_log():
    p = os.path.join(ROOT, "05-platform", "decisions.json")
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_decisions_log(items):
    os.makedirs(os.path.join(ROOT, "05-platform"), exist_ok=True)
    p = os.path.join(ROOT, "05-platform", "decisions.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def next_inbox_id():
    d = os.path.join(ROOT, "00-inbox")
    mx = 0
    if os.path.isdir(d):
        for n in os.listdir(d):
            m = re.match(r"(\d+)", n)
            if m:
                mx = max(mx, int(m.group(1)))
    return mx + 1


def safe_path(rel):
    real = os.path.realpath(os.path.join(ROOT, rel))
    if not real.startswith(os.path.realpath(ROOT) + os.sep):
        return None
    return real


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            html_text = read_text(os.path.join(PLATFORM_DIR, "index.html"))
            self._send(200, html_text, "text/html; charset=utf-8")
        elif u.path == "/api/state":
            st = parse_state()
            payload = {
                "stage": st["stage"], "title": st["title"],
                "updated_at": st["updated_at"], "kb_snapshot": st["kb_snapshot"],
                "gates": [{"id": k, "label": GATE_LABEL.get(k, k), "value": v}
                          for k, v in st["gates"].items()],
                "pending": st["pending"], "questions": st["questions"],
                "decisions": st["decisions"],
                "decision_log": load_decisions_log(),
                "tasks": parse_tasks(),
                "dirs": list_dir_files(),
                "commits": recent_commits(),
                "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self._send(200, json.dumps(payload, ensure_ascii=False))
        elif u.path == "/api/file":
            rel = parse_qs(u.query).get("path", [""])[0]
            real = safe_path(rel)
            if not real or not os.path.isfile(real):
                self._send(404, json.dumps({"error": "not found"}, ensure_ascii=False))
                return
            self._send(200, json.dumps({"path": rel, "content": read_text(real)},
                                       ensure_ascii=False))
        else:
            self._send(404, "{}")

    def do_POST(self):
        u = urlparse(self.path)
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        except Exception:
            self._send(400, json.dumps({"error": "bad body"}, ensure_ascii=False))
            return

        if u.path == "/api/requirement":
            text = (body.get("text") or "").strip()
            if not text:
                self._send(400, json.dumps({"error": "需求内容为空"}, ensure_ascii=False))
                return
            num = next_inbox_id()
            ts = datetime.now().strftime("%Y%m%d-%H%M")
            fname = f"{num:03d}-原始需求-{ts}.md"
            content = (f"# 原始需求 {num:03d}\n\n- 提交时间：{datetime.now().isoformat(timespec='seconds')}\n"
                       f"- 提交渠道：协作平台\n\n> 以下为人类审核方原话，原文照存不改\n\n{text}\n")
            with open(os.path.join(ROOT, "00-inbox", fname), "w", encoding="utf-8") as f:
                f.write(content)
            git_commit_push(f"docs(inbox): 收录原始需求 {num:03d}（平台提交）")
            self._send(200, json.dumps({"ok": True, "file": f"00-inbox/{fname}"},
                                       ensure_ascii=False))

        elif u.path == "/api/decision":
            item = {"ts": datetime.now().isoformat(timespec="seconds"),
                    "target": (body.get("target") or "").strip(),
                    "choice": (body.get("choice") or "").strip(),
                    "note": (body.get("note") or "").strip()}
            if not item["target"] or not item["choice"]:
                self._send(400, json.dumps({"error": "缺少 target/choice"}, ensure_ascii=False))
                return
            log = load_decisions_log()
            log.append(item)
            save_decisions_log(log)
            git_commit_push(f"docs(decision): 人类裁决 {item['target']} → {item['choice']}（平台记录）")
            self._send(200, json.dumps({"ok": True}, ensure_ascii=False))

        else:
            self._send(404, "{}")


def main():
    addr = ("127.0.0.1", PORT)
    server = HTTPServer(addr, Handler)
    print(f"platform serving http://localhost:{PORT}  root={ROOT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
