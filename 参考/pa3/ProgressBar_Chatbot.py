import tkinter as tk
from tkinter import ttk
import re
from chatbot import process_conversation, load_past_messages
from tkinter import Canvas, Frame, Scrollbar
import threading

# 定义 send_message_thread 函数，将在新线程中运行
import time

def send_message_thread(message):
    display.insert(tk.END, f'Assistant: Sending message to ChatGPT...\n')
    display.see(tk.END)

    # 开始倒计时
    progressbar["maximum"] = 10
    progressbar["value"] = 0
    progressbar_update()

    reply = process_conversation(message)

    display.insert(tk.END, f'Assistant: Received reply from ChatGPT...\n')
    display.see(tk.END)

    codes = extract_and_create_code_widgets(reply)

    if codes:
        update_code_frame(codes)

    display.insert(tk.END, f'Assistant: {reply}\n')

    # 完成后，隐藏进度条
    progressbar.grid_remove()

def progressbar_update():
    progressbar["value"] += 1
    if progressbar["value"] < progressbar["maximum"]:
        root.after(1000, progressbar_update)  # 每隔 1000 毫秒（1 秒）更新一次进度条
    else:
        send_button.config(state="normal")  # 在倒计时结束后启用发送按钮

def send_message(event=None):
    message = user_input.get()
    display.insert(tk.END, f'User: {message}\n')
    user_input.delete(0, tk.END)

    # 显示进度条并启动新线程
    progressbar.grid(row=2, column=0, columnspan=2, sticky='NSEW', pady=5)
    send_button.config(state="disabled")  # 禁用发送按钮，直到倒计时结束
    thread = threading.Thread(target=send_message_thread, args=(message,))
    thread.start()


def display_past_messages():
    past_messages = load_past_messages()
    for msg in past_messages:
        role, content = msg["role"].capitalize(), msg["content"]
        display.insert(tk.END, f'{role}: {content}\n')

    display.see(tk.END)

def create_code_frame(root):
    code_frame = Frame(root)
    code_frame.grid(row=0, column=1, sticky='NS')

    canvas = Canvas(code_frame, bg='white', height=400, width=300)
    scrollbar = Scrollbar(code_frame, orient='vertical', command=canvas.yview)
    scrollable_frame = Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='left', fill='y')

    return code_frame, scrollable_frame

def extract_and_create_code_widgets(content):
    code_pattern = r"```([^`]+)```"
    code_blocks = re.findall(code_pattern, content)
    return code_blocks

def update_code_frame(codes):
    for code_widget in scrollable_frame.winfo_children():
        code_widget.destroy()

    for idx, code in enumerate(codes):
        code_label = ttk.Label(scrollable_frame, text=f'Code-Python ({idx + 1}):')
        code_label.grid(row=idx * 2, column=0, padx=5, pady=5, sticky='w')

        code_widget = tk.Text(scrollable_frame, wrap='word', height=5, width=40, padx=5, pady=5)
        code_widget.insert(tk.END, code)
        code_widget.grid(row=idx * 2 + 1, column=0, padx=5, pady=5)
        code_widget.config(state='disabled')


root = tk.Tk()
root.title('Chatbot')
# 在 main_frame 中添加进度条

code_frame, scrollable_frame = create_code_frame(root)
main_frame = ttk.Frame(root, padding='10')
main_frame.grid(row=0, column=0, sticky='NSEW')

display = tk.Text(main_frame, wrap='word', width=80, height=25)
display.grid(row=0, column=0, columnspan=2, sticky='NSEW')

display_past_messages()

user_input = ttk.Entry(main_frame, width=80)
user_input.grid(row=1, column=0, sticky='W')

send_button = ttk.Button(main_frame, text='Send', command=send_message)
send_button.grid(row=1, column=1, sticky='E')
progressbar = ttk.Progressbar(main_frame, mode='indeterminate', length=300)

progressbar.grid(row=2, column=0, columnspan=2, sticky='NSEW', pady=5)
progressbar.grid_remove()  # 默认隐藏进度条
root.bind('<Return>', send_message)

root.mainloop()
