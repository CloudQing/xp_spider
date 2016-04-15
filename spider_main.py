#!/usr/bin/python2.6
#coding=UTF-8
import sys,re,time
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append('/root/python/')
from spider import html_downloader,html_parser,html_outputer,db,Threading
import time
class Spider():

        def __init__(self):
                self.db=db.database('root','beibei','xueping')
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


        def jd_goods_api(self):
                        r=self.db.get('xp_jd_urls','old=0')
                        for i in range(len(r)):
                                db_url=r[i][1]
                                url='http:'+r[i][1]
				try:
                                	self.jd_craw_good(url)
				except:
					continue
                                where='url=\''+db_url+"'"
                                self.db.url_update('xp_jd_urls','old',1,where)

        def jd_craw_good(self,url):
                result=list()
                price_json_api='http://p.3.cn/prices/mgets?skuIds=J_%d'      #价格json入口
                comment_json_api='http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=%d'        #评论json入口

                id=int(re.findall('[0-9]+',url)[0])
                print '正在爬商品:%d' % id
                comment_obj=self.downloader.json(comment_json_api,id)
                html_cont=self.downloader.downloader(url)

                img,name=self.parser.jd_item_parser(html_cont)
                price=self.downloader.json(price_json_api,id)[0]['p']
                comment=comment_obj['CommentsCount'][0]['GoodRateShow']
                comments=comment_obj['CommentsCount'][0]['CommentCount']
                img=self.img_craw_urls(img)
                url=url.replace('http:','')
                self.db.insert('xp_jd_goods',id,name.encode('utf-8'),int(float(price)),url.encode('utf-8'),int(comment),int(comments),img)

        def img_craw_urls(self,url):
                html_cont=self.downloader.downloader(url)
                filename=re.findall(r'/[^/]*.jpg',url)[0]
                name=filename
                filename='img'+filename
                self.parser.img_parser(html_cont,filename)
                return name





if __name__=='__main__':
        obj_spider=Spider()
	obj_spider.jd_goods_api()
	obj_spider.db.close()

