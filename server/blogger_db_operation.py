import mysql.connector as mc

def inserting(q):
	mydb = mc.connect(
				host = 'localhost',
				user = 'suprateekn',
				passwd = 'MINDFIRE',
				database = 'mydatabase'
				)
	cur = mydb.cursor()
	val = []
	for v in q.values():
		val.append(v)
	val = tuple(val[:-1])
	print(val)
	
	sql = "insert into blogger (name, email, address, gender, password) values (%s, %s, %s, %s, %s)"
	cur.execute(sql, val)
	mydb.commit()