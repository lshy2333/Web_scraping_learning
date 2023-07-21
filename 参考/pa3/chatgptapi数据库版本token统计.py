import json
import openai
import tiktoken
import time


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    token_integers = encoding.encode(text)
    return len(token_integers)


def add_user_message(conversation, message):
    conversation["messages"].append({
        "role": "user",
        "content": message
    })


def truncate_conversation(conversation, n_messages):
    return conversation[-n_messages:]


with open("conversations.json", "r") as file:
    data = json.load(file)

conversation = data["conversations"][-1]

print("设置API密钥...")
openai.api_key = "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"

while True:
    user_input = input("请输入问题：")
    user_tokens = count_tokens(user_input)
    print(f"User input tokens: {user_tokens}")
    add_user_message(conversation, user_input)

    truncated_conversation = truncate_conversation(conversation["messages"], 5)
    token_count = sum(count_tokens(msg["content"]) for msg in truncated_conversation)

    # 打印检测的 token 长度
    print(f"检测的 token 长度: {token_count}")

    if token_count > 2500:
        print("只发送了这次信息，因为 token 数量超过 2500。")
        truncated_conversation = truncate_conversation(conversation["messages"], 1)

    print(f"请求的内容：")
    print(json.dumps(truncated_conversation, indent=2))

    try:
        response = openai.ChatCompletion.create(
            model=conversation["model"],
            messages=truncated_conversation
        )
    except openai.error.RateLimitError as e:
        print("遇到速率限制错误，等待 5 秒后重试...")
        time.sleep(5)
        continue

    assistant_reply = response.choices[0].message.content
    assistant_tokens = count_tokens(assistant_reply)
    print(f"Assistant reply tokens: {assistant_tokens}")

    conversation["messages"].append({
        "role": "assistant",
        "content": assistant_reply
    })

    with open("conversations.json", "w") as file:
        json.dump(data, file, indent=2)

    print("助手的回复：")
    print(assistant_reply)
