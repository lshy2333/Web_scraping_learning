import tkinter as tk
from tkinter import ttk
import threading
import time
import re
import requests


# 定义函数和变量
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def update_progressbar_color(value):
    if value < 50:
        color = rgb_to_hex((255, int(255 * value / 50), 0))
    else:
        color = rgb_to_hex((int(255 * (100 - value) / 50), 255, 0))
    s.configure("custom.Horizontal.TProgressbar", troughcolor="grey", background=color)


def update_progressbar(progressbar, value):
    progressbar['value'] = value
    update_progressbar_color(value)
    progressbar.update()





def send_message_thread(input_widget, chat_widget, progressbar, send_button):
    send_button.config(state="disabled")
    message = input_widget.get("1.0", "end-1c")
    input_widget.delete("1.0", tk.END)
    chat_widget.config(state="normal")
    chat_widget.insert(tk.END, f"User: {message}\n")
    chat_widget.see(tk.END)
    chat_widget.config(state="disabled")

    # 在此处添加调用聊天机器人API的代码，并根据API响应管理进度条和显示回复
    # 以下代码是一个简单的示例
    for i in range(100):
        update_progressbar(progressbar, i + 1)
        time.sleep(0.02)

    response = f"Chatbot: This is a response to '{message}'.\n"
    chat_widget.config(state="normal")
    chat_widget.insert(tk.END, response)
    chat_widget.see(tk.END)
    chat_widget.config(state="disabled")
    send_button.config(state="normal")
    progressbar['value'] = 0


def send_message(event=None):
    threading.Thread(target=send_message_thread, args=(input_widget, chat_widget, progressbar, send_button)).start()


def display_past_messages(chat_widget):
    chat_widget.config(state="normal")
    chat_widget.insert(tk.END, "Chat history loaded.\n")
    chat_widget.config(state="disabled")


def create_code_frame(parent):
    code_frame = tk.Frame(parent)
    scrollable_frame = ttk.Frame(code_frame)
    return code_frame, scrollable_frame


def extract_and_create_code_widgets(text, code_frame):
    code_blocks = re.findall(r'```([\s\S]*?)```', text)
    for code_block in code_blocks:
        code_widget = tk.Text(code_frame, wrap=tk.WORD, width=80, height=5, padx=5, pady=5)
        code_widget.insert(tk.END, code_block.strip())
        code_widget.pack()


def update_code_frame(text, code_frame):
    for child in code_frame.winfo_children():
        child.destroy()
    extract_and_create_code_widgets(text, code_frame)


# 设置图形用户界面
root = tk.Tk()
root.title("Chatbot")
root.geometry("800x600")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
# 创建一个自定义样式
s = ttk.Style()
s.theme_use("default")
s.configure("custom.Horizontal.TProgressbar", thickness=20)

# 使用自定义样式创建进度条
progressbar = ttk.Progressbar(main_frame, mode='determinate', maximum=100, style="custom.Horizontal.TProgressbar")
chat_widget = tk.Text(main_frame, wrap=tk.WORD, width=80, height=25, padx=5, pady=5, state="disabled")
chat_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

input_widget = tk.Text(main_frame, wrap=tk.WORD, width=80, height=5, padx=5, pady=5)
input_widget.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
input_widget.bind('<Return>', send_message)

send_button = ttk.Button(main_frame, text="Send", command=send_message)
send_button.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

progressbar = ttk.Progressbar(main_frame, mode='determinate', maximum=100)
progressbar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

display_past_messages(chat_widget)

code_frame, scrollable_frame = create_code_frame(main_frame)
code_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()

