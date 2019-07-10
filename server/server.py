from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
# import fetch_from_db
import urllib.parse
import blogger_db_operation as bdo
from login_sessions import login_fn
import sessions_db

class Server(BaseHTTPRequestHandler):
	def do_HEAD(self):
		return

	def do_POST(self):
		print(self.requestline)
		content_len = int(self.headers.get('Content-Length', 0))
		if content_len:
			content = urllib.parse.unquote_plus(self.rfile.read(content_len).decode("UTF-8"))
			queries_list = content.split("&")
			queries = {}
			for query in queries_list:
				q = query.split("=")
				queries[q[0]] = q[1]
				
			print(queries)
			print(type(self.path))
		# if queries['password'] != queries['confirm_password'] :
		# 	content_type = "text/html"
		# 	env = Environment(loader=FileSystemLoader('%s/template/' % '/home/mindfire/Projects/beginner_project/server'), autoescape = select_autoescape(['html','css']))
		# 	temp = env.get_template('index.html')
		# 	if queries['gender'] == 'MALE':
		# 		response_content = temp.render(name = queries['name'], email = queries['email'], address = queries['address'], MALE = 'checked', hidden_email_text = 'hidden')
		# 	else:
		# 		response_content = temp.render(name = queries['name'], email = queries['email'], address = queries['address'], FEMALE = 'checked', hidden_email_text = 'hidden')
		# 	self.send_response(200)
		# 	self.send_header('Content-type', content_type)
		# 	self.end_headers()
		# 	self.wfile.write(bytes(response_content, "UTF-8"))

		# email_list = bdo.get_email_id_list()
		# print(email_list)
		# if queries['email'] in email_list:
		# 	content_type = "text/html"
		# 	env = Environment(loader=FileSystemLoader('%s/template/' % '/home/mindfire/Projects/beginner_project/server'), autoescape = select_autoescape(['html','css']))
		# 	temp = env.get_template('index.html')
		# 	if queries['gender'] == 'MALE':
		# 		response_content = temp.render(name = queries['name'],  address = queries['address'], MALE = 'checked', hidden_password = 'hidden')
		# 	else:
		# 		response_content = temp.render(name = queries['name'],  address = queries['address'], FEMALE = 'checked', hidden_password = 'hidden')
		# 	self.send_response(200)
		# 	self.send_header('Content-type', content_type)
		# 	self.end_headers()
		# 	self.wfile.write(bytes(response_content, "UTF-8"))			

		
		# bdo.inserting(queries)
		# login_fn()

			login_msg = bdo.check_valid_user(queries)
		content_type = "text/html"
		env = Environment(loader=FileSystemLoader('%s/template/' % '/home/mindfire/Projects/beginner_project/server'), autoescape = select_autoescape(['html','css']))
	
		temp = env.get_template('logout.html')
		response_content = temp.render()
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(bytes(response_content, "UTF-8"))
		# sessions_db.delete_after_logout()

	def do_GET(self):
		url = self.path.split("?")
		if url:
			queries = url[0]
			print(queries)
			self.respond()

	def get(self):
		pass

	def handle_http(self):
		status = 200
		content_type = "text/plain"
		response_content = ""
		print(type(self.path))

		if self.path in routes:
			# print(routes[self.path])
			url = "localhost:8004/"
			route_content = routes[self.path]['template']
			filepath = Path("template/{}".format(route_content))
			print(filepath.is_file())
			if filepath.is_file():
				content_type = "text/html"
				env = Environment(loader=FileSystemLoader('%s/template/' % '/home/mindfire/Projects/beginner_project/server'), autoescape = select_autoescape(['html','css']))
				# temp = env.get_template('index.html')
				temp = env.get_template(routes[self.path]['template'])
				response_content = temp.render(hidden_password = 'hidden', hidden_email_text = 'hidden')

				
			else:
				content_type = "text/plain"
				response_content = "404 NOT FOUND"

		else :
			content_type = "text/plain"
			response_content = "404 NOT FOUND"

		self.send_response(status)
		self.send_header('Content-type', content_type)
		self.end_headers()

		return bytes(response_content, "UTF-8")

	def respond(self):
		content = self.handle_http()
		self.wfile.write(content)
		