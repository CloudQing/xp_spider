class Htmloutputer():

	def __init__(self):
		self.datas=[]


	def collect_data(self,data):
		if data is None:
			return
		self.datas.append(data)

	def Htmloutput(self):
		fout=open("test.txt",'w')
		for i in self.datas:
			keys=[]
			values=[]

			for key,value in i.items():
				keys.append(key)
				values.append("\'"+value+"\'")

			keys=','.join(keys)
			values=','.join(values)
			fout.write('INSERT yun(%s) VALUES(%s);\n' % (keys,values))
		fout.close()
