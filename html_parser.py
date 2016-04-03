#coding=UTF-8
import bs4,re,urlparse

class Htmlparser():

        def parser(self,html_cont,url):
                if html_cont is None:
                        return None
                soup=bs4.BeautifulSoup(html_cont,'html.parser',from_encoding='utf8')
                new_urls=self.__get_new_urls(soup)
                new_data=self.__get_new_data(html_cont,url)
                return new_urls,new_data

        '''
        @db     数据库类对象
        '''
        def jd_url_parser(self,html_cont,db):
                if html_cont is None:
                        return None
                links=re.findall(r"//item\.jd\.com/[0-9]+\.html",html_cont)
                for link in links:
			check_sql="url='%s'" % link
                        if not db.check('xp_jd_urls',check_sql):
                                db.insert('xp_jd_urls',link,0)
                        


        def __get_new_urls(self,soup):
                new_urls=set()
                links=soup.find_all('a',href=re.compile(r"/contents/XueYuanFengCai/ynusei\S+\.html"))

                for link in links:
                        new_url=urlparse.urljoin('http://www.sei.ynu.edu.cn',link['href'])
                        new_urls.add(new_url)

                return new_urls

        def __get_new_data(self,html_cont,url):
                res_data={}
                searchObj=re.search(r"<div class=\"title\">[\s\S\u4e00-\u9fa5]+<br />[\s\S]*<span class=\"titledetail\">",html_cont)
                result=searchObj.group()
                for i in ['<div class="title">','<br />','<span class="titledetail">']:
                        result=result.replace(i,'')
		res_data['url']=url
                res_data['title']=result.strip()
                return res_data
