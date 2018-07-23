#coding:GBK
'''
#笔趣阁,小说下载 ==> .txt
#http://www.biquge.lu/book/27659/
http://www.shengyan.org/book/108342.html
'''
import re
import requests as REQ
from bs4 import BeautifulSoup as SP
#天津小说网
url='http://www.sikushu.org/book/134282/'
url=input("http://www.biquge.lu/\nhttp://www.shengyan.org\n\t笔趣阁\n请输入小说网址:")
try:
    r = REQ.get(url)
except:
    print("网址错误:"+url)
    input()
    quit()

encode='GBK'
r.encoding = encode
s = r.text
h = SP(s,'lxml')
novel=h.find(class_ = 'info')
fname =novel.find('h2').string.strip()
novel=h.find(class_ = 'intro')

简介=novel.text.strip()
print(fname,简介)
urls=[]
li=h.find(class_= 'listmain')
i=0
x=6
url=url[:url.rfind('/b')]
if url=='http://www.shengyan.org':x=12


for aa in li.find_all('a'):
    #print(aa)
    i+=1
    if i<=x:continue
    
    urls.append((aa['href'],re.sub('^(\d+)','第\\1章 ',aa.string)))
#urls=set(urls)
#urls=list(urls)
#urls.sort()

f=open('txt\\'+fname+'.txt','wb')
f.write( bytes(fname+'\n\n'+简介+'\n','utf-8'))
ii=len(urls)
j=input("\n\t起始页（总页数%d）:"%len(urls))
jj=input("\n\t结束页（总页数%d）:"%len(urls))

j=int(j) if j.isdigit() else 0
jj=int(jj) if jj.isdigit() else len(urls)
print(j,jj)
jj+=1

i=0
for ur in urls:
    i+=1

    if i<j:
        #print(i,end='\t');
        continue
    if i==jj:break
    print(fname+"[%04d:%04d"%(ii,i)+"]:\t"+ur[1])    
    u = url+ur[0]
    try:
        r = REQ.get(u)
    except:
        print("Try again...")
        print("...."+fname+":\t"+ur[1])
        r = REQ.get(u)
    if not r.ok : r = REQ.get(u)
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
    t=t.replace('(四库书小说网 www.sikushu.org)chaptererror()','\n')
    t=t.replace('(四库书小说网 www.sikushu.org)','')
    t=t.replace('\t\t',"")
    t=t.replace('\t\t',"\t")
    t=t.replace('\t\n',"")
    t=t.replace('\t ',"\t")
    re.sub(r'\t第\w+章.+','\n',t)
    t=re.sub(r'【推荐】.+','\n',t)
    t=t.replace('\n\n',"\n")
    f.write( bytes('\n'+ur[1]+t,'utf-8'))
f.close()

#the End
