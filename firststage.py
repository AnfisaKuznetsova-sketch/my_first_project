import os
import socket
import tkinter as tk
from tkinter import scrolledtext

running = True
def split_args(line):
    parts = []
    word = ""
    quote = ""
    for ch in line:
        if quote:
            if ch == quote:
                quote = ""
            else:
                word += ch
        elif ch == "'" or ch == '"':
            quote = ch
        elif ch == " ":
            if word:
                parts.append(word)
                word = ""
        else:
            word += ch
    if word:
        parts.append(word)
    return parts, quote



def execute(line):
    global running
    args, bad = split_args(line)

    if bad:
        return "Ошибка: незакрытая кавычка\n"
    if not args:
        return ""

    cmd = args[0]
    rest = args[1:]

    if cmd == "ls":
        out = "ls\n"
        if not rest:
            out += "Аргументов нет\n"
        else:
            out += "Аргументы:\n"
            for i, a in enumerate(rest, 1):
                out += f"  [{i}] '{a}'\n"
        return out

    if cmd == "cd":
        out = "cd\n"
        if not rest:
            out += "Аргументов нет\n"
        elif len(rest) > 1:
            out += f"Ошибка: cd принимает один аргумент, получено {len(rest)}\n"
        else:
            out += f"Аргументы:\n  [1] '{rest[0]}'\n"
        return out

    if cmd == "exit":
        running = False
        return "Завершение работы...\n"

    return f"Команда не найдена: {cmd}\n"



def on_enter(event):
    line = entry.get()
    entry.delete(0, tk.END)
    show("> " + line + "\n")
    answer = execute(line)
    if answer:
        show(answer)
    show("\n")
    if not running:
        entry.config(state="disabled")


def show(text):
    box.config(state="normal")
    box.insert(tk.END, text)
    box.see(tk.END)
    box.config(state="disabled")


root = tk.Tk()
root.title(f"Эмулятор - [{os.environ.get('USER', 'user')}@{socket.gethostname()}]")
root.geometry("700x450")

box = scrolledtext.ScrolledText(root, state="disabled",
                                bg="black", fg="white", font=("Consolas", 11))
box.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 0))

entry = tk.Entry(root, font=("Consolas", 12))
entry.pack(fill=tk.X, padx=6, pady=6)
entry.bind("<Return>", on_enter)
entry.focus_set()

show("Команды: ls, cd, exit\n\n")

root.mainloop()