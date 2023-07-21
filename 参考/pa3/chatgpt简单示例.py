import openai

def ask_gpt(message: str) -> str:
    openai.api_key = "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"

    conversation = [
        {
            "role": "user",
            "content": message
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    assistant_reply = response.choices[0].message.content
    return assistant_reply

print("与 GPT-3.5-turbo 对话。按 q 键退出。")
while True:
    user_input = input("请输入问题：")
    if user_input.lower() == 'q':
        break

    assistant_reply = ask_gpt(user_input)
    print("助手的回复：")
    print(assistant_reply)
