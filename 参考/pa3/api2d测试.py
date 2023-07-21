import requests

url = "https://openai.api2d.net/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer fk194281-BEg4thfQmkW6oaEURrBQVm7ehxmKJoFi' # <-- 把 fkxxxxx 替换成你自己的 Forward Key，注意前面的 Bearer 要保留，并且和 Key 中间有一个空格。
}

data = {
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "apple is what mean?"}]
}

response = requests.post(url, headers=headers, json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())

# 提取 'content' 并打印
content = response.json()["choices"][0]["message"]["content"]
print("Content: ", content)
