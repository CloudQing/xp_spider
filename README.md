# xp_spider
爬取各大电商网站女性服饰等数据.


spider_main.py  程序入口
  ——html_downloader.py  网页下载器
  —— html_parser.py 页面解析器
  ——Threading.py暂时不用
  
  
html_outputer.py，url_manager.py   还未开发
import_mysql.py   备用数据库导入方案（未使用）

备注：目前只能爬去京东商品（手动录入关键字）
——jd_craw_urls京东商品链接爬虫（只需传入关键字）
——jd_goods_api  从链接池爬去未爬去的商品

数据表为sql.txtss
