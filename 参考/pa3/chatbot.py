import json
import openai
import tiktoken
def load_past_messages():
    with open("N_conversations.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    conversation = data["conversations"][-1]["messages"]
    return conversation

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    token_integers = encoding.encode(text)
    return len(token_integers)

def process_conversation(user_input):
    with open("N_conversations.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    conversation = data["conversations"][-1]["messages"]

    openai.api_key = "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"

    add_user_message(conversation, user_input)

    truncated_conversation = truncate_conversation(conversation, 5)
    token_count = sum(count_tokens(msg["content"]) for msg in truncated_conversation)

    if token_count > 2500:
        truncated_conversation = truncate_conversation(conversation, 1)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=truncated_conversation
    )

    assistant_reply = response.choices[0].message.content

    conversation.append({
        "role": "assistant",
        "content": assistant_reply
    })

    data["conversations"][-1]["messages"] = conversation

    with open("N_conversations.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return assistant_reply

def add_user_message(messages, message):
    messages.append({
        "role": "user",
        "content": message
    })

def truncate_conversation(messages, n_messages):
    return messages[-n_messages:]
