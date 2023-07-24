from  web_scraping_json import  web_scraping_json
a=input()
for i in range(a,9000):
    j=str(i)
    print(j)
    url="https://huggingface.co/models?p="+j+"&sort=trending"
    results=web_scraping_json(url,"h4","")
    print(results[0])