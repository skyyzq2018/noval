#coding:GBK
'''
#文学迷,小说下载 ==> .txt
#https://www.wenxuemi.com/files/article/html/23/23636/
#https://www.wenxuemi.com/files/article/html/23/23636/11370428.html
'''
import re
import requests as REQ
from bs4 import BeautifulSoup as SP
print("\n文学迷:  https://www.wenxuemi.com \n")
url='http://www.sikushu.org/book/134282/'
url=input("请输入小说网址:")
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
    #i+=1
    #if i<10:continue
    urls.append((aa['href'],re.sub('^(\d+)','第\\1章 ',aa.string)))
#urls=set(urls)
#urls=list(urls)
#urls.sort()
f=open(fname+'.txt','wb')
f.write( bytes(fname+'\n\n'+简介+'\n','utf-8'))

j=input("\n\t起始页（总页数%d）:"%len(urls))
jj=input("\n\t结束页（总页数%d）:"%len(urls))

j=int(j) if j.isdigit() else 0
jj=int(jj) if jj.isdigit() else len(urls)
print(j,jj)
jj+=1
url=url[:url.rfind('/files')]
i=0
for ur in urls:
    i+=1

    if i<j:
        #print(i,end='\t');
        continue
    if i==jj:break
    print(fname+":\t"+re.sub('^(第.+章)(.+)',r'\1 \2',ur[1]))    
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
    re.sub(r'\t第\w+章.+','\n',t)
    t=t.replace('\n\n',"\n")
    f.write( bytes('\n\n'+re.sub('^(第.+章)(.+)',r'\1 \2',ur[1])+'\n'+t,'utf-8'))
f.close()

#the End
