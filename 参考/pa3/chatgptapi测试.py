import openai

print("设置API密钥...")
openai.api_key = "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"

print("创建聊天补全...")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?,relpy in chinese!"}
    ]
)

print("收到响应：")
print(response)

print("提取助手的回复...")
assistant_reply = response.choices[0].message.content

print("助手的回复：")
print(assistant_reply)
