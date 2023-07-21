import json
import requests
import tiktoken
import time

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

with open("new_conversations.json", "r", encoding="utf-8") as file:
    data = json.load(file)

if "conversations" not in data:
    data["conversations"] = []

if not data["conversations"]:
    data["conversations"].append({"messages": []})

conversation = data["conversations"][-1]["messages"]

url = "https://openai.api2d.net/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer fk194281-BEg4thfQmkW6oaEURrBQVm7ehxmKJoFi' # <-- 使用你自己的 Forward Key，注意前面的 Bearer 要保留，并且和 Key 中间有一个空格。
}

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

    data = {
        "model": "gpt-3.5-turbo",
        "messages": truncated_conversation
    }

    start_time = time.time()

    try:
        response = requests.post(url, headers=headers, json=data)
    except requests.exceptions.RequestException as e:
        print("遇到速率限制错误，等待 5 秒后重试...")
        time.sleep(5)
        continue

    response_time = time.time() - start_time
    print(f"本次请求用时：{response_time:.2f} 秒")

    response_json = response.json()

    assistant_reply = response_json["choices"][0]["message"]["content"]
    assistant_tokens = count_tokens(assistant_reply)
    print(f"Assistant reply tokens: {assistant_tokens}")
    print("助手的回复：")
    print(assistant_reply)

    conversation.append({
        "role": "assistant",
        "content": assistant_reply
    })

    conversation.append({
        "role": "assistant",
        "content": assistant_reply
    })

    new_conversation = {"messages": conversation, "response_time": response_time}

    if "conversations" not in data:
        data["conversations"] = []
        data["conversations"].append(new_conversation)
    else:
        data["conversations"][-1] = new_conversation

    with open("new_conversations.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
