#coding=UTF-8
import threading

class jd_Threadings(threading.Thread):
	def __init__(self,keyword,id,obj):
		#threading.Thread.__init__(self)
		super(jd_Threadings,self).__init__()
		self.keyword=keyword
		self.id=id
		self.obj=obj
		self.lock=threading.Lock()
		
	def run(self):
		self.lock.acquire()
		print '%d : 正在爬取%s类.' % (self.id,self.keyword)
		self.obj.jd_craw_urls(self.keyword)
		self.lock.release()

