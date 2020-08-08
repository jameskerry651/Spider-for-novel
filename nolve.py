import requests
import re
from time import sleep


#该函数是获取原始的html并解码
def spider(url):
    head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; '
                           'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    data=requests.get(url,head)
    data.encoding='gbk'
    html=data.text
    return html


#该函数是用来从html中获取小说文本内容，以及保持排序正确
def cleardata(unclear_data):
    pat1=re.compile(r'<div id="txtContent">(.*)<br/>',re.DOTALL)      #从html中取文本的正则式子

    st=pat1.findall(unclear_data)

#此处简单处理文本多余信息（虽然 代码不太美观 - -）
    s1=str(st).replace(r"\r\n\t\r\n        \r\n        \r\n        \t\r\n        \u3000\u3000","")
    s1=str(s1).replace(r"<div class='gad2'><script type='text/javascript'>try{mad1();} catch(ex){}</script></div>","")
    s1=str(s1).replace(r"<br/>\u3000\u3000","\n  ")
    s1=s1.replace('[','')
    s1=s1.replace(']','')
    #print(s1)

    return s1

#该函数主要是获取章节的链接 和名称（由于章节的链接并不是规律的 循环没法生成一个链接列表，所以需要从小说目录链接爬取章节链接和名字
def novel_spider():
    urlls=spider('https://www.boquge.com/book/84409/')
    pat_url=re.compile(r'<li >(.*?)</li>')

    url_n=pat_url.findall(urlls,re.DOTALL)


    pat_link=re.compile(r'href="(.*?)"')
    pat_chapter=re.compile(r'>(.*)</a>')
    ls_link=[]
    ls_chaper=[]
    for i in url_n:
        link=pat_link.findall(i)  #得到是一个列表
        link='https://www.boquge.com/'+link[0]


        chapter=pat_chapter.findall(i)[0]
        ls_link.append(link)
        ls_chaper.append(chapter)

    return ls_link,ls_chaper


#正式开始 并调用上面的函数
def start():
    ls_link,ls_chaper=novel_spider()
    count_num=0
    for i,j in zip(ls_link,ls_chaper):
        count_num=count_num+1
        try:
            data=spider(i)
            sleep(0.2)              #加入sleep是因为速度过快，服务器没有响应 就开始爬取下一章，导致小说不连续
            cdata=cleardata(data)
            #print(cdata)
            if len(cdata)>200 :
                print(f'第{count_num}章爬取成功')
            else:
                print(f"第{count_num}章断线")
            with open(r'D:\python项目文件\诡秘之主.txt','a') as fp:         #此处有些瑕疵，应该先打开文件后再爬取，不需要重复打开文件，只需要多次写入

                fp.write('\n'+str(j)+'\n')           


                fp.write(str(cdata))
                print('成功写入')
        except:
            print('写入失败')




start()
