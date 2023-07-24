import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import json
from token_count import count_tokens

def web_scraping_json(url_name: str, tag_name: str, class_name: str = ""):
    # 定义目标网页的url
    url = url_name
    text_all = []

    # 发送get请求，获取网页内容
    response = requests.get(url)

    # 判断请求是否成功
    if response.status_code == 200:
        # 解析网页内容，使用html.parser作为解析器
        soup = BeautifulSoup(response.text, "html.parser")

        if class_name == "":
            # 找到所有的特定标签
            tags = soup.find_all(tag_name)
            class_tag = "all_class"
        else:
            # 找到特定class的特定标签
            tags = soup.find_all(tag_name, class_=class_name)
            class_tag = "class_name:" + class_name

        # 创建 progress_output 文件夹
        if not os.path.exists('progress_output'):
            os.makedirs('progress_output')

        # 获取当前时间并格式化为字符串，用作文件名
        current_time = datetime.now().strftime(tag_name+"_"+class_tag)

        # 文件名
        filename = f'progress_output/{current_time}.json'

        # 如果文件已经存在，读取文件内容
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                text_all = json.load(f)

        # 遍历所有标签
        for tag in tags:
            tag_text = tag.text
            # 如果该标签的文本不在列表中，则添加到列表中
            if tag_text not in text_all:
                text_all.append(tag_text)

        # 检查 text_all 是否为空
        if text_all:
            status = "successful"
            content = "\n".join(text_all)
            token_count = count_tokens(content)
            # 将列表写入到json文件中
            with open(filename, 'w') as f:
                json.dump(text_all, f)
        else:
            print("No text found in tags.")
            status = "unsuccessful written"
            content = ""
            token_count = ""
    else:
        # 请求失败，打印出状态码
        print("请求失败，状态码为：", response.status_code)
        status = "unsuccessful written"
        content = ""
        token_count = ""

    return status, content, token_count
