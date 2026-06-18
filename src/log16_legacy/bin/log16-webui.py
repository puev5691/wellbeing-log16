#!/usr/bin/env python3
# Local browser UI for consultant-pipeline-v05.2 + log16.
# Dependencies: Python standard library only.

from __future__ import annotations

import argparse
import html
import os
import subprocess
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path("/data/wellbeing/obs/log16")
BIN = ROOT / "bin"

CMD_ASK_IMPORT = BIN / "log16-ask-import-v05-2.sh"
CMD_IMPORT_LATEST = BIN / "log16-import-latest-v05-2.sh"
CMD_STATUS = BIN / "log16-status.sh"
CMD_CASE = BIN / "log16-case-summary.sh"
CMD_LAST_REPORT = BIN / "log16-last-report.sh"

DEFAULT_QUESTION = "Как привлекаемый участник будет находить своё поле деятельности в проекте?"
DEFAULT_PATTERN = "participant_pathway"


def run_cmd(cmd: list[str], timeout: int = 300) -> tuple[int, str]:
    start = time.strftime("%Y-%m-%d %H:%M:%S")
    header = f"$ {' '.join(cmd)}\nstarted: {start}\n\n"
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return p.returncode, header + p.stdout + f"\n[exit_code={p.returncode}]\n"
    except subprocess.TimeoutExpired as e:
        out = e.stdout or ""
        return 124, header + out + "\nERROR: command timeout\n[exit_code=124]\n"
    except FileNotFoundError as e:
        return 127, header + f"ERROR: command not found: {e}\n[exit_code=127]\n"
    except Exception as e:
        return 1, header + f"ERROR: {type(e).__name__}: {e}\n[exit_code=1]\n"


def page(title: str, output: str = "", question: str = DEFAULT_QUESTION, pattern: str = DEFAULT_PATTERN) -> bytes:
    safe_output = html.escape(output)
    safe_question = html.escape(question)
    safe_pattern = html.escape(pattern)
    body = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  body {{
    font-family: system-ui, -apple-system, Segoe UI, sans-serif;
    margin: 0;
    background: #f5f5f5;
    color: #111;
  }}
  header {{
    background: #222;
    color: white;
    padding: 14px 18px;
  }}
  main {{
    padding: 16px;
    max-width: 1200px;
    margin: auto;
  }}
  textarea {{
    width: 100%;
    box-sizing: border-box;
    min-height: 100px;
    font-family: inherit;
    font-size: 15px;
    padding: 10px;
  }}
  input[type=text] {{
    width: 360px;
    max-width: 100%;
    font-size: 15px;
    padding: 8px;
  }}
  .row {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 10px 0;
    align-items: center;
  }}
  button {{
    padding: 9px 12px;
    font-size: 14px;
    cursor: pointer;
  }}
  .card {{
    background: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 14px;
    margin: 12px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }}
  pre {{
    white-space: pre-wrap;
    word-break: break-word;
    background: #111;
    color: #eee;
    padding: 14px;
    border-radius: 10px;
    overflow: auto;
    min-height: 260px;
  }}
  .hint {{
    color: #555;
    font-size: 14px;
  }}
  .ok {{
    color: #0a5;
    font-weight: 600;
  }}
</style>
</head>
<body>
<header>
  <h2>log16 / КОНСУЛЬТАНТ v05.2</h2>
  <div>Локальный web UI: вопрос → run → import → case view. Да, наконец-то не терминальный обряд.</div>
</header>
<main>
  <div class="card">
    <form method="post" action="/ask">
      <label><b>Вопрос</b></label>
      <textarea name="question">{safe_question}</textarea>
      <div class="row">
        <button type="submit">Спросить v05.2 + сохранить в log16</button>
      </div>
    </form>
  </div>

  <div class="card">
    <form method="post" action="/case">
      <div class="row">
        <label><b>Pattern / дело:</b></label>
        <input type="text" name="pattern" value="{safe_pattern}">
        <button type="submit">Показать дело</button>
      </div>
    </form>
    <div class="row">
      <form method="post" action="/status"><button type="submit">Статус log16</button></form>
      <form method="post" action="/latest"><button type="submit">Импортировать последний run</button></form>
      <form method="post" action="/last-report"><button type="submit">Последний отчёт</button></form>
      <form method="get" action="/"><button type="submit">Очистить</button></form>
    </div>
    <div class="hint">
      После вопроса нажимай “Показать дело”: это сводит answer/gap/task/review в один читаемый блок.
    </div>
  </div>

  <div class="card">
    <h3>Вывод</h3>
    <pre>{safe_output}</pre>
  </div>
</main>
</body>
</html>"""
    return body.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "Log16WebUI/0.1"

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def _read_form(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        parsed = urllib.parse.parse_qs(raw)
        return {k: v[0] if v else "" for k, v in parsed.items()}

    def _send(self, content: bytes, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._send(page("log16 Web UI"))
        else:
            self._send(page("Not found", f"Not found: {self.path}"), 404)

    def do_POST(self):
        form = self._read_form()
        question = form.get("question", DEFAULT_QUESTION).strip() or DEFAULT_QUESTION
        pattern = form.get("pattern", DEFAULT_PATTERN).strip() or DEFAULT_PATTERN

        if self.path == "/ask":
            if not CMD_ASK_IMPORT.exists():
                out = f"ERROR: missing command: {CMD_ASK_IMPORT}"
            else:
                _, out = run_cmd([str(CMD_ASK_IMPORT), question], timeout=900)
                if CMD_CASE.exists():
                    _, case_out = run_cmd([str(CMD_CASE), "--pattern", pattern], timeout=300)
                    out = out + "\n\n===== CASE SUMMARY AFTER ASK =====\n" + case_out
            self._send(page("log16 ask", out, question, pattern))
            return

        if self.path == "/case":
            if not CMD_CASE.exists():
                out = f"ERROR: missing command: {CMD_CASE}"
            else:
                _, out = run_cmd([str(CMD_CASE), "--pattern", pattern], timeout=300)
            self._send(page("log16 case", out, question, pattern))
            return

        if self.path == "/status":
            if not CMD_STATUS.exists():
                out = f"ERROR: missing command: {CMD_STATUS}"
            else:
                _, out = run_cmd([str(CMD_STATUS)], timeout=120)
            self._send(page("log16 status", out, question, pattern))
            return

        if self.path == "/latest":
            if not CMD_IMPORT_LATEST.exists():
                out = f"ERROR: missing command: {CMD_IMPORT_LATEST}"
            else:
                _, out = run_cmd([str(CMD_IMPORT_LATEST)], timeout=600)
                if CMD_CASE.exists():
                    _, case_out = run_cmd([str(CMD_CASE), "--pattern", pattern], timeout=300)
                    out = out + "\n\n===== CASE SUMMARY AFTER IMPORT =====\n" + case_out
            self._send(page("log16 latest import", out, question, pattern))
            return

        if self.path == "/last-report":
            if not CMD_LAST_REPORT.exists():
                out = f"ERROR: missing command: {CMD_LAST_REPORT}"
            else:
                _, out = run_cmd([str(CMD_LAST_REPORT)], timeout=120)
            self._send(page("log16 last report", out, question, pattern))
            return

        self._send(page("Not found", f"Not found: {self.path}"), 404)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=int(os.environ.get("LOG16_WEBUI_PORT", "8896")))
    args = ap.parse_args()

    httpd = HTTPServer((args.host, args.port), Handler)
    print(f"log16 Web UI running: http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
