#coding:GBK
'''
#顶点小说,小说下载 ==> .txt
#https://www.x23us.com/html/59/59253/
#绝世剑神
'''
import re
import requests as REQ
from bs4 import BeautifulSoup as SP
#天津小说网
url='https://www.x23us.com/html/59/59253/'
url=input("https://www.x23us.com/\n\t顶点小说\n\n请输入小说网址:")
head={"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360EE'}

try:
    r = REQ.get(url,headers=head)
except:
    print("网址错误:"+url)
    input()
    quit()

encode='GBK'
r.encoding = encode
s = r.text
h = SP(s,'lxml')
novel=h.find(id = 'info')
fname =h.find('title').text.split()[0]
novel=h.find(id = 'intro')

简介='' #novel.text.strip()
print(fname,简介)
urls=[]
li=h.find(id= 'at')
i=0
for aa in li.find_all('a'):
    #print(aa)
    i+=1
    if i<1:continue
    urls.append((aa['href'],re.sub('^(\d+)','第\\1章 ',aa.string)))
#urls=set(urls)
#urls=list(urls)
#urls.sort()
f=open(fname+'.txt','wb')
f.write( bytes(fname+'\n\n'+简介+'\n','utf-8'))
ii=len(urls)
j=input("\n\t起始页（总页数%d）:"%len(urls))
jj=input("\n\t结束页（总页数%d）:"%len(urls))

j=int(j) if j.isdigit() else 0
jj=int(jj) if jj.isdigit() else len(urls)
print(j,jj)
jj+=1
#url=url[:url.rfind('/b')]
i=0
for ur in urls:
    i+=1

    if i<j:
        #print(i,end='\t');
        continue
    if i==jj:break
    print(fname+"[%04d-%04d]:\t"%(ii,i)+ur[1])    
    u = url+ur[0]
    try:
        r = REQ.get(u,headers=head)
    except:
        print("Try again...")
        print("...."+fname+"[%04d-%04d]:\t"%(ii,i)+ur[1])
        r = REQ.get(u,headers=head)
    if not r.ok : r = REQ.get(u,headers=head)
    r.encoding = encode
    s = r.text
    txt=SP(s,'lxml')
    t=txt.find(id="contents")
    if t==None: continue
    t=t.text
    t=t.replace('\xa0',' ') #空格 \xa0
    t=t.replace("    ",'\n\t')
    t=t.replace('\r',"")
    t=t.replace('\t\t',"")
    t=t.replace('\t\t',"\t")
    re.sub(r'\t第\w+章.+','\n',t)
    t=t.replace('\n\n',"\n")
    f.write( bytes('\n'+ur[1]+t,'utf-8'))
f.close()

#the End
