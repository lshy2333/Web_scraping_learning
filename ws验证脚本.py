from Web_Scraping import web_scraping
print("url:")
url_name=input()
print("class_name:")
class_name=input()
result=web_scraping(url_name,class_name)
status=result[0]
content=result[1]
token_count=str(result[2])

# 使用索引访问元组中的元素
print("status:"+result[0]+"\ntoken_count:"+token_count+"\nif show 'y'")
switch=input()
if switch=="y":
    print(content)