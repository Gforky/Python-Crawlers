__author__ = 'LWM'
# -*- coding : utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
import codecs

#qiushibaike crawler
class QSBK:
	#Initialization
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (Compatible; MSIE 5.5; Windows NT)'
		#Initialize headers
		self.headers = {'User-Agent' : self.user_agent}
		#store the stories, each element is the stories of one page
		self.stories = []
		#boolean flag to set the validation of program's operation
		self.enable = False;

	#get the html code from the input page index
	def getPage(self, pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			#decode the html code into UTF-8
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				print e.code
			if hasattr(e, 'reason'):
				print 'link attempt failed', e.reason
			return None

	#get stories from the pageCode
	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		#page loading failed
		if not pageCode:
			print 'loading page failed'
			return None
		#do regular expression to find the stories
		pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class' + 
							'="content".*?>(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
		items = re.findall(pattern, pageCode)
		#store the stories
		pageStories = []
		#iterate the items to retrieve every story
		for item in items:
			#item[0] is the author of the story, item[1] is the content, item[2] is the image if has any, item[3] is the like numbers
			pageStories.append([item[0].strip(), item[1].strip(), item[3].strip()])
			#use codecs.open(endcoding='utf-8') to directly read and write the file to/from Unicode
			with codecs.open('qiushibaike.txt', 'a', encoding='utf-8') as file:
				copyFile = u'%s\r\n%s\r\n%s\r\n' %(item[0].strip(), item[1].strip(), item[3].strip())
				file.write(copyFile)
		return pageStories

	#load the page and add the content into list
	def loadPage(self):
		#if total number of unread pages is less than 1, load the new page
		if self.enable == True:
			if len(self.stories) < 1:
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	#return a story each time click the "Enter" button
	def getOneStory(self, pageStories, page):
		for story in pageStories:
			input = raw_input()
			if input == "Q":
				self.enable = False
				return
			print u'Page%d\tPublisher:%s\nStory:%s\nLike Numbers:%s\n' %(page, story[0], story[1], story[2])
		#load next page
		input = raw_input()
		if input == "Q":
				self.enable = False
				return
		self.loadPage()

	#start function
	def start(self):
		print u"Loading stories from QiushiBaike, click Enter to get stories, click 'Q' to exit"
		#Enable the program to start
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()
