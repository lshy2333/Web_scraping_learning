#写一个程序调用openai的dalle模型

import openai
import json
import time

def add_user_message(conversation, message):
    conversation["messages"].append({
        "role": "user",
        "content": message
    })


def truncate_conversation(conversation, n_messages):
    return conversation[-n_messages:]

with open("conversations.json", "r") as file:
    data = json.load(file)
