import tkinter as tk
from tkinter import ttk
from chatbot import process_conversation, load_past_messages

def send_message(event=None):
    message = user_input.get()
    display.insert(tk.END, f'User: {message}\n')
    user_input.delete(0, tk.END)

    display.insert(tk.END, f'Assistant: Sending message to ChatGPT...\n')
    display.see(tk.END)

    reply = process_conversation(message)

    display.insert(tk.END, f'Assistant: Received reply from ChatGPT...\n')
    display.see(tk.END)

    display.insert(tk.END, f'Assistant: {reply}\n')

def display_past_messages():
    past_messages = load_past_messages()
    for msg in past_messages:
        role, content = msg["role"].capitalize(), msg["content"]
        display.insert(tk.END, f'{role}: {content}\n')

    # 滚动到文本框底部
    display.see(tk.END)


root = tk.Tk()
root.title('Chatbot')

frame = ttk.Frame(root, padding='10')
frame.grid(row=0, column=0, sticky='NSEW')

display = tk.Text(frame, wrap='word', width=80, height=25)
display.grid(row=0, column=0, columnspan=2, sticky='NSEW')

display_past_messages()

user_input = ttk.Entry(frame, width=80)
user_input.grid(row=1, column=0, sticky='W')

send_button = ttk.Button(frame, text='Send', command=send_message)
send_button.grid(row=1, column=1, sticky='E')

# 绑定Enter键到发送消息的功能
root.bind('<Return>', send_message)

root.mainloop()
