"""
tiny.py is a practice project that implements the 
most basic possible web framework in Python.
"""

import re
import cgi

def wsgiref_server(app, host='', port=8080):
	"""Implements a WSGIref server and serves continuously.
	   Can override default host and port if desired."""
	
	from wsgiref.simple_server import make_server

	host_pretty = 'localhost' if host == '' else host
	print 'Starting wsgiref_server at %s:%s' % (host_pretty, port)

	server = make_server(host, port, app)
	server.serve_forever()

def run_app(app):
	"""Runs a given app with a WSGIref server.
	   The server does this by invoking the 'callable' provided by the app.
	   This is to WSGI specs."""

	print 'wsgiref_server is invoking the WSGI callable object.'

	wsgiref_server(app)

# TODO: Routing

def index():
	return 'Home'

# FIX: Better URL handling

URLS = {
	'/index': index,
	'/': index,
	'/user': user
}

# FIX: Implement requests most stably/generalizably (likely in a class).
# TODO: Add handling of POST (and other) requests.

def request_handler(environ, start_response):
	"""The simplest request handler possible. This runs when the client makes
	   a request. The server has gotten the environ dictionary from the client
	   when the client made the request and is passing it to the request handler
	   for parsing and handling the request. The server also provides the
	   start_response function which is called below."""

	request.bind(environ)

	# URL Routing
	# if path not in URLS:
	# 	# Status, headers represent the HTTP response expected by the client.
	# 	status = '404 NOT FOUND'

	# 	# Important that this remains a list as specified by WSGI specs.
	# 	headers = [('Content-type', 'text/plain')]

	# 	# start_response is used to begin the HTTP response.
	# 	# This sends the response headers to the server, which sends to the client.
	# 	start_response(status, headers)
		
	# 	return ['Not found']
	# else:
	# 	# Status, headers represent the HTTP response expected by the client.
	# 	status = '200 OK'

	# 	# Important that this remains a list as specified by WSGI specs.
	# 	headers = [('Content-type', 'text/html')]
		
	# 	# start_response is used to begin the HTTP response.
	# 	# This sends the response headers to the server, which sends to the client.
	# 	start_response(status, headers)

	# 	if post_data:
	# 		content = URLS[path](post_data)
	# 	elif queries_data:
	# 		content = URLS[path](post_data)
	# 	else:
	# 		content = URLS[path]()
	# 	return [content]

class Request(object):
	"""Represents a request object. It is initialized upon starting the app.
	   When a user makes a request, it will bind user's request information
	   (environment, queries, post data) to the request object so that it can
	   be used elsewhere."""

	def bind(self, environ):
		"""Binds the request object to the user's request data."""

		self.environ = environ
		self.path = self.environ.get('PATH_INFO', '/')
		self.path = '/' + self.path if not self.path[0] == '/' else self.path
		self.method = self.environ.get('REQUEST_METHOD', '').upper()
		self.get_data = None
		self.post_data = None

		if self.method == 'GET':
			self.get_data = self.get()
		elif self.method == 'POST':
			self.post_data = self.post()

	def get(self):
		"""Parses the query string of a get request and returns it in 
		   a dictionary."""

		form = cgi.FieldStorage(fp=self.environ.get('wsgi.input'), environ=self.environ)
		get_dict = {key: form.getvalue(key) for key in form.keys()}
		return get_dict

	def post(self):
		"""Parses the data of a post request and returns it in a dictionary."""

		form = cgi.FieldStorage(fp=self.environ.get('wsgi.input'), environ=self.environ)
		post_dict = {key: form.getvalue(key) for key in form.keys()}
		return post_dict

request = Request()

# TODO: Response

# TODO: Headers

# TODO: Error handling

if __name__ == '__main__':
	run_app(request_handler)