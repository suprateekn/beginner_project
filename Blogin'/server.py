from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import urllib.parse
import sessions_db
import requests
import server_utils as su
from response.requestHandler import RequestHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.staticHandler import StaticHandler
import os
import blogin_db_operations as bdo


class Server(BaseHTTPRequestHandler):
	
	def do_HEAD(self):
		"""Overridden method of the BaseHTTPRequestHandler class."""
		return

	def do_POST(self): 
		"""Overridden method of the BaseHTTPRequestHandler class that is called when a POST request is made
		"""
		content_len = int(self.headers.get('Content-Length', 0))
		if content_len:
			queries = su.get_query_string(self, content_len)
			print(queries)

		if 'login' in self.path:
			response_content = bdo.check_valid_user(queries)
			su.send_response(self, response_content)

		print(self.path)
		if 'submit' in self.path:
			bdo.inserting(queries)
			response_content = su.for_signup()
			su.send_response(self, response_content)


	def do_GET(self):
		"""Overridden method of the BaseHTTPRequestHandler class that is called when a GET request is made. 
		Transfers the control to the respond method
		"""
		split_path = os.path.splitext(self.path)
		request_extension = split_path[1]

		if request_extension is "" or request_extension is ".html":
			if self.path in routes:
				handler = TemplateHandler()
				handler.find(routes[self.path])
			else:
				handler = BadRequestHandler()
		elif request_extension is ".py":
			handler = BadRequestHandler()
		else:
			handler = StaticHandler()
			handler.find(self.path)


		self.respond({
			'handler': handler
		})

	def handle_http(self, handler):
		"""Overridden method of the BaseHTTPRequestHandler class that is called from the respond() and renders the dynamic and static files and returns them.
		
		Args:
		    handler (Object of requestHandler class): Passes the control to that handler class responsible for handling good(dynamic/static) requests
		    and bad requests 
		
		Returns:
		    TYPE: Byte
		"""
		status_code = handler.getStatus()

		self.send_response(status_code)

		if status_code is 200:
			content = handler.getContents()
			self.send_header('Content-type', handler.getContentType())
		else:
			content = "404 Not Found"

		self.end_headers()

		if isinstance( content, (bytes, bytearray) ):
			return content
			
		return bytes(content, 'UTF-8')

	def respond(self, opts):
		"""Overridden method of the BaseHTTPRequestHandler class which is called from the do_GET() and calls the http_handler()
		and passes the appropriate handler and writes the content into the browser.
		
		Args:
		    opts (dict): Dictionary that  has the handler used for handling the http request
		"""
		response = self.handle_http(opts['handler'])
		self.wfile.write(response)