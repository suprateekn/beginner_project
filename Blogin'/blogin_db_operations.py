import mysql.connector as mc
import server_utils as su

mydb = mc.connect(
			host = 'localhost',
			user = 'suprateek',
			passwd = 'mindfire',
			database = 'blog_in'
			)

def inserting(q):
	cur = mydb.cursor()
	val = []
	for v in q.values():
		val.append(v)
	val = tuple(val[:-1])
	print(val)
	
	sql = "insert into user_info (first_name, last_name, user_name, user_email, address, gender, password) values (%s, %s, %s, %s, %s, %s, %s)"
	cur.execute(sql, val)
	mydb.commit()

def get_email_id_list():
	cur = mydb.cursor()
	cur.execute("select email from user_info")
	res = cur.fetchall()
	r = []
	for x in res:
		r.append(x[0])	
	return r

def check_valid_user(q):

	cur = mydb.cursor()

	cur.execute(f"select user_name from user_info where user_email = '{q['email']}' and password = '{q['password']}'")
	res = cur.fetchone()
	if res:
		response_content = su.for_login(q)
		return response_content