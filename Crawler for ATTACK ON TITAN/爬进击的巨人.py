import requests
import re
import time
import threading
import os
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
chapter_link=requests.get('https://manhua.fzdm.com/39/',headers=headers,timeout=5)
chapter_link_get=re.findall('<a href="([^<]*?)" title="(进击的巨人.*?)">',chapter_link.text)
print(len(chapter_link_get))
g_lock=threading.Lock()
if not os.path.exists('进击的巨人'):
    os.makedirs('进击的巨人')
def downloadpic(chapterurl,page,failpage,pic):
    print('try to download%s %s'%(chapterurl,page))
    pageurl='%sindex_%d.html'%(chapterurl,page)
    global headers
    try:
        pageresponse=requests.get(pageurl,headers=headers,timeout=5)
        if pageresponse.status_code==404:
            return 0
        picurllast=re.findall('var mhurl="(.*?)"',pageresponse.text)[0]
        picurl='http://www-mipengine-org.mipcdn.com/i/p1.manhuapan.com/'+picurllast
    except:
        failpage.append(page)
        return 1
    try:
        downloadpicture= requests.get(picurl,timeout=5).content
        pic.append(downloadpicture)
        return 2
    except:
        failpage.append(page)
        return 1
class download(threading.Thread):
    def run(self):
        global chapter_link_get
        while len(chapter_link_get)>0:
            g_lock.acquire()
            url,title=chapter_link_get.pop()
            g_lock.release()
            if not os.path.exists('进击的巨人\%s'%title):
                os.makedirs('进击的巨人\%s'%title)
            url='https://manhua.fzdm.com/39/%s'%url
            failpage=[]
            page=1
            status=2
            while status!=0:
                pic=[]
                status=downloadpic(url,page,failpage,pic)
                if status==0:
                    break
                elif status==2:
                    with open('进击的巨人\%s\%s.jpg'%(title,page),'wb') as f:
                        f.write(pic[0])
                page=page+1
            for i in range(4):
                thisroundfailpage=[]
                for thisroundpage in failpage:
                    pic=[]
                    status=downloadpic(url,thisroundpage,thisroundfailpage,pic)
                    if status==2:
                        with open('进击的巨人\%s\%s.jpg' % (title, thisroundpage), 'wb') as f:
                            f.write(pic[0])
                failpage=thisroundfailpage
            with open('进击的巨人\%s\failpage.txt'%title,'w') as f:
                f.write(list(failpage))
if __name__=='__main__':
    for x in range(10):
        gospider=download()
        gospider.start()
