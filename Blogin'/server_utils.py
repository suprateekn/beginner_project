from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import urllib.parse
import requests
import blogin_db_operations as bdo
import sessions_db as sd
from datetime import datetime


def get_query_string(self, content_len):
    """Returns the query string passed with the post request

    Args:
            content_len (int): The length of the query string

    Returns:
            Dict: Dictionary having key_value  pairs of query
    """
    content = urllib.parse.unquote_plus(
        self.rfile.read(content_len).decode("UTF-8"))
    queries_list = content.split("&")
    queries = {}
    for query in queries_list:
        q = query.split("=")
        queries[q[0]] = q[1]
    print(queries)
    return queries


def for_login(queries=None, path = ''):
    """Renders the files for required for login page using render_content()

    Args:
            queries (Dict): Dictionary of query string 

    Returns:
            string: The content to be written to the browser.
    """
    blog_content = ''
    if 'blog' in path:
        blog_id = path.split('blog/')[1]
        u_name = bdo.fetch_from_db('user_name', 'blog_info', 'id', blog_id)
        email = bdo.fetch_from_db('user_email', 'user_info', 'user_name', u_name[0])
        blog_content = bdo.fetch_from_db('title, content', 'blog_info', 'id' ,blog_id)
    elif 'home?' in path:
        user_email = path.split("=")[1]
        email = urllib.parse.unquote(user_email).strip("(),'")
        u_name = bdo.fetch_from_db('user_name', 'user_info', 'user_email', email)
    else:
        u_name = bdo.fetch_from_db('user_name', 'user_info', 'user_email', queries['email'])
        email = queries['email']

    vals = bdo.fetch_multiple_vals_from_db('title, content, date(date), id', 'blog_info', 'user_name', u_name[0])
    response_content = render_content(
        'home.html', user_email=email, user_name = u_name, values = vals, blog_content = blog_content)
    return response_content


def for_signup():
    """Renders the files for required for login page using render_content()

    Returns:
            string: The content to be written to the browser.
    """
    response_content = render_content('signup_successful.html')
    return response_content


def render_content(template,blog_content='', values = '', user_name = '',user_email='', hidden_password_field='hidden', hidden_email_text_field='hidden', hidden_user_name_field='hidden'):
    """Renders the files using jinja2 module

    Args:
            template (.html): The file to be rendered
            hidden_password_field (str): To render the hidden field in the <p> tag of some files
            hidden_email_text_field (str): To render the hidden field in the <p> tag of some files

    Returns:
            string: The content to be written to the browser.
    """
    env = Environment(loader=FileSystemLoader(
        '%s/template/' % "/home/mindfire/Projects/beginner_project/Blogin'"), autoescape=select_autoescape(['html', 'css']))
    temp = env.get_template(template)
    
    response_content = temp.render(values = values, blog_content=blog_content, hidden='hidden',user_name = user_name, user_email=user_email, hidden_password=hidden_password_field,
                                   hidden_email_text=hidden_email_text_field, hidden_user_name=hidden_user_name_field)
    return response_content


def check_pwd_confirm_pwd(self, queries):
    """Checks ifb pwdd and confirm_pwd matches and if not asks the user to re enter.

    Args:
            queries (dict): The dictionary of query strings
    """
    if queries['password'] != queries['confirm_password']:
        content_type = "text/html"
        env = Environment(loader=FileSystemLoader(
            '%s/template/' % "/home/mindfire/Projects/beginner_project/Blogin'"), autoescape=select_autoescape(['html', 'css']))
        temp = env.get_template('signup.html')
        if queries['gender'] == 'MALE':
            response_content = temp.render(first_name=queries['first_name'], last_name=queries['last_name'], user_name=queries['user_name'],
                                           user_email=queries['user_email'], address=queries['address'], MALE='checked', hidden_email_text='hidden', hidden_user_name='hidden')
        else:
            response_content = temp.render(first_name=queries['first_name'], last_name=queries['last_name'], user_name=queries['user_name'],
                                           user_email=queries['user_email'], address=queries['address'], FEMALE='checked', hidden_email_text='hidden', hidden_user_name='hidden')
        write_response(self, response_content)
        return False
    return True


def check_unique(self, queries, attribute, table_name):
    """Checks for unique user_name and email and if not received asks the user for re-entry

    Args:
            queries (dict): The dictionary of query strings
            attribute (string): user_name or email
    """
    print(attribute)
    list_of_all = bdo.get_list(attribute, table_name)

    if queries[attribute] in list_of_all:
        print(queries[attribute])
        if attribute == 'title' or attribute == 'content':
            return False
        else:
            content_type = "text/html"
            env = Environment(loader=FileSystemLoader(
                '%s/template/' % "/home/mindfire/Projects/beginner_project/Blogin'"), autoescape=select_autoescape(['html', 'css']))
            temp = env.get_template('signup.html')
            if attribute == 'user_email':
                if queries['gender'] == 'MALE':
                    response_content = temp.render(first_name=queries['first_name'], last_name=queries['last_name'], user_name=queries['user_name'],
                                                   address=queries['address'], MALE='checked', hidden_password='hidden', hidden_user_name='hidden')
                else:
                    response_content = temp.render(first_name=queries['first_name'], last_name=queries['last_name'], user_name=queries['user_name'],
                                                   address=queries['address'], FEMALE='checked', hidden_password='hidden', hidden_user_name='hidden')
            elif attribute == 'user_name':
                if queries['gender'] == 'MALE':
                    response_content = temp.render(first_name=queries['first_name'], last_name=queries['last_name'], user_email=queries['user_email'],
                                                   address=queries['address'], MALE='checked', hidden_password='hidden', hidden_email_text='hidden')
                else:
                    response_content = temp.render(first_name=queries['first_name'], last_name=queries['last_name'], user_email=queries['user_email'],
                                                   address=queries['address'], FEMALE='checked', hidden_password='hidden', hidden_email_text='hidden')
            write_response(self, response_content)
            return False

    return True


def write_response(self, response_content):
    """Writes the files into browser in byte format

    Args:
            response_content (string): The content to be written on the browser
    """
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write(bytes(response_content, "UTF-8"))
    return