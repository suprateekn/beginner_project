from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
# import fetch_from_db
import urllib.parse
import blogger_db_operation as bdo

class Server(BaseHTTPRequestHandler):
	def do_HEAD(self):
		return

	def do_POST(self):
		print(self.requestline)
		content_len = int(self.headers.get('Content-Length'))
		content = urllib.parse.unquote_plus(self.rfile.read(content_len).decode("UTF-8"))
		queries_list = content.split("&")
		queries = {}
		for query in queries_list:
			q = query.split("=")
			queries[q[0]] = q[1]
			
		print(queries)
		if queries['password'] == queries[confirm_password]:
			bdo.inserting(queries)
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(bytes("<html><body>Thanks</body></html>", "UTF-8"))

	def do_GET(self):
		self.respond()

	def handle_http(self):
		status = 200
		content_type = "text/plain"
		response_content = ""

		if self.path in routes:
			print(routes[self.path])
			url = "localhost:8004/"
			route_content = routes[self.path]['template']
			filepath = Path("template/{}".format(route_content))
			print(filepath.is_file())
			if filepath.is_file():
				content_type = "text/html"
				env = Environment(loader=FileSystemLoader('%s/template/' % '/home/suprateek/Projects/beginner_project/server'), autoescape = select_autoescape(['html','css']))
				temp = env.get_template('index.html')
				response_content = temp.render()
				# name_from_db = fetch_from_db.fetch_name()
				# response_content = (temp.render(name = name_from_db))
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
		