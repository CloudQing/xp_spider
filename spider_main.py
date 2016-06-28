#!/usr/bin/python2.6
#coding=UTF-8
import sys,re,time
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append('/root/python/')
from spider import html_downloader,html_parser,db
import time
class Spider():

        def __init__(self):
                self.db=db.database('root','beibei123','xueping')
                self.downloader=html_downloader.Htmldownloader()
                self.parser=html_parser.Htmlparser()



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
                                self.jd_craw_good(url)
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
		print img
                img=self.img_craw_urls(img)
                url=url.replace('http:','')
                self.db.insert('xp_jd_goods',id,name.encode('utf-8'),int(float(price)),url.encode('utf-8'),int(comment),int(comments),img)

        def img_craw_urls(self,url):
                html_cont=self.downloader.downloader(url)
		try:
                	filename=re.findall(r'/[^/]*.jpg',url)[0]
		except:
			filename=re.findall(r'/[^/]*.png',url)[0]
                name=filename
                filename='img'+filename
                self.parser.img_parser(html_cont,filename)
                return name

        def vip_craw_urls(self):
                api='http://category.vip.com/search-5-0-%d.html?q=3|30036||&rp=30074|30063#catPerPos'

                for i in range(1,21):
                        f=open('vip_urls_sql.txt','a')
                        url=api % i
                        print '正在爬取第%d页' % i
                        req=urllib2.Request(url)
                        response=urllib2.urlopen(req)
                        links=re.findall(r'http://www\.vip\.com/detail-[0-9]+-[0-9]+\.html',response.read())
                        for link in set(links):
                                sql='INSERT xp_vip_urls(url) VALUes(\'%s\')\n' % link
                                f.write(sql)
                        f.close()
                

        def vip_craw_goods(self):

                #url='http://www.vip.com/detail-765237-107551024.html'
                f1=open('vip_urls_sql.txt','r')
		f2=open('vip_goods_sql.txt','a')
		while f.readline():
			url=f1.readline()
                	browser=webdriver.PhantomJS()
                	browser.get(url)

                	name=browser.title
			 print 'name:%s' % name
	
        	        #type=browser.find_element_by_tag_name("td")[5]
        	        #print 'type:%s' % type.text

        	        n_price=browser.find_element_by_css_selector("em[class=\"J-price\"]")
        	        print 'n_price:%s' % n_price.text

        	        o_price=browser.find_element_by_css_selector("del[class=\"J-mPrice\"]")
        	        print 'o_price:%s' % o_price.text

                	discount=browser.find_element_by_css_selector("span[class=\"pbox-off J-discount\"]")
			print 'discount:%s' % discount.text

                	sql='INSERT xp_vip_goods(name,o_price,n_price,url) VALUES(\'%s\',\'%s\',\'%s\',\'%s\')\nUPDATE xp_vip_urls SET name=%s WHERE url=%s\n' %(name,o_price,n_price,url,name,url)
                	f2.write(sql)
			browser.quit()











        def tb_craw_urls(self,kw):

                #kw='裙子'
                f=open('tb_urls_sql.txt','a')
                url='http://s.taobao.com/search?q=%s&ie=utf8' % kw
                req=urllib2.Request(url)
                response=urllib2.urlopen(req)
                ids=re.findall(r'\"[0-9]{11,12}\"',response.read())
                ids=set(ids)
                ids=list(ids)
                for i in ids:
                        t=i.replace('"','')
                        link='https://detail.tmall.com/item.htm?id=%s' % t
                        sql='INSERT xp_tb_urls(url) VALUes(\'%s\')\n' % link
                        f.write(sql)
                f.close()


        def tb_craw_goods(self):
                f=open('tb_goods_sql.txt','a')
                url='https://detail.tmall.com/item.htm?id=38482025385'
                browser=webdriver.PhantomJS()
                browser.get(url)
                try:
                        pop=browser.find_element_by_css_selector('span[id=\"J_CollectCount\"]')
                        pri=browser.find_element_by_css_selector('span[class=\"tm-price\"]')
                except:
                        pass
                try:
                        pop=browser.find_element_by_css_selector('em[class=\"J_FavCount\"]')
                        pri=browser.find_element_by_css_selector('em[class=\"tb-rmb-num\"]')

                except:
                        pass
                '''
                print '名称:'+browser.title
                print '价格:'+pri.text
                print '人气:'+pop.text
                '''
                sql='INSERT xp_vip_goods(name,price,url,popularity) VALUES(\'%s\',\'%s\',\'%s\,\'%s\'')\nUPDATE xp_tb_urls SET name=%s WHERE url=%s\n' %(name,price,url,pop,name,url)
                f.write(sql)
                f.close()
                browser.quit()




if __name__=='__main__':
        obj_spider=Spider()
	obj_spider.jd_goods_api()

