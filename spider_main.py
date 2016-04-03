#!/usr/bin/python2.6
#coding=UTF-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append('/root/python/')
from spider import html_downloader,html_parser,html_outputer,url_manager,db,Threading
class Spider():

        def __init__(self):
                self.db=db.database('root','beibei','xueping')
        	self.urlmanager=url_manager.Urlmanager()
                self.downloader=html_downloader.Htmldownloader()
                self.parser=html_parser.Htmlparser()
                self.outputer=html_outputer.Htmloutputer()

        def craw(self,url):
                        self.count = 0
                        self.urlmanager.add_new_url(url)
                        while self.urlmanager.has_new_url():
                                url=self.urlmanager.get_new_url()
                                print 'craw %d : %s' % (self.count,url)
                                html_cont=self.downloader.downloader(url)
                                new_urls,new_data = self.parser.parser(html_cont,url,self.db)
                                self.urlmanager.add_new_urls(new_urls)
                                self.outputer.collect_data(new_data)

                                self.count += 1



        def jd_craw_urls(self,keyword,api='http://search.jd.com/Search?keyword=%s&enc=utf-8&page=%d'):
                        for i in range(1,201):
                                url=api % (keyword,i)
        			print '正在爬取第 %d 页: %s' % (i,url)
        			html_cont=self.downloader.downloader(url)
        			self.parser.jd_url_parser(html_cont,self.db)

                                

if __name__=='__main__':
        obj_spider=Spider()
        keywords=list()
        threads=list()
        while 1:
                try:
                        num=input('需要查询的类型个数：\n')
                        break
                except:
                        print '输入格式错误，请重新输入!'
        for i in range(num):
                keyword=raw_input('请输入查询关键字:\n')
                keywords.append(keyword)
                try:
                        threads.append(Threading.jd_Threadings(keywords[i],i,obj_spider))
                        print '%d线程创建成功' % (i+1)
                except:
                        print '%d线程创建失败' % (i+1)
        for i in range(num):
                try:
                        threads[i].start()
                        print '%d线程启动成功' % (i+1)
                except:
                        print '%d线程启动失败' % (i+1)

