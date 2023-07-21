# 导入requests库和BeautifulSoup库
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# 定义目标网页的url
url = "https://huggingface.co/meta-llama/Llama-2-7b"

# 发送get请求，获取网页内容
response = requests.get(url)

# 判断请求是否成功
if response.status_code == 200:
    # 解析网页内容，使用html.parser作为解析器
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到所有的div标签
    divs = soup.find_all('div')

    # 创建 output 文件夹
    if not os.path.exists('output'):
        os.makedirs('output')

    # 获取当前时间并格式化为字符串，用作文件名
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 创建并打开文件
    with open(f'output/{current_time}.txt', 'w') as f:
        # 遍历所有div标签
        for div in divs:
            p_list = div.find_all("p")
            for p in p_list:
                f.write(p.text + '\n')
                print(p.text)

else:
    # 请求失败，打印出状态码
    print("请求失败，状态码为：", response.status_code)
