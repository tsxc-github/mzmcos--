import datetime
import requests
import xml.etree.ElementTree as ET
from dateutil.parser import parse
from markdownify import markdownify as md
import os
import random
import yaml

response = requests.get("https://mzmc.top/feed",verify=False)
# os.open("feed.xml",os.O_CREAT)
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
    
os.makedirs("pages", exist_ok=True)
# os.open("pages/pages.yml",os.O_CREAT)
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
                f.write("[文章链接]("+link+") ")
                f.write("发布时间: "+pubDate+"\n")
                f.write(MDcontent)
            with open("pages/pages.yml","a",encoding='UTF-8') as f:
                f.write(" - "+"page"+str(order)+"\n")
            order+=1
            
os.system("mkdir public")
os.system("builder build --output-path public/output.xaml")

# 将卡片设置为折叠
with open("public/output.xaml","r",encoding='UTF-8') as f:
    Text=f.read().replace("IsSwaped=\"False\"","IsSwaped=\"True\"")
with open("public/output.xaml","w",encoding='UTF-8') as f:
    f.write(Text)
    
# 随机添加一条你知道吗
with open("Tips.yaml","r",encoding='UTF-8') as f:
    Tips=yaml.load(f.read(),Loader=yaml.FullLoader)["Tips"]
Tip=Tips[random.SystemRandom().randint(0,len(Tips)-1)]

with open("public/output.xaml","r",encoding='UTF-8') as f:
    Text=f.read().replace("$你知道吗$",Tip)
with open("public/output.xaml","w",encoding='UTF-8') as f:
    f.write(Text)