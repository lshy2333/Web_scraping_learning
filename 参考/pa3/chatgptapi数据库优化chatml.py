import json
import openai
import tiktoken
import time
import tkinter as tk
from tkinter import scrolledtext

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    token_integers = encoding.encode(text)
    return len(token_integers)

def add_user_message(messages, message):
    messages.append({
        "role": "user",
        "content": message
    })


def truncate_conversation(messages, n_messages):
    return messages[-n_messages:]

with open("N_conversations.json", "r", encoding="utf-8") as file:
    data = json.load(file)

conversation = data["conversations"][-1]["messages"]

print("设置API密钥...")
openai.api_key = "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"

while True:
    user_input = input("请输入问题：")
    user_tokens = count_tokens(user_input)
    print(f"User input tokens: {user_tokens}")
    add_user_message(conversation, user_input)

    truncated_conversation = truncate_conversation(conversation, 5)
    token_count = sum(count_tokens(msg["content"]) for msg in truncated_conversation)

    print(f"检测的 token 长度: {token_count}")

    if token_count > 2500:
        print("只发送了这次信息，因为 token 数量超过 2500。")
        truncated_conversation = truncate_conversation(conversation, 1)

    print(f"请求的内容：")
    print(json.dumps(truncated_conversation, indent=2, ensure_ascii=False))

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=truncated_conversation
        )
    except openai.error.RateLimitError as e:
        print("遇到速率限制错误，等待 5 秒后重试...")
        time.sleep(5)
        continue

    assistant_reply = response.choices[0].message.content
    assistant_tokens = count_tokens(assistant_reply)
    print(f"Assistant reply tokens: {assistant_tokens}")

    conversation.append({
        "role": "assistant",
        "content": assistant_reply
    })

    data["conversations"][-1]["messages"] = conversation

    with open("N_conversations.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print("助手的回复：")
    print(assistant_reply)


class ChatGPTGUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatGPT")

        self.conversation_frame = tk.Frame(master)
        self.conversation_frame.pack(pady=10)

        self.conversation_text = scrolledtext.ScrolledText(self.conversation_frame, wrap=tk.WORD, width=100, height=20)
        self.conversation_text.pack()

        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10)

        self.user_input = tk.Entry(self.input_frame, width=80)
        self.user_input.pack(side=tk.LEFT)

        self.submit_button = tk.Button(self.input_frame, text="发送", command=self.submit_input)
        self.submit_button.pack(side=tk.LEFT, padx=(10, 0))

    def submit_input(self):
        user_input = self.user_input.get()
        self.conversation_text.insert(tk.END, f"你: {user_input}\n")
        self.user_input.delete(0, tk.END)

        # 原有代码的用户输入处理...

        assistant_reply = "这是助手的回复。"  # 替换为从 GPT-3.5-turbo 模型获取的回复
        self.conversation_text.insert(tk.END, f"助手: {assistant_reply}\n")
        self.conversation_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGPTGUI(root)
    root.mainloop()