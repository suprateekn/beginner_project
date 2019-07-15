import mysql.connector as mc
import server_utils as su
import sessions_db as sd
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

mydb = mc.connect(
    host='localhost',
    user='suprateek',
    passwd='mindfire',
    database='blog_in'
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


def get_list(attribute):
    cur = mydb.cursor()
    cur.execute(f"select {attribute} from user_info")
    res = cur.fetchall()
    r = []
    for x in res:
        r.append(x[0])
    return r


def check_valid_user(q):

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
