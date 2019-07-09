import mysql.connector as mc

def inserting(q):
	mydb = mc.connect(
				host = 'localhost',
				user = 'suprateek',
				passwd = 'mindfire',
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

def get_email_id_list():
	mydb = mc.connect(
				host = 'localhost',
				user = 'suprateek',
				passwd = 'mindfire',
				database = 'mydatabase'
				)
	cur = mydb.cursor()
	cur.execute("select email from blogger")
	res = cur.fetchall()
	r = []
	for x in res:
		r.append(x[0])	
	return r