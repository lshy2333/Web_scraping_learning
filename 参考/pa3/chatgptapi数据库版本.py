import json
import openai

def add_user_message(conversation, message):
    conversation["messages"].append({
        "role": "user",
        "content": message
    })

# 读取JSON文件
with open("conversations.json", "r") as file:
    data = json.load(file)

# 获取最后一个对话
conversation = data["conversations"][-1]

# 使用API密钥进行身份验证
print("设置API密钥...")
openai.api_key = "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"

while True:
    # 从用户获取输入
    user_input = input("请输入问题：")
    add_user_message(conversation, user_input)

    # 发送API请求
    print("创建聊天补全...")
    response = openai.ChatCompletion.create(
        model=conversation["model"],
        messages=conversation["messages"]
    )

    # 获取助手的回复
    assistant_reply = response.choices[0].message.content

    # 将回复添加到消息列表中
    conversation["messages"].append({
        "role": "assistant",
        "content": assistant_reply
    })


    # 将数据写回JSON文件
    with open("conversations.json", "w") as file:
        json.dump(data, file, indent=2)

    # 打印助手的回复
    print("助手的回复：")
    print(assistant_reply)
