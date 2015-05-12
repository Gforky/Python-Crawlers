__author__ = 'LWM'
# -*- coding: utf-8 -*-
import urllib2
import re
import codecs

# tool used to replace some useless tags
class tagTool:
    # remove img tags, 7 continuous spaces
    removeImg = re.compile('<img.*?>| {7}')
    # remove anchor tags
    removeAnchor = re.compile('<a.*?>|</a>')
    # replace line break with \n
    replaceLineBreak = re.compile('<tr>|<div>|<p.*?>|</tr>|</div>|</p>')
    # replace <td> with \t
    replaceTD = re.compile('<td>')
    # replace <br> with \n\n
    replaceBR = re.compile('<br><br>|<br>')
    # remove other tags
    removeOtherTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, '', x)
        x = re.sub(self.removeAnchor, '', x)
        x = re.sub(self.replaceLineBreak, '\r\n', x)
        x = re.sub(self.replaceTD, '\t', x)
        x = re.sub(self.replaceBR, '\r\n', x)
        x = re.sub(self.removeOtherTag, "", x)
        return x.strip()

# 百度贴吧爬虫
class BDTB:
    # Initialize the base url and parameters
    def __init__(self, baseUrl, seeLZ):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.MyTagTool = tagTool()
        self.floor = 1
        self.file = None
        self.defaultFileName = u'百度贴吧'
        self.curPageIndex = 1

    # get the html code according to the page index
    def getPage(self, pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # read() function to read an object and return a string, decode the string using 'utf-8'
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, 'reason'):
                print 'loading page failed: ', e.reason
            return None

    # get appropriate title
    def getTitle(self, page):
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # get the total number of pages of current post
    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?<span.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # get the content of the post
    def getPageContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        result = re.findall(pattern, page)
        contents = []
        for item in result:
            contents.append('\r\n' + self.MyTagTool.replace(item) + '\r\n')
        return contents

    # set the file's name
    def setFileName(self, title):
        if title is not None:
            self.file = codecs.open(title + '.txt', 'w+', encoding='utf-8')
        else:
            self.file = codecs.open(self.defaultFileName + '.txt', 'w+', encoding='utf-8')

    # write data into file
    def writeData(self, contents):
        for content in contents:
            floorLine = '\r\n' + str(self.floor) + u'楼-----------------------------------------------------------\r\n'
            self.file.write(floorLine)
            self.file.write(content)
            self.floor += 1

    # start function
    def start(self):
        startPage = self.getPage(1)
        pageNum = self.getPageNum(startPage)
        fileName = self.getTitle(startPage)
        self.setFileName(fileName)
        if pageNum is None:
            print 'URL 已失效'
            return None
        try:
            print '该贴共有 ' + str(pageNum) + ' 页'
            for index in range(1, int(pageNum) + 1):
                print '正在写入第 ' + str(index) + ' 页内容'
                page = self.getPage(index)
                pageContent = self.getPageContent(page)
                self.writeData(pageContent)
        except IOError, e:
            print '写入异常: ' + e.message
        finally:
            print '写入过程结束'


baseUrl = 'http://tieba.baidu.com/p/' + str(raw_input('请输入需要抓取的帖子编号\n'))
seeLZ = raw_input('请确认是否只获取楼主发言：是请输入1， 否请输入0\n')
myBDTB = BDTB(baseUrl, seeLZ)
myBDTB.start()
