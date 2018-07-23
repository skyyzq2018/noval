#coding:GBK
'''
#四库书,小说下载 ==> .txt
# http://www.sikushu.org/book/134282/
'''
import re
import requests as REQ
from bs4 import BeautifulSoup as SP
head={"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360EE'}

#天津小说网
url='http://www.sikushu.org/book/134282/'
url=input("http://www.sikushu.org/\n\t四库书\n请输入小说网址:")
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
fname =novel.find('h1').string.strip()
novel=h.find(id = 'intro')

简介=novel.text.strip()
print(fname,简介)
urls=[]
li=h.find(id= 'list')
i=0
for aa in li.find_all('a'):
    #print(aa)
    i+=1
    if i<10:continue
    urls.append((aa['href'],re.sub('^(\d+)','第\\1章 ',aa.string)))
#urls=set(urls)
#urls=list(urls)
#urls.sort()
f=open('txt\\'+fname+'.txt','wb')
f.write( bytes(fname+'\n\n'+简介+'\n','utf-8'))

j=input("\n\t起始页（总页数%d）:"%len(urls))
jj=input("\n\t结束页（总页数%d）:"%len(urls))

j=int(j) if j.isdigit() else 0
jj=int(jj) if jj.isdigit() else len(urls)
print(j,jj)
jj+=1
url=url[:url.rfind('/b')]
i=0
for ur in urls:
    i+=1

    if i<j:
        #print(i,end='\t');
        continue
    if i==jj:break
    print(fname+":\t"+ur[1])    
    u = url+ur[0]
    try:
        r = REQ.get(u,headers=head)
    except:
        print("Try again...")
        print("...."+fname+":\t"+ur[1])
        r = REQ.get(u,headers=head)
    if not r.ok : r = REQ.get(u,headers=head)
    r.encoding = encode
    s = r.text
    txt=SP(s,'lxml')
    t=txt.find(id="content")
    if t==None: continue
    t=t.text
    t=t.replace('\xa0',' ') #空格 \xa0
    t=t.replace("    ",'\n\t')
    t=t.replace('\r',"")
    t=t.replace('(四库书 www.sikushu.org)','')
    t=t.replace('（本章完）3k (四库书小说网 www.sikushu.org)chaptererror()','\n')
    t=t.replace('(四库书小说网 www.sikushu.org)','')
    t=t.replace('\t\t',"")
    t=t.replace('\t\t',"\t")
    re.sub(r'\t第\w+章.+','\n',t)
    t=t.replace('\n\n',"\n")
    f.write( bytes('\n'+ur[1]+t,'utf-8'))
f.close()

#the End
