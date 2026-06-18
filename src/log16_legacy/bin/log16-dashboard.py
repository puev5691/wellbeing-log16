#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import sys
sys.path.insert(0, "/data/wellbeing/repos/wellbeing-log16/src")

from log16.review.decisions import apply_review_decision
from log16.storage.layout import RuntimeLayout

HOST = "127.0.0.1"
PORT = 8898

ROOT = Path("/data/wellbeing/obs/log16")
OUTBOX = Path("/data/wellbeing/obs/consultant/outbox")
BIN = ROOT / "bin"
PULT = BIN / "log16-pult"
DASH_RUNS = ROOT / "dashboard-runs"

NEEDS_REVIEW = ROOT / "entity-responses" / "needs_review"
APPROVED = ROOT / "entity-responses" / "approved"
REJECTED = ROOT / "entity-responses" / "rejected"
REVISION = ROOT / "entity-responses" / "revision_requested"
REVIEWS = ROOT / "reviews"
REVIEWED_DOCS = ROOT / "reviewed-docs"

ALLOWED_ROOTS = [ROOT.resolve(), OUTBOX.resolve()]

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def stamp():
    return time.strftime("%Y%m%d-%H%M%S")

def esc(s: Any) -> str:
    return html.escape(str(s), quote=True)

def run_cmd(cmd: list[str], timeout: int = 1800) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = "$ " + " ".join(cmd) + "\n\n"
        out += "STDOUT:\n" + p.stdout + "\n\nSTDERR:\n" + p.stderr
        return p.returncode, out
    except Exception as e:
        return 999, f"ERROR: {type(e).__name__}: {e}"

def is_allowed_path(path: Path) -> bool:
    try:
        rp = path.resolve()
    except Exception:
        return False
    for root in ALLOWED_ROOTS:
        try:
            rp.relative_to(root)
            return True
        except ValueError:
            pass
    return False

def read_text_file(path: Path) -> str:
    if not is_allowed_path(path):
        return "DENIED: path outside allowed roots"
    if not path.exists():
        return "NOT FOUND"
    if path.is_dir():
        return "IS DIRECTORY"
    return path.read_text(encoding="utf-8", errors="replace")

