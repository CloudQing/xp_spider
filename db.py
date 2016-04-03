#coding=UTF-8
import MySQLdb
'''

*db.py数据库操作类
@lastmodify 2016-4-19

'''
class database():

	'''
		@addr 		数据库地址
		@use 		数据库用户名
		@pwd    	数据库密码
		@database   数据库名
	'''

        def __init__(self,user,pwd,database,addr='localhost'):
                self.db=MySQLdb.connect(addr,user,pwd,database)
                self.cursor=self.db.cursor()

        '''
		*关闭数据库
        '''
        def close(self):
                return self.db.close()

        '''
		*查询数据信息
		@table    数据表名称
		@where    查询条件
		@cols     需要查询字段
        '''
        def get(self,table,where=None,cols='*'):
                if where != None:
                        sql = 'SELECT %s FROM %s WHERE %s' % (cols,table,where)
                else:
                        sql = 'SELECT %s FROM %s' % (cols,table)
                self.cursor.execute(sql)
                return self.cursor.fetchall()

        '''
		**插入数据
		@table    数据表名
		@*values  插入的数据（所有除了自增字段外的字段）
        '''
        def insert(self,table,*values):
                self.cursor.execute('SHOW COLUMNS FROM %s' % table)
                self.cols=self.cursor.fetchall()
                self.temp=list()
                for i in self.cols[1:]:
                        self.temp.append(i[0])
                self.cols=str(tuple(self.temp)).replace('\'','')
                sql='INSERT %s%s VALUES %s' % (table,self.cols,str(values))
                try:
                        self.cursor.execute(sql)
                        self.db.commit()
                except:

                        return False

        '''
		**删除数据
		@table    数据表名
		@where    DELETE删除条件
        '''
        def delect(self,table,where):
                sql='DELETE FROM %s WHERE %s' % (table,where)
                print sql
                try:
                        self.cursor.execute(sql)
                        self.db.commit()
                except:
                        return False

        '''
		**检查数据
		@where检查条件
        '''
        def check(self,table,where):
                sql='SELECT * FROM %s WHERE %s' % (table,where)
                if self.cursor.execute(sql) == 1:
                        return True
                return False

        
