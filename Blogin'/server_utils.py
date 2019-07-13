from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import urllib.parse
import sessions_db
import requests
import blogin_db_operations as bdo

def get_query_string(self, content_len):
	"""Returns the query string passed with the post request
	
	Args:
	    content_len (int): The length of the query string
	
	Returns:
	    Dict: Dictionary having key_value  pairs of query
	"""
	content = urllib.parse.unquote_plus(self.rfile.read(content_len).decode("UTF-8"))
	queries_list = content.split("&")
	queries = {}
	for query in queries_list:
		q = query.split("=")
		queries[q[0]] = q[1]
	return queries

def for_login(queries):
	"""Renders the files for required for login page using render_content()
	
	Args:
	    queries (Dict): Dictionary of query string 
	
	Returns:
	    string: The content to be written to the browser.
	"""
	response_content = render_content('logout.html')
	return response_content

def for_signup():
	"""Renders the files for required for login page using render_content()
	
	Returns:
	    string: The content to be written to the browser.
	"""
	response_content = render_content('signup_successful.html')
	return response_content

def render_content(template, hidden_password_field = '', hidden_email_text_field = ''):
	"""Renders the files using jinja2 module
	
	Args:
	    template (.html): The file to be rendered
	    hidden_password_field (str): To render the hidden field in the <p> tag of some files
	    hidden_email_text_field (str): To render the hidden field in the <p> tag of some files
	
	Returns:
	    string: The content to be written to the browser.
	"""
	env = Environment(loader=FileSystemLoader('%s/template/' % '/home/mindfire/Projects/Blog_in/'), autoescape = select_autoescape(['html','css']))
	temp = env.get_template(template)	
	response_content = temp.render(hidden_password = hidden_password_field, hidden_email_text = hidden_email_text_field)
	return response_content

def check_pwd_confirm_pwd(queries):
	"""Checks ifb pwdd and confirm_pwd matches and if not asks the user to re enter.
	
	Args:
	    queries (dict): The dictionary of query strings
	"""
	if queries['password'] != queries['confirm_password'] :
		content_type = "text/html"
		env = Environment(loader=FileSystemLoader('%s/template/' % '/home/mindfire/Projects/beginner_project/server'), autoescape = select_autoescape(['html','css']))
		temp = env.get_template('signup.html')
		if queries['gender'] == 'MALE':
			response_content = temp.render(name = queries['name'], email = queries['email'], address = queries['address'], MALE = 'checked', hidden_email_text = 'hidden')
		else:
			response_content = temp.render(name = queries['name'], email = queries['email'], address = queries['address'], FEMALE = 'checked', hidden_email_text = 'hidden')
		self.send_response(200)
		self.send_header('Content-type', content_type)
		self.end_headers()
		self.wfile.write(bytes(response_content, "UTF-8"))

def check_unique(queries,attribute):
	"""Checks for unique user_name and email and if not received asks the user for re-entry
	
	Args:
	    queries (dict): The dictionary of query strings
	    attribute (string): user_name or email
	"""
	list_of_all = bdo.get_list()
	print(list_of_all)
	if queries[attribute] in list_of_all:
		content_type = "text/html"
		env = Environment(loader=FileSystemLoader('%s/template/' % '/home/mindfire/Projects/beginner_project/server'), autoescape = select_autoescape(['html','css']))
		temp = env.get_template('signup.html')
		if queries['gender'] == 'MALE':
			response_content = temp.render(name = queries['name'],  address = queries['address'], MALE = 'checked', hidden_password = 'hidden')
		else:
			response_content = temp.render(name = queries['name'],  address = queries['address'], FEMALE = 'checked', hidden_password = 'hidden')
		self.send_response(200)	
		self.send_header('Content-type', content_type)
		self.end_headers()
		self.wfile.write(bytes(response_content, "UTF-8"))		

def send_response(self, response_content):
	"""Writes the files into browser in byte format
	
	Args:
	    response_content (string): The content to be written on the browser
	"""
	self.send_response(200)
	self.send_header('Content-type', 'text/html')
	self.end_headers()
	self.wfile.write(bytes(response_content, "UTF-8"))