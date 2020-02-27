import requests
from lxml import etree

class fdd:
    def __init__(self, url):
        self.url = url
        self.page=self._GetPage(self.url)

    def _GetChapterUrl(self,url):
        ChapNames = self.page.xpath('//td[@class="L"]/a/text()')#章节名
        ChapUrls = self.page.xpath('//td[@class="L"]/a/@href')  # url
        return ChapNames,ChapUrls

    def _GetPage(self,url):
        self.html = requests.get(url)
        self.html.encoding = 'utf-8'
        return etree.HTML(self.html.text)

    def _GetContent(self,url):
        page=self._GetPage(url)
        return page.xpath('//dd[@id="contents"]/text()')

    def ExpTxt(self,path):
        name=self.page.xpath('//title/text()')[0]
        FilePath=path+'\\'+name+'.txt'
        file=open(FilePath,'wb+')
        ChapNames, ChapUrls= self._GetChapterUrl(self.url)
        for i in range(len(ChapNames)):
            print(ChapNames[i])
            file.write(str(ChapNames[i]+'\n\n\n').encode("utf-8"))
            Contents = self._GetContent(ChapUrls[i])
            for j in range(len(Contents)):
                txt=str(Contents[j]).encode("utf-8")
                file.write(txt)
            file.write('\n\n\n\n'.encode("utf-8"))

if __name__=="__main__":
    url="https://www.23us.so/files/article/html/10/10839/index.html"
    obj=fdd(url)
    obj.ExpTxt('C:\\Users\\admin\\Desktop')

