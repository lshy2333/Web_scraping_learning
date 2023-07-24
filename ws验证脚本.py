from web_scraping_json import web_scraping_json
print("url:")
url_name=input()
print("tag_name:")
tag_name=input()
print("class_name:")
class_name=input()
result=web_scraping_json(url_name,tag_name,class_name)
status=result[0]
content=result[1]
token_count=str(result[2])

# 使用索引访问元组中的元素
print("status:"+result[0]+"\ntoken_count:"+token_count+"\nif show 'y'")
switch=input()
if switch=="y":
    print(content)