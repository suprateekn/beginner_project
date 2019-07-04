import mysql.connector as mc
import uuid

class MysqlFunction:
	"""A class defining functions for all the sql query statements"""
	def __init__(self, host_name,u_name,pwd,db):
		"""Takes arguments as first one being the host name, then the username, then the password and finally the database name(all being strings)
		To create a MysqlCursor class object for every new object created"""
		self.mydb = mc.connect(
			host = host_name,
			user = u_name,
			passwd = pwd,
			database = db
			)


	def create_table(self, table_name, cols):
		"""Takes two arguments one being the table name(string) and the second one being the columns to create(a dictionary having the column name as keys and the description of the keys, i.datatypes and constraints as values)
		Function to create a query for creating a table and returing it. 
		The parameters are the table name and a dictionary that contains the info regarding the column name and the data type"""
		s = "create table " + table_name
		columns = ""
		for k,v in cols.items():
			columns += k + " " + v + ", "

		
		s += "(" + columns[:-2] + ")"
		return s

	def insert_into_table(self, table_name, *cols):
		"""Takes two arguments, first one the table name(string) and the second one being the columns where the vaues is to be inserted(*args)
		Function to create a query string for inserting values into the table and returning the  string.
		This query string is the first parameter of the execute/executemany function"""
		s = "insert into " + table_name + " ("
		column = ""
		place_holder = ""
		for i in range(len(cols)):
			column += cols[i] + ", "
			place_holder += "%s, "
		s += column[:-2] + ") values (" + place_holder[:-2] + ")"
		
		return s


	def delete_from_table(self, table_name):
		"""Takes only one arguent: the table name(string)
		Function to create a query string for deleting from a table. Doesn't return the string but creates a variable(name of the variable is 's') for the object to access
		The other clause(s) can be added by using method chaining of this method with the respective clause methods"""
		self.s = "delete from " + table_name
		return self

	def select_from_table(self, table_name, cols):
		"""Takes two arguments. First one being the table name(string) and the second one being the string of columns"""
		self.s = f"select {cols} from {table_name}"
		return self

	def execute_query(self,s,v = None):
		"""Takes first arg as the sql query string and the second is optional(used for insert operation)
		To execute any query string that is created using other functions"""
		self.mycursor = self.mydb.cursor()
		print(s)
		if v is None:
			self.mycursor.execute(s)
		else :
			self.mycursor.executemany(s,v)	
		
		if s[:6] == "select":
			
			res = self.mycursor.fetchall()
			for x in res :
				print(x)		

	def where_clause(self, col, value):
		"""Takes the first arg as column name(string) and the second arg as value to check(valid type present in the table)
		Function to add the where clause to any mysql statement that calls this method using method chaining
		It doesn't return the string but the variable(name of the variable is 's') is which it is stored is created for the object and can be accessed using the object name"""
		if type(value) is str:
			self.s += f" where {col} = '{value}'"	
		else:
			self.s += f" where {col} = {value}"
		return self

	def group_by(self, col):
		"""Function that takes one argument that has the column string wrt to which we are going to group by. 
		It is used with the help of method chaining with other methods."""
		self.s += f" group by {col}"
		return self

	def order_by(self, col, order = 'asc'):
		"""Function to order the output of the select statement. used with the help of method chaining. 
		Takes two arguments: the column wrt which we have to order by and the order parameter which by default does ascending order"""
		self.s += f" order by {col} {order}"
		

	

c1 = MysqlFunction('localhost', 'suprateekn', 'MINDFIRE', 'mydatabase')
# cols = {
# 	'name' : 'varchar(255)',
# 	'amount' : 'float(8,7)',
# 	'phone' : 'bigint',
# 	'id' : 'binary(16) primary key'
# }
# s = c1.create_table('tb1', cols)
# print(s)

# s = c1.insert_into_table('student', *('id', 'name'))
# trigger_string = "create trigger before_insert_tb1 before insert on tb1 for each row set new.id = unhex(replace(uuid(), '-',''))"
# c1.execute_query(trigger_string)
# val = [(1,"Ajay"),
		# (2,"Bijay")]
# c1.execute_query(s, val)
# c1.delete_from_table('student').where_clause('id',1)
# c1.execute_query(s)

# c1.mydb.commit()

c1.select_from_table('student', "id,count(id)").where_clause('id', 1).group_by('id').order_by('id','desc')
c1.execute_query(c1.s)








