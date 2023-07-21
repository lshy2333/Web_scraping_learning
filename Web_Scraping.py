# 导入requests库和BeautifulSoup库
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from token_count import count_tokens

def web_scraping(url_name:str, class_name:str=""):
    # 定义目标网页的url
    url = url_name
    text_all=""

    # 发送get请求，获取网页内容
    response = requests.get(url)

    # 判断请求是否成功
    if response.status_code == 200:
        # 解析网页内容，使用html.parser作为解析器
        soup = BeautifulSoup(response.text, "html.parser")

        if class_name == "":
            # 找到所有的div标签
            divs = soup.find_all('div')
            class_tag = "all_class"
        else:
            # 找到特定class的div标签
            divs = soup.find_all('div', class_=class_name)
            class_tag = "class_name:" + class_name

        # 创建 progress_output 文件夹
        if not os.path.exists('progress_output'):
            os.makedirs('progress_output')

        # 获取当前时间并格式化为字符串，用作文件名
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S' + class_tag)

        # 创建并打开文件
        with open(f'progress_output/{current_time}.txt', 'w') as f:
            # 遍历所有div标签
            for div in divs:
                p_list = div.find_all("p")
                for p in p_list:
                    text_all=text_all+'\n'+p.text
                    f.write(p.text + '\n')



        # 检查 p_list 是否为空
        if text_all:
            status = "successful"
            content = text_all
            token_count = count_tokens(content)

        else:
            print("No text found in divs.")
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
