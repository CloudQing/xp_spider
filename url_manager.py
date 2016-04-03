class Urlmanager():

	def __init__(self):
		self.new_url=set()
		self.old_url=set()


	def add_new_url(self,url):
		if url == None or len(url)==0:
			return 
		if url not in self.new_url and url not in self.old_url:
			self.new_url.add(url)


	def has_new_url(self):
		if len(self.new_url) == 0 :
			return False
		return True

	def add_new_urls(self,urls):
		if urls==None or len(urls)==0:
			return

		for i in urls:
			self.add_new_url(i)


	def get_new_url(self):
		url=self.new_url.pop()
		self.old_url.add(url)
		return url
