import requests
import re
import time
import threading
import os
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
chapter_link=requests.get('https://manhua.fzdm.com/39/',timeout=5)#进击的巨人首页
chapter_link_get=re.findall('<a href="([^<]*?)" title="(进击的巨人.*?)">',chapter_link.text)#爬取章节名称以及对应的链接
#print(len(chapter_link_get))
g_lock=threading.Lock()
if not os.path.exists('进击的巨人'):#建立文件夹
    os.makedirs('进击的巨人')
def downloadpic(chapterurl,page,failpage,pic):#定义单章下载的函数
    print('try to download%s %s'%(chapterurl,page))
    pageurl='%sindex_%d.html'%(chapterurl,page)#根据网站的规则，由章节的url和页数，组成单页的url
    global headers
    try:
        pageresponse=requests.get(pageurl,headers=headers,timeout=5)
        if pageresponse.status_code==404 or pageresponse.status_code==500:
            return 0#返回0意味着本章已经爬完了
        picurllast=re.findall('var mhurl="(.*?)"',pageresponse.text)[0]
        picurl='http://www-mipengine-org.mipcdn.com/i/p1.manhuapan.com/'+picurllast#爬取图片的链接
    except:
        failpage.append(page)
        return 1
    try:
        downloadpicture= requests.get(picurl,timeout=5).content
        pic.append(downloadpicture)
        return 2#返回2说明本页成功下载，并且图片已经保存到pic的列表变量中
    except:
        failpage.append(page)
        return 1#返回1说明本页未成功下载，并且失败的页数已经保存到failpage的变量列表中
class download(threading.Thread):#定义多线程爬取
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
            for i in range(70):#每章不超过70
                pic=[]
                status=downloadpic(url,page,failpage,pic)
                if status==0:
                    break
                elif status==2:
                    with open('进击的巨人\%s\%s.jpg'%(title,page),'wb') as f:
                        f.write(pic[0])
                page=page+1
            for i in range(4):#将失败的页面再尝试4次
                thisroundfailpage=[]
                for thisroundpage in failpage:
                    pic=[]
                    status=downloadpic(url,thisroundpage,thisroundfailpage,pic)
                    if status==2:
                        with open('进击的巨人\%s\%s.jpg' % (title, thisroundpage), 'wb') as f:
                            f.write(pic[0])
                failpage=thisroundfailpage

            if len(failpage)>0:#如果还有失败的页面，输出个失败页面清单
                with open('进击的巨人\%sfailpage.txt'%title,'w') as f:
                    f.write(" ".join(failpage))
if __name__=='__main__':
    for x in range(20):
        gospider=download()
        gospider.start()
