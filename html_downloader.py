import urllib2

class Htmldownloader():

	def downloader(self,url):
		if url==None or len(url)==0:
			return

		request=urllib2.Request(url)
		request.add_header('User-Agent','Mozilla/5.0')
		respoense=urllib2.urlopen(request)

		if respoense.getcode() != 200:
			return None
			
		return respoense.read()
