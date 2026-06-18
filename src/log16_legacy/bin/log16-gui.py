#!/usr/bin/env python3
# Simple GUI for consultant-pipeline-v05.2 + log16.
# Uses only Python stdlib tkinter.

from __future__ import annotations

import os
import queue
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path("/data/wellbeing/obs/log16")
BIN = ROOT / "bin"
APP = Path("/data/wellbeing/obs/consultant/bin/consultant-pipeline-v05.2")

CMD_ASK_IMPORT = BIN / "log16-ask-import-v05-2.sh"
CMD_IMPORT_LATEST = BIN / "log16-import-latest-v05-2.sh"
CMD_STATUS = BIN / "log16-status.sh"
CMD_CASE = BIN / "log16-case-summary.sh"
CMD_LAST_REPORT = BIN / "log16-last-report.sh"

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except Exception as e:
    print("ERROR: tkinter is not available.")
    print("On Ubuntu, install it with:")
    print("  sudo apt install python3-tk")
    print()
    print("Details:", e)
    raise SystemExit(2)


class Log16Gui:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("log16 / КОНСУЛЬТАНТ v05.2")
        self.root.geometry("1100x760")

        self.queue: queue.Queue[str] = queue.Queue()
        self.running = False

        self._build_ui()
        self._poll_queue()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(
            main,
            text="log16 / КОНСУЛЬТАНТ v05.2",
            font=("TkDefaultFont", 14, "bold"),
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            main,
            text="Окно для вопроса, запуска v05.2, импорта в log16 и просмотра состояния дела.",
        )
        subtitle.pack(anchor="w", pady=(0, 8))

        q_frame = ttk.LabelFrame(main, text="Вопрос")
        q_frame.pack(fill=tk.X, pady=5)

        self.question = tk.Text(q_frame, height=4, wrap=tk.WORD)
        self.question.pack(fill=tk.X, expand=False, padx=6, pady=6)
        self.question.insert(
            "1.0",
            "Как привлекаемый участник будет находить своё поле деятельности в проекте?",
        )

        pattern_frame = ttk.Frame(main)
        pattern_frame.pack(fill=tk.X, pady=(2, 6))

        ttk.Label(pattern_frame, text="Pattern / дело:").pack(side=tk.LEFT)
        self.pattern = ttk.Entry(pattern_frame, width=36)
        self.pattern.pack(side=tk.LEFT, padx=6)
        self.pattern.insert(0, "participant_pathway")

        btns = ttk.Frame(main)
        btns.pack(fill=tk.X, pady=4)

        self.btn_ask = ttk.Button(
            btns,
            text="Спросить v05.2 + сохранить в log16",
            command=self.ask_import,
        )
        self.btn_ask.pack(side=tk.LEFT, padx=3)

        self.btn_latest = ttk.Button(
            btns,
            text="Импортировать последний run",
            command=self.import_latest,
        )
        self.btn_latest.pack(side=tk.LEFT, padx=3)

        self.btn_case = ttk.Button(
            btns,
            text="Показать дело",
            command=self.show_case,
        )
        self.btn_case.pack(side=tk.LEFT, padx=3)

        self.btn_status = ttk.Button(
            btns,
            text="Статус log16",
            command=self.show_status,
        )
        self.btn_status.pack(side=tk.LEFT, padx=3)

        self.btn_report = ttk.Button(
            btns,
            text="Последний отчёт",
            command=self.show_last_report,
        )
        self.btn_report.pack(side=tk.LEFT, padx=3)

        self.btn_clear = ttk.Button(
            btns,
            text="Очистить окно",
            command=self.clear_output,
        )
        self.btn_clear.pack(side=tk.RIGHT, padx=3)

        out_frame = ttk.LabelFrame(main, text="Ответ / отчёт / состояние дела")
        out_frame.pack(fill=tk.BOTH, expand=True, pady=6)

        self.output = tk.Text(out_frame, wrap=tk.WORD)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(out_frame, orient=tk.VERTICAL, command=self.output.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.configure(yscrollcommand=scroll.set)

        footer = ttk.Label(
            main,
            text="Подсказка: сначала нажми “Спросить v05.2 + сохранить в log16”, потом “Показать дело”.",
        )
        footer.pack(anchor="w", pady=(4, 0))

    def clear_output(self):
        self.output.delete("1.0", tk.END)

    def append(self, text: str):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def set_busy(self, busy: bool):
        self.running = busy
        state = tk.DISABLED if busy else tk.NORMAL
        for b in [
            self.btn_ask,
            self.btn_latest,
            self.btn_case,
            self.btn_status,
            self.btn_report,
            self.btn_clear,
        ]:
            b.configure(state=state)

    def run_command(self, title: str, cmd: list[str]):
        if self.running:
            return
        self.set_busy(True)
        self.queue.put(f"\n===== {title} =====\n")
        self.queue.put("$ " + " ".join(cmd) + "\n\n")

        def worker():
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
                assert proc.stdout is not None
                for line in proc.stdout:
                    self.queue.put(line)
                code = proc.wait()
                self.queue.put(f"\n[exit_code={code}]\n")
            except FileNotFoundError as e:
                self.queue.put(f"ERROR: command not found: {e}\n")
            except Exception as e:
                self.queue.put(f"ERROR: {type(e).__name__}: {e}\n")
            finally:
                self.queue.put("__DONE__")

        threading.Thread(target=worker, daemon=True).start()

    def _poll_queue(self):
        try:
            while True:
                item = self.queue.get_nowait()
                if item == "__DONE__":
                    self.set_busy(False)
                else:
                    self.append(item)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    def ask_import(self):
        question = self.question.get("1.0", tk.END).strip()
        if not question:
            messagebox.showwarning("Нет вопроса", "Введите вопрос.")
            return
        if not CMD_ASK_IMPORT.exists():
            messagebox.showerror("Нет скрипта", f"Не найдено: {CMD_ASK_IMPORT}")
            return
        self.run_command("Спросить v05.2 и импортировать в log16", [str(CMD_ASK_IMPORT), question])

    def import_latest(self):
        if not CMD_IMPORT_LATEST.exists():
            messagebox.showerror("Нет скрипта", f"Не найдено: {CMD_IMPORT_LATEST}")
            return
        self.run_command("Импортировать последний run v05.2", [str(CMD_IMPORT_LATEST)])

    def show_case(self):
        pattern = self.pattern.get().strip()
        if not pattern:
            pattern = "participant_pathway"
        if not CMD_CASE.exists():
            messagebox.showerror("Нет скрипта", f"Не найдено: {CMD_CASE}")
            return
        self.run_command("Показать дело log16", [str(CMD_CASE), "--pattern", pattern])

    def show_status(self):
        if not CMD_STATUS.exists():
            messagebox.showerror("Нет скрипта", f"Не найдено: {CMD_STATUS}")
            return
        self.run_command("Статус log16", [str(CMD_STATUS)])

    def show_last_report(self):
        if not CMD_LAST_REPORT.exists():
            messagebox.showerror("Нет скрипта", f"Не найдено: {CMD_LAST_REPORT}")
            return
        self.run_command("Последний отчёт log16", [str(CMD_LAST_REPORT)])


def main():
    tk_root = tk.Tk()
    app = Log16Gui(tk_root)
    tk_root.mainloop()


if __name__ == "__main__":
    main()
