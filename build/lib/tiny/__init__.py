"""
tiny.py is a practice project that implements the 
most basic possible web framework in Python.
"""

# cgi used for form parsing; inspect used for argument counting for routing.
import cgi, inspect

class TinyApp(object):
	"""Represents an app created by the user.
	   Holds the data and functionality needed by the user to create
	   a simple app."""

	def __init__(self):
		"""Initializes the app object with an empty dict of routes."""

		self.ROUTES = {}

	def add_route(self, route, handler, methods=['GET']):
		"""Adds a function to the app's routing dict.
		   Handler - function defined by the user that creates a response."""

		self.ROUTES[route] = (handler, methods)

	def route(self, route, **kwargs):
		"""Decorator for add_route."""

		def wrapper(handler):
			self.add_route(route, handler, **kwargs)
			return handler
		return wrapper

	### Request Handlers ###

	def request_handler(self, environ, start_response):
		"""When the client makes a request, the server gets the environ w/ the
		   request and passes it here. The handler uses the environ data to craft
		   a response and send it back to the server using the start_response
		   function, which is provided by the server."""

		request = TinyRequest(environ)

		action = self.ROUTES[request.path]

		# URL Routing
		# TODO: Move this into its own function/method
		if request.path not in self.ROUTES or request.method not in action[1]:
			# Status, headers represent the HTTP response expected by the client.
			status = '404 NOT FOUND'

			# Important that this remains a list as specified by WSGI specs.
			headers = [('Content-type', 'text/plain')]

			# start_response is used to begin the HTTP response.
			# This sends the response headers to the server, which sends to the client.
			start_response(status, headers)
			
			# TODO: Don't determine this here; use the URL routing/error handling to do this.
			return ['Not found']
		else:
			action_fun = action[0]

			# Store num of arguments in the handler function.
			arg_num = len(inspect.getargspec(action_fun)[0])

			# If there aren't any arguments, don't pass the get_data dict to it.
			if arg_num == 0:
				response = action_fun()
			else:
				response = action_fun(request)
			
			# Sends the start of the response to the server, which sends it to the client.
			start_response(response.status, response.headers)

			# Sends the body of the response (usually, the html) to the server.
			return [response.body]

	def __call__(self, environ, start_response):
		"""Makes the user's app a WSGI application. It is now callable by
		   a WSGI server."""

		return self.request_handler(environ, start_response)

### Request and Response Classes ###

class TinyRequest(object):
	"""Represents a request object. An empty one is created upon starting the app.
	   When a user makes a request, it will bind user's request information
	   (environment, queries, post data) to the request object so that it can
	   be used elsewhere."""

	def __init__(self, environ):
		"""Binds the request object to the user's request data."""

		self.environ = environ
		self.path = self.environ.get('PATH_INFO', '/')

		# Standardizes path slashes.
		self.path = '/' + self.path if not self.path[0] == '/' else self.path

		# Standardizes request methods.
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

class TinyResponse(object):
	"""Represents a request object. It is initialized upon starting the app.
	   When a user makes a request, the app will formulate the response based
	   on the request data. Tiny will bind that response data to an object of
	   this class."""

	def __init__(self, body, status='200 OK', headers=[('Content-Type', 'text/html')]):
		"""Creates a response object that can hold the data for the HTTP response.
		   Defaults to a '200 OK' response with HTML content but allows user to 
		   override."""
		
		self.body = body
		self.status = status
		self.headers = headers


# TODO: HTTP/WSGI Headers


# TODO: Error handling


### Server and run script ###

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