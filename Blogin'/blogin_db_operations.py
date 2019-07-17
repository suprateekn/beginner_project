import mysql.connector as mc
import server_utils as su
import sessions_db as sd
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

mydb = mc.connect(
    host='localhost',
    user='suprateek',
    passwd='mindfire',
    database='blog_in'
)


def inserting(q):
    """Inserts the values into the user_info table
    
    Args:
        q (dict): Dict of query strings containing the user_info during sign up as key val pairs
    """
    cur = mydb.cursor()
    val = []
    for v in q.values():
        val.append(v)
    val = tuple(val[:-1])
    print(val)

    sql = "insert into user_info (first_name, last_name, user_name, user_email, address, gender, password) values (%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql, val)
    mydb.commit()


def get_list(attribute):
    """Get the list of all the rows of the specified column from the user_info table
    
    Args:
        attribute (str): Column name whose list has to be fetched
    
    Returns:
        list : list of all the rows of the specified col
    """
    cur = mydb.cursor()
    cur.execute(f"select {attribute} from user_info")
    res = cur.fetchall()
    r = []
    for x in res:
        r.append(x[0])
    return r


def check_valid_user(q):
    """Checks whether the credentials entered by the user during login are valid or not and if not asks for re enter
    
    Args:
        q (dict): Dict containing the email and password of the user trying to login
    
    Returns:
        str: The response content to be written into the server.
    """
    cur = mydb.cursor()

    cur.execute(
        f"select user_name from user_info where user_email = '{q['email']}' and password = '{q['password']}'")
    res = cur.fetchone()
    if res:
        response_content = su.for_login(q)
        sd.insert_into_sessions(q['email'])
        return response_content

    else:
        env = Environment(loader=FileSystemLoader(
            '%s/template/' % "/home/mindfire/Projects/beginner_project/Blogin'"), autoescape=select_autoescape(['html', 'css']))
        temp = env.get_template("login.html")
        response_content = temp.render(hidden='')
        return response_content

def fetch_from_db(col, tab_name, where_attr, val):
    """Fetch the desired column of the user logged in.
    
    Args:
        col (str): can be a single column name or a coma separated str of columns
        user_email (str): A unique key that will be put in the where clause to search for the name.
    
    Returns:
        str: Desired column of the user logged in
    """
    cur = mydb.cursor()
    cur.execute(f"select {col} from {tab_name} where {where_attr} = '{val}'")   
    res = cur.fetchone() 

    
    return res

def fetch_multiple_vals_from_db(col, tab_name, where_attr, val):
    """Fetch the desired column of the user logged in.
    
    Args:
        col (str): can be a single column name or a coma separated str of columns
        user_email (str): A unique key that will be put in the where clause to search for the name.
    
    Returns:
        str: Desired column of the user logged in
    """
    cur = mydb.cursor()
    cur.execute(f"select {col} from {tab_name} where {where_attr} = '{val}'")   
    res = cur.fetchall() 

    
    return res    

def insert_into_blog_info(q):
    cur = mydb.cursor()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    sql = "insert into blog_info (title, content, user_name, date) values (%s, %s, %s, %s)"
    val = []
    for v in q.values():
        val.append(v)
    val = val[:-1]
    val.append(formatted_date)
    val = tuple(val)
    cur.execute(sql, val)
    mydb.commit()