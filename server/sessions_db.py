import mysql.connector as mc

mydb = mc.connect(
			host = 'localhost',
			user = 'suprateek',
			passwd = 'mindfire',
			database = 'mydatabase'
				)
cur = mydb.cursor()

def insert_into_sessions(user_email):
	cur.execute(f"insert into sessions_tab(k, value, user_email) values('name',(select name from blogger where email = '{user_email}'), '{user_email}')")
	mydb.commit()