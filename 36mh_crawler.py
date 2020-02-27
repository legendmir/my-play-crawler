import os
import time
import requests
from lxml import etree

def GetChapterUrl(url):
    '''
    :param url: 一人之下漫画url
    :return: 章节名字和url地址所构成的字典
    '''
    ChapDict = {}#空字典，用于放章节名和对应的url
    html = requests.get(url)#获取页面源码
    html.encoding = 'utf-8'
    page = etree.HTML(html.text)#解析
    ChapNames = page.xpath('//ul[@id="chapter-list-4"]/li/a/span/text()')#章节名
    for i in range(len(ChapNames)):
        if ChapNames[i].find('?')>=0:
            ChapNames[i]=ChapNames[i].replace('?','')
    ChapUrls = page.xpath('//ul[@id="chapter-list-4"]/li/a/@href')  # url
    for i in range(len(ChapNames)):
        ChapDict[ChapNames[i]]=ChapUrls[i]
    return ChapDict

def GetImgUrl(url):
    '''
    :param url: 图集url
    :return: 图集名字和图片地址所构成的字典
    '''
    ImgDict={}
    html = requests.get(url)#获取页面源码
    html.encoding = 'utf-8'
    page = etree.HTML(html.text)#解析
    ImgDict['1'] = page.xpath('//div/mip-link/mip-img/@src')[0]
    ImgNum=page.xpath('//span[@id="k_total"]/text()')[0]
    for i in range(2,int(ImgNum)+1):
        NextUrl=url.replace('.html','-%s.html'%str(i))#计算下一页url
        NextHtml = requests.get(NextUrl)
        NextPage = etree.HTML(NextHtml.text)  # 解析
        xxx=NextPage.xpath('//div/mip-link/mip-img/@src')
        if len(xxx)!=0:
            ImgDict[str(i)] = xxx[0]
    return ImgDict

def MakeDir(path):
    if os.path.exists(path):  # 判断路径及文件夹是否存在，不存在即创建
        pass
    else:
        os.mkdir(path)

def downloader(path,name,url,header={}):
    start = time.time()#开始时间
    size = 0
    response = requests.get(url,header)
    chunk_size = 1024#每次下载的数据大小
    content_size = int(response.headers['content-length'])#总大小
    if response.status_code == 200:
        print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))#换算单位并print
        with open(path+'\\%s'%name, "ab") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                file.flush()#清空缓存
                size += len(data)#已下载文件大小
                #\r指定行第一个字符开始，搭配end属性完成覆盖进度条
                print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50/ content_size),float(size / content_size * 100)),end='')
    end = time.time()#结束时间
    print('\n'+"%s下载完成！用时%.2f秒"%(name,(end-start)))

if __name__ == '__main__':

    url = 'https://m.36mh.com/manhua/jinjidejuren/'
    ChapDict=GetChapterUrl(url)
    DirPath="C:\\Users\\admin\\Desktop\\进击的巨人"
    MakeDir(DirPath)
    flag=0
    for name in ChapDict.keys():
        '''
        爬取36mh网站时，偶尔会有requests失败的时候，
        猜测可能是网站服务器有反爬限制，跟进继续爬可于下注释代码设置继续爬
        '''
        # if name == "Before the fall前传 57":
        #     flag = 1
        # if flag == 0:
        #     continue
        path=DirPath+"\\"+name
        MakeDir(path)
        ImgDic = GetImgUrl(ChapDict[name])
        for i in ImgDic.keys():
            downloader(path, '%s.jpg' % i,str(ImgDic[i]))
        ImgDic.clear()

