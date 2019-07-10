import mysql.connector as mc
import sessions_db

mydb = mc.connect(
			host = 'localhost',
			user = 'suprateek',
			passwd = 'mindfire',
			database = 'mydatabase'
			)
cur = mydb.cursor()
def inserting(q):

	val = []
	for v in q.values():
		val.append(v)
	val = tuple(val[:-1])
	print(val)
	
	sql = "insert into blogger (name, email, address, gender, password) values (%s, %s, %s, %s, %s)"
	cur.execute(sql, val)
	mydb.commit()

def get_email_id_list():

	cur.execute("select email from blogger")
	res = cur.fetchall()
	r = []
	for x in res:
		r.append(x[0])	
	return r

def check_valid_user(q):
	mydb = mc.connect(
			host = 'localhost',
			user = 'suprateek',
			passwd = 'mindfire',
			database = 'mydatabase'
			)
	cur = mydb.cursor()

	cur.execute("select email from blogger")
	res = cur.fetchall()
	email_list = []
	for x in res:
		email_list.append(x[0])
	cur.execute("select password from blogger")
	res = cur.fetchall()
	pwd_list = []
	for x in res:
		pwd_list.append(x[0])

	val = []
	for v in q.values():
		val.append(v)
	val = tuple(val)
	if val[0] in email_list and val[1] in pwd_list :
		cur.execute(f"select name from blogger where email = '{val[0]}' and password = '{val[1]}'")
		sessions_db.insert_into_sessions(val[0])
		r = cur.fetchall()
		for x in r:
			return f"Welcome {x[0]}!"
	