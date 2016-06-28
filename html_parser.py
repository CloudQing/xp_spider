#coding=UTF-8
import bs4,re,urlparse,MySQLdb

class Htmlparser():


        '''
        @db     数据库类对象
        '''
        def jd_url_parser(self,html_cont,db):
                if html_cont is None:
                        return None
                links=re.findall(r"//item\.jd\.com/[0-9]+\.html#",html_cont)
                for link in links:
			check_sql="url='%s'" % link
			link=link.replace('#','')
                        if not db.check('xp_jd_urls',check_sql):
                                sql=db.insert('xp_jd_urls',link,0)
        
                       
        def jd_item_parser(self,html_cont):
                if html_cont is None:
                        return None
                soup=bs4.BeautifulSoup(html_cont,'lxml',from_encoding='utf-8')
		try:
                	img='http:'+str(soup.find('img',class_='img-hover')['src'])
			name=str(soup.find('img',class_='img-hover')['alt'])
		except:
			img='http:'+str(soup.find('li',class_='img-hover').img['src'])
			name=str(soup.find('li',class_='img-hover').img['alt'])
		print 'url:'+name
                return img,name

        def img_parser(self,html_cont,file):
                try:
                        file=open(file,'w')
                except:
                        print '文件打开失败'
                        return False
                try:
                        file.write(html_cont)
                except:
                        print '图片写入失败'
                        return False
                file.close()



        def tags_filter(self,str):
                tar=re.findall(r'<\S+?>',str)
                for i in range(len(tar)):
                        str=str.replace(tar[i],'')
                return str

        def quote_buffer(self,buf):  
                    """ 
                    chinese to mysql 
                    """  
                    retstr = ''.join(map(lambda c:'%02x'%ord(c), buf))  
                    retstr = "x'" + retstr + "'"  
                    return retstr



