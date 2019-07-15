import mysql.connector as mc

mydb = mc.connect(
    host='localhost',
    user='suprateek',
    passwd='mindfire',
    database='blog_in'
)


def insert_into_sessions(user_email):
    """Insert the users required info when the user logs into their account. 

    Args:
        user_email (str): Identifies which info belongs to which user when multiple users are logged in.
    """
    cur = mydb.cursor()
    cur.execute(
        f"insert into sessions_tab(k, value, user_email) values('name',(select first_name from user_info where user_email = '{user_email}'), '{user_email}')")
    mydb.commit()


def delete_after_logout(user_email):
    """Delete the users info when the user logs out.

    Args:
        user_email (str): Email of the user who logs out
    """
    print(user_email)
    cur = mydb.cursor()
    cur.execute(f"delete from sessions_tab where user_email = '{user_email}'")
    mydb.commit()
