import datetime
import requests
import xml.etree.ElementTree as ET
from dateutil.parser import parse
from markdownify import markdownify as md
import os

response = requests.get("https://mc.boen.fun/feed",verify=False)
os.open("feed.xml",os.O_CREAT)
with open("feed.xml","w",encoding='UTF-8') as f:
    f.write(response.text)
tree =ET.parse("feed.xml")

response.keep_alive = False
response.close()

print(tree)
root = tree.getroot()

# 删除所有临时文件
for i in range(1,100):
    try:
        os.remove("libraries/"+"page"+str(i)+".md")
    except:
        pass

os.open("pages/pages.yml",os.O_CREAT)
with open("pages/pages.yml","w",encoding='UTF-8') as f:
    f.write("name: pages\ncards:\n - header\n")

order=1
for child in root:
    for subchild in child:
        if(subchild.tag == "item"):
            for item in subchild:
                # if(item.tag == "{http://purl.org/dc/elements/1.1/}creator"):
                #     print(item.text)# 作者
                #     creator=item.text
                if(item.tag == "title"):
                    print(item.text)# 标题
                    title=item.text
                if(item.tag == "pubDate"):
                    print(item.text)# 发布时间
                    pubDate=item.text
                if(item.tag == "link"):
                    # print(item.text)# 文章链接
                    link=item.text
                if(item.tag == "{http://purl.org/rss/1.0/modules/content/}encoded"):
                    # print(item.text)# 文章内容
                    content=item.text
                if(item.tag == "description"):
                    # print(item.text)# 文章描述
                    description=item.text
            print("=====================================")
            pubDate=(parse(pubDate)+datetime.timedelta(hours=8)).strftime("%Y年%m月%d日 %H:%M:%S")
            MDcontent=md(content)
            os.open("libraries/"+"page"+str(order)+".md",os.O_CREAT)
            with open("libraries/"+"page"+str(order)+".md","w",encoding='UTF-8') as f:
                f.write("# "+title+"\n")
                f.write("发布时间: "+pubDate+"\n")
                f.write(MDcontent)
            with open("pages/pages.yml","a",encoding='UTF-8') as f:
                f.write(" - "+"page"+str(order)+"\n")
            order+=1
            
            
os.system("builder build")