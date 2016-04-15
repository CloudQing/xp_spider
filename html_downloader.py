#coding=UTF-8
import urllib2,demjson

class Htmldownloader():

	def downloader(self,url):
		if url==None or len(url)==0:
			return

		try:
			respoense=urllib2.urlopen(url)
		except:
			print '链接无法打开!'
		if respoense.getcode() != 200:
			return None
			
		return respoense.read()

	def json(self,api,*vars):
                url=api % vars;
                return demjson.decode(self.downloader(url))
