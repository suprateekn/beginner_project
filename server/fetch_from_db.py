# from mysql_queris.py import MysqlFunction
import mysql.connector as mc
def fetch_name():
	mydb = mc.connect(
			host = 'localhost',
			user = 'suprateekn',
			passwd = 'MINDFIRE',
			database = 'mydatabase'
			)
	cur = mydb.cursor()
	cur.execute("select name from student limit 1")
	res = cur.fetchall()
	return res[0][0]

print(fetch_name())