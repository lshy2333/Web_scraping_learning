import tkinter as tk
from tkinter import ttk
import re
from chatbot import process_conversation, load_past_messages
from tkinter import Canvas, Frame, Scrollbar
import threading
import time
import concurrent.futures

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*map(int, rgb))

def update_progressbar_color(progress, style_name):
    red = int(min(255, max(0, (1 - progress) * 510)))
    green = int(min(255, max(0, progress * 510 - 255)))
    s.configure(
        style_name,
        background=rgb_to_hex((red, green, 0)),
        troughcolor="#c2c2c2",
        bordercolor="#c2c2c2"
    )


def update_progressbar(value, end=False):
    if end or value == 0:
        send_button.config(state="enabled")
        progressbar.grid_remove()
        elapsed_time = round(time.time() - start_time, 2)
        remaining_time_label.configure(text=f"Last Time: {elapsed_time}s")
        return

    progress = value / progressbar["maximum"]
    progressbar["value"] = value
    update_progressbar_color(progress, "custom.Horizontal.TProgressbar")
    remaining_time = (progressbar["maximum"] - value) / 1000
    remaining_time_label.configure(text=f"Remaining Time: {remaining_time:.2f}s")

    if remaining_time_label["text"].startswith("Remaining Time"):
        root.after(100, lambda: update_progressbar(value - 1))

def update_progressbar(value, end=False):
    if end or value == 0:
        send_button.config(state="enabled")
        progressbar.grid_remove()
        return

    progress = value / progressbar["maximum"]
    progressbar["value"] = value
    update_progressbar_color(progress, "custom.Horizontal.TProgressbar")
    remaining_time = (progressbar["maximum"] - value) / 100
    remaining_time_label.configure(text=f"Remaining Time: {remaining_time:.2f}s")

    if remaining_time_label["text"].startswith("Remaining Time"):
        root.after(10, lambda: update_progressbar(value - 1))

def update_progressbar(value, end=False):
    if end or value == 0:
        send_button.config(state="enabled")
        progressbar.grid_remove()
        return

    progress = value / progressbar["maximum"]
    progressbar["value"] = value
    update_progressbar_color(progress, "custom.Horizontal.TProgressbar")
    remaining_time = (progressbar["maximum"] - value) / 100
    remaining_time_label.configure(text=f"Remaining Time: {remaining_time:.2f}s")

    if remaining_time_label["text"].startswith("Remaining Time"):
        root.after(10, lambda: update_progressbar(value - 1))

def send_message_thread(message):
    global start_time
    display.insert(tk.END, f'Assistant: Sending message to ChatGPT...\n')
    display.see(tk.END)

    progressbar["maximum"] = 6000
    progressbar["value"] = progressbar["maximum"]

    reply_received = False

    def process_message():
        reply = process_conversation(message)
        return reply, True

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(process_message)

        while not reply_received:
            remaining_time = int(progressbar["maximum"] - (time.time() - start_time) * 100)
            update_progressbar(remaining_time)
            root.after(100, root.update_idletasks())
            if future.done():
                reply, reply_received = future.result()
                update_progressbar(remaining_time, end=True)

    elapsed_time = round(time.time() - start_time, 2)
    send_button.config(state="enabled")
    progressbar.grid_remove()

    remaining_time_label.configure(text=f"Last Time: {elapsed_time}s")

    display.insert(tk.END, f'Assistant: Received reply from ChatGPT...\n')
    display.see(tk.END)

    codes = extract_and_create_code_widgets(reply)

    if codes:
        update_code_frame(codes)

    display.insert(tk.END, f'Assistant: {reply}\n')




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
code_frame, scrollable_frame = create_code_frame(root)
s = ttk.Style()
s.layout('custom.Horizontal.TProgressbar',
[('Horizontal.Progressbar.trough',
{'children': [('Horizontal.Progressbar.pbar',
{'side': 'left', 'sticky': 'ns'})],
'sticky': 'nswe'}),
('Horizontal.Progressbar.label', {'sticky': ''})])
for i in range(6):
   s.configure(f"custom.Horizontal.TProgressbar{i}", thickness=i * 2 + 2)

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
progressbar = ttk.Progressbar(main_frame, mode='determinate', length=300, maximum=5)

progressbar.grid(row=2, column=0, columnspan=2, sticky='NSEW', pady=5)
progressbar.grid_remove() # 默认隐藏进度条

remaining_time_label = ttk.Label(main_frame, text='Last Time: 5s')
remaining_time_label.grid(row=3, column=0, columnspan=2)

root.bind('<Return>', send_message)

root.mainloop()