def load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def save_json(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def count_json(path: Path) -> int:
    return len(list(path.glob("*.json"))) if path.exists() else 0

def status_counts() -> dict[str, int]:
    return {
        "themes": count_json(ROOT / "themes" / "captured"),
        "tasks_proposed": count_json(ROOT / "derived-tasks" / "proposed"),
        "tasks_routed": count_json(ROOT / "derived-tasks" / "routed"),
        "tasks_dispatched": count_json(ROOT / "derived-tasks" / "dispatched"),
        "tasks_done": count_json(ROOT / "derived-tasks" / "done"),
        "requests_pending": count_json(ROOT / "entity-requests" / "pending"),
        "requests_done": count_json(ROOT / "entity-requests" / "done"),
        "responses_review": count_json(NEEDS_REVIEW),
        "responses_approved": count_json(APPROVED),
        "responses_revision": count_json(REVISION),
        "responses_rejected": count_json(REJECTED),
        "responses_failed": count_json(ROOT / "entity-responses" / "failed"),
        "runner_reports": len([p for p in (ROOT / "runner-reports").iterdir() if p.is_dir()]) if (ROOT / "runner-reports").exists() else 0,
        "pult_runs": len([p for p in (ROOT / "pult-runs").iterdir() if p.is_dir()]) if (ROOT / "pult-runs").exists() else 0,
    }

def recent_files(patterns: list[str], limit: int = 10) -> list[Path]:
    out = []
    for pat in patterns:
        out.extend(Path("/").glob(pat.lstrip("/")))
    out = [p for p in out if p.exists() and p.is_file()]
    out.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return out[:limit]

def path_link(path: Path, label: str | None = None) -> str:
    qp = urllib.parse.urlencode({"path": str(path)})
    return f'<a href="/view?{qp}">{esc(label or path.name)}</a>'

def review_link(path: Path, label: str = "Открыть review") -> str:
    qp = urllib.parse.urlencode({"path": str(path)})
    return f'<a class="button" href="/review-item?{qp}">{esc(label)}</a>'

def latest_answer() -> Path | None:
    files = recent_files([str(ROOT / "pult-runs" / "answer-*" / "direct-answer.md")], 1)
    return files[0] if files else None

def latest_reports(limit=6) -> list[Path]:
    return recent_files([
        str(ROOT / "pult-runs" / "*" / "*.md"),
        str(ROOT / "runner-reports" / "*" / "runner-summary.md"),
        str(ROOT / "dashboard-runs" / "*" / "*.md"),
        str(ROOT / "reviews" / "*.md"),
    ], limit)

def page(title: str, body: str) -> bytes:
    css = """
    :root { --bg:#f6f7f9; --card:#fff; --line:#d7dbe2; --text:#17202a; --muted:#65717f; --accent:#2457c5; --bad:#9b1c1c; --ok:#116b35; --warn:#9a6700; }
    body { font-family: system-ui, -apple-system, sans-serif; margin: 0; background: var(--bg); color: var(--text); line-height: 1.45; }
    header { background: #111827; color: white; padding: 16px 24px; }
    header h1 { margin: 0; font-size: 1.35rem; }
    nav { padding: 10px 24px; background: white; border-bottom: 1px solid var(--line); display:flex; gap: 12px; flex-wrap:wrap; }
    nav a { color: var(--accent); text-decoration:none; font-weight:600; }
    main { max-width: 1200px; margin: 22px auto; padding: 0 18px; }
    .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; }
    .card { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 16px; box-shadow: 0 1px 2px rgba(0,0,0,.04); }
    .card h2, .card h3 { margin-top: 0; }
    .big { font-size: 2rem; font-weight: 800; }
    .muted { color: var(--muted); }
    .ok { color: var(--ok); font-weight:700; }
    .bad { color: var(--bad); font-weight:700; }
    .warn { color: var(--warn); font-weight:700; }
    textarea { width: 100%; min-height: 120px; border-radius: 10px; border:1px solid var(--line); padding:12px; font-family: inherit; box-sizing: border-box; }
    button, input[type=submit], .button { padding: 10px 16px; border-radius: 10px; border: 1px solid #9aa4b2; background:white; cursor:pointer; font-weight:700; text-decoration:none; display:inline-block; color:var(--text); }
    button.primary, input.primary, .primary { background: var(--accent); color:white; border-color: var(--accent); }
    .approve { background:#116b35; color:white; border-color:#116b35; }
    .revise { background:#9a6700; color:white; border-color:#9a6700; }
    .reject { background:#9b1c1c; color:white; border-color:#9b1c1c; }
    pre { white-space: pre-wrap; background: #111827; color: #f4f4f5; padding: 14px; border-radius: 12px; overflow-x: auto; }
    .doc { background:white; color:var(--text); border:1px solid var(--line); }
    details { background:white; border: 1px solid var(--line); border-radius: 12px; padding: 12px; margin: 12px 0; }
    summary { cursor:pointer; font-weight:700; }
    ul.clean { padding-left: 20px; }
    .pill { display:inline-block; padding: 4px 8px; border-radius:999px; background:#eef2ff; color:#263b80; font-size:.9rem; }
    .actions { display:flex; gap:10px; flex-wrap:wrap; margin-top:12px; }
    """
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{esc(title)}</title>
<style>{css}</style>
</head>
<body>
<header><h1>log16 dashboard</h1><div class="muted">Операторская панель: ответить, поставить задачу, проверить, принять решение.</div></header>
<nav>
  <a href="/">Главная</a>
  <a href="/review">Review</a>
  <a href="/decisions">Decisions</a>
  <a href="/reports">Результаты</a>
  <a href="/status">Техстатус</a>
  <a href="/action?cmd=cleanup">Cleanup</a>
  <a href="/action?cmd=run-pending">Run pending</a>
</nav>
<main>{body}</main>
</body>
</html>""".encode("utf-8")

def render_top_status() -> str:
    c = status_counts()
    attention = []
    if c["requests_pending"]:
        attention.append(f'<div class="card"><h3>Нужно запустить</h3><div class="big bad">{c["requests_pending"]}</div><p>pending requests ждут runner.</p><p><a class="button primary" href="/action?cmd=run-pending">Запустить pending</a></p></div>')
    if c["responses_review"]:
        attention.append(f'<div class="card"><h3>Ждут review</h3><div class="big warn">{c["responses_review"]}</div><p>Ответы Сущностей требуют решения.</p><p><a class="button primary" href="/review">Перейти к review</a></p></div>')
    if c["tasks_routed"]:
        attention.append(f'<div class="card"><h3>Нужно cleanup</h3><div class="big bad">{c["tasks_routed"]}</div><p>routed tasks могут быть stale.</p><p><a class="button" href="/action?cmd=cleanup">Убрать хвосты</a></p></div>')
    if not attention:
        attention.append('<div class="card"><h3>Очередь спокойна</h3><div class="big ok">OK</div><p>Нет pending requests и routed-хвостов.</p></div>')

    return f"""
<section class="grid">
  {''.join(attention)}
  <div class="card"><h3>Approved</h3><div class="big ok">{c["responses_approved"]}</div><p class="muted">принятые ответы</p></div>
  <div class="card"><h3>Revision</h3><div class="big warn">{c["responses_revision"]}</div><p class="muted">отправлено на доработку</p></div>
  <div class="card"><h3>Rejected</h3><div class="big bad">{c["responses_rejected"]}</div><p class="muted">забраковано</p></div>
</section>
"""

def render_forms() -> str:
    return """
<section class="grid" style="margin-top:16px;">
  <div class="card">
    <h2>Спросить Систему</h2>
    <form method="post" action="/answer">
      <textarea name="text" placeholder="Например: Какое количество Сущностей задействовано в проекте на данном этапе?"></textarea>
      <br><br><input class="primary" type="submit" value="Получить ответ">
    </form>
  </div>
  <div class="card">
    <h2>Поставить тему в работу</h2>
    <form method="post" action="/tasks">
      <textarea name="text" placeholder="Например: Нужно разработать систему учёта полезных результатов участников"></textarea>
      <br><br><input class="primary" type="submit" value="Породить задачи">
    </form>
  </div>
</section>
"""

def render_latest_answer() -> str:
    files = recent_files([str(ROOT / "pult-runs" / "answer-*" / "direct-answer.md")], 1)
    if not files:
        return '<div class="card"><h2>Последний ответ</h2><p class="muted">Пока нет direct-answer.md.</p></div>'
    p = files[0]
    txt = read_text_file(p)
    snippet = txt[:1400] + ("..." if len(txt) > 1400 else "")
    return f'<div class="card"><h2>Последний ответ</h2><p>{path_link(p, "Открыть полностью")}</p><pre class="doc">{esc(snippet)}</pre></div>'

def render_reports(limit=8) -> str:
    files = latest_reports(limit)
    if not files:
        return '<div class="card"><h2>Последние результаты</h2><p class="muted">Пока пусто.</p></div>'
    items = []
    for p in files:
        label = p.name.replace(".md", "")
        items.append(f'<li>{path_link(p, label)}<br><span class="muted">{esc(str(p))}</span></li>')
    return '<div class="card"><h2>Последние результаты</h2><ul class="clean">' + "\n".join(items) + "</ul></div>"

def render_home() -> str:
    return render_top_status() + render_forms() + '<section style="margin-top:16px;">' + render_latest_answer() + render_reports(8) + "</section>"

def response_card_html(p: Path) -> str:
    data = load_json(p) or {}
    entity = data.get("target_display_name") or data.get("target_entity") or "?"
    case = data.get("source_case", "?")
    expected = data.get("expected_output", "?")
    text = (data.get("response_text") or "").strip()
    snippet = text[:700] + ("..." if len(text) > 700 else "")
    return f"""
<div class="card">
  <h3>{esc(entity)}</h3>
  <p><span class="pill">{esc(case)}</span></p>
  <p><b>Ожидаемый результат:</b> {esc(expected)}</p>
  <div class="actions">{review_link(p, "Проверить / принять решение")}</div>
  <pre class="doc">{esc(snippet)}</pre>
</div>
"""

def render_review() -> str:
    files = sorted(NEEDS_REVIEW.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return "<h2>Review</h2><p>Нет ответов, требующих review.</p>"
    cards = [response_card_html(p) for p in files[:50]]
    return "<h2>Ответы, требующие review</h2><p>Открой карточку, отредактируй или зафиксируй решение.</p><div class='grid'>" + "\n".join(cards) + "</div>"

def render_review_item(path: Path) -> str:
    if not is_allowed_path(path) or path.parent != NEEDS_REVIEW:
        return "<h2>Недопустимая карточка review</h2>"
    data = load_json(path)
    if not data:
        return "<h2>Не удалось прочитать JSON</h2>"
    entity = data.get("target_display_name") or data.get("target_entity") or "?"
    response_id = data.get("response_id") or path.stem
    text = data.get("response_text") or ""
    expected = data.get("expected_output") or ""
    case = data.get("source_case") or ""
    return f"""
<h2>Review: {esc(entity)}</h2>
<div class="card">
  <p><b>Response:</b> {esc(response_id)}</p>
  <p><b>Source case:</b> <span class="pill">{esc(case)}</span></p>
  <p><b>Expected output:</b> {esc(expected)}</p>
  <p class="muted">{esc(str(path))}</p>
</div>

<form method="post" action="/review-submit">
  <input type="hidden" name="path" value="{esc(str(path))}">
  <h3>Текст / правка ОПЕРАТОРА</h3>
  <p class="muted">Можно оставить как есть, дописать правку или написать причину доработки/отклонения.</p>
  <textarea name="operator_text" style="min-height:420px;">{esc(text)}</textarea>
  <h3>Комментарий</h3>
  <textarea name="operator_note" style="min-height:110px;" placeholder="Коротко: почему принять, что исправить, что не так."></textarea>
  <div class="actions">
    <button class="approve" name="decision" value="approve_as_is">Принять как есть</button>
    <button class="approve" name="decision" value="approve_with_edit">Принять с правкой</button>
    <button class="revise" name="decision" value="request_revision">На доработку</button>
    <button class="reject" name="decision" value="reject">Забраковать</button>
  </div>
</form>
"""

def review_decision(path: Path, decision: str, operator_text: str, operator_note: str) -> tuple[str, Path | None]:
    try:
        result = apply_review_decision(
            path,
            RuntimeLayout(ROOT),
            decision=decision,
            operator_text=operator_text,
            operator_note=operator_note,
            reviewer="OPERATOR/log16-dashboard",
        )
        return f"PASS review decision fixed: {result.decision}", result.review_md_path
    except Exception as e:
        return f"ERROR review decision failed: {type(e).__name__}: {e}", None
def render_decisions() -> str:
    files = sorted(REVIEWS.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return "<h2>Decisions</h2><p>Пока нет review decisions.</p>"
    items = [f"<li>{path_link(p, p.name)}</li>" for p in files[:50]]
    return "<h2>Зафиксированные решения review</h2><ul class='clean'>" + "\n".join(items) + "</ul>"

def render_technical_status() -> str:
    rc, out = run_cmd([str(PULT), "status", "--cleanup"], timeout=300)
    return render_top_status() + f"<details open><summary>Технический вывод pult status --cleanup</summary><pre>{esc(out)}</pre></details>"

def extract_special_lines(output: str) -> str:
    lines = []
    for ln in output.splitlines():
        if ln.startswith(("PASS", "WARN", "NO_PENDING", "SUMMARY:", "ARCHIVE:", "ANSWER:", "MOVED:", "REQUESTS_", "RESPONSES_", "FAILED:")):
            if ln.startswith(("SUMMARY:", "ARCHIVE:", "ANSWER:")):
                path = ln.split(":", 1)[1].strip()
                if path:
                    lines.append(f"<p><b>{esc(ln.split(':',1)[0])}:</b> {path_link(Path(path), path)}</p>")
            else:
                lines.append(f"<p><b>{esc(ln)}</b></p>")
    return "\n".join(lines)

class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, content: bytes, ctype="text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/":
            self._send(200, page("log16 dashboard", render_home()))
            return
        if parsed.path == "/review":
            self._send(200, page("review", render_review()))
            return
        if parsed.path == "/review-item":
            raw_path = q.get("path", [""])[0]
            self._send(200, page("review item", render_review_item(Path(raw_path))))
            return
        if parsed.path == "/decisions":
            self._send(200, page("decisions", render_decisions()))
            return
        if parsed.path == "/reports":
            self._send(200, page("reports", render_reports(40)))
            return
        if parsed.path == "/status":
            self._send(200, page("status", render_technical_status()))
            return
        if parsed.path == "/action":
            cmd = q.get("cmd", [""])[0]
            if cmd == "cleanup":
                command = [str(PULT), "cleanup"]
            elif cmd == "run-pending":
                command = [str(PULT), "run-pending"]
            else:
                self._send(400, page("bad action", f"<h2>Bad action</h2><pre>{esc(cmd)}</pre>"))
                return
            rc, out = run_cmd(command)
            body = render_top_status() + extract_special_lines(out)
            body += f"<details><summary>Технический вывод</summary><pre>{esc(out)}</pre></details>"
            self._send(200, page(cmd, body))
            return
        if parsed.path == "/view":
            raw_path = q.get("path", [""])[0]
            p = Path(raw_path)
            txt = read_text_file(p)
            body = f"<h2>{esc(p.name)}</h2><p class='muted'>{esc(str(p))}</p><pre class='doc'>{esc(txt)}</pre>"
            self._send(200, page("view", body))
            return
        self._send(404, page("not found", "<h2>Not found</h2>"))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        form_raw = self.rfile.read(length).decode("utf-8", errors="replace")
        form = urllib.parse.parse_qs(form_raw)

        if parsed.path == "/review-submit":
            raw_path = form.get("path", [""])[0]
            decision = form.get("decision", [""])[0]
            operator_text = form.get("operator_text", [""])[0]
            operator_note = form.get("operator_note", [""])[0]
            msg, review_md = review_decision(Path(raw_path), decision, operator_text, operator_note)
            body = render_top_status()
            body += f"<div class='card'><h2>Review decision</h2><p>{esc(msg)}</p>"
            if review_md:
                body += f"<p>{path_link(review_md, 'Открыть decision record')}</p>"
            body += "</div>"
            body += "<p><a class='button primary' href='/review'>Вернуться к review</a></p>"
            self._send(200, page("review decision", body))
            return

        text = form.get("text", [""])[0].strip()
        if not text:
            self._send(400, page("empty", "<h2>Пустой ввод</h2>"))
            return

        if parsed.path == "/answer":
            cmd = [str(PULT), "ask", text]
            title = "Ответ"
        elif parsed.path == "/tasks":
            cmd = [str(PULT), "tasks", text]
            title = "Задачи"
        else:
            self._send(404, page("not found", "<h2>Not found</h2>"))
            return

        rc, out = run_cmd(cmd)
        run_dir = ROOT / "dashboard-runs" / f"{parsed.path.strip('/')}-{stamp()}"
        run_dir.mkdir(parents=True, exist_ok=True)
        log = run_dir / "dashboard-action.log"
        log.write_text(out, encoding="utf-8")

        body = render_top_status()
        body += f"<div class='card'><h2>{esc(title)}</h2><p><b>Запрос:</b></p><pre class='doc'>{esc(text)}</pre></div>"
        body += extract_special_lines(out)
        answer_path = None
        for ln in out.splitlines():
            if ln.startswith("ANSWER:"):
                answer_path = Path(ln.split(":",1)[1].strip())
        if answer_path:
            body += f"<div class='card'><h2>Полученный ответ</h2><p>{path_link(answer_path, 'Открыть файл ответа')}</p><pre class='doc'>{esc(read_text_file(answer_path))}</pre></div>"
        body += f"<details><summary>Технический вывод</summary><pre>{esc(out)}</pre></details>"
        self._send(200, page(title, body))

def main():
    for d in [DASH_RUNS, APPROVED, REJECTED, REVISION, REVIEWS, REVIEWED_DOCS]:
        d.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"log16 dashboard v03 listening on http://{HOST}:{PORT}/")
    print("Ctrl+C to stop.")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
