"""
tiny.py is a practice project that implements the 
most basic possible web framework in Python.
"""

# cgi used for form parsing; inspect for argument counting for routing; os for template directory; re for template rendering.
import cgi, inspect, os, re

class TinyApp(object):
	"""Represents an app created by the user.
	   Holds the data and functionality needed by the user to create
	   a simple app."""

	def __init__(self):
		"""Initializes the app object with an empty dict of routes."""

		self.routes = {}

	def add_route(self, route, handler, methods=['GET']):
		"""Adds a function to the app's routing dict.
		   Handler - function defined by the user that creates a response."""

		self.routes[route] = (handler, methods)

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
		action_fun, action_methods = self.routes.get(request.path, (None, None)) 

		# TODO: Move this into its own function/method
		# TODO: Request handling is failing on multiple subsequent requests of different types.
		if not action_fun:
			response = TinyResponse.error(404)
		elif request.method not in action_methods:
			response = TinyResponse.error(405)
		else:
			arg_num = len(inspect.getargspec(action_fun)[0])

			# If there aren't any arguments, don't pass the get_data dict to it.
			if arg_num == 0:
				response = action_fun()
			else:
				response = action_fun(request)

		start_response(response.status, response.headers)
		return [response.body]

	def set_template_path(self, template_path):
		"""Registers an absolute template path as the app's template directory."""

		self.template_path = template_path

	def render(self, template_name, *args, **kwargs):
		"""Outputs text of an HTML file from a given template name.
		   Assumes the template is coming from the registered templates dir."""

		template_content = open(os.path.join(self.template_path, template_name)).read()
		pattern = re.compile(r"({{\s?(\w+)\s?}})")
		replacements = {k[0]: k[1] for k in kwargs.iteritems()}
		template_vars = {k[0]: replacements[k[1]] for k in re.findall(pattern, template_content)}
		replacement_pattern = re.compile('|'.join(["{{ %s }}" % (i) for i in replacements.keys()]))
		replaced_content = replacement_pattern.sub(lambda m: template_vars[m.group(0)], template_content)
		return replaced_content

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
		self.path = '/' + self.path if not self.path[0] == '/' else self.path

		self.method = self.environ.get('REQUEST_METHOD', '').upper()

		self._get_data = None
		self._post_data = None

	@property
	def get_data(self):
		"""Returns parsed dictionary of query string parameters."""

		if self.method == 'GET' and self._get_data is None:
			self._get_data = self.get()
		return self._get_data

	@property
	def post_data(self):
		"""Returns parsed dictionary of post data."""

		if self.method == 'POST' and self._post_data is None:
			self._post_data = self.post()
		return self._post_data

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
	"""Represents a response object. When a user makes a request, the app will 
	   formulate the response based on the request data. Tiny binds that response 
	   data to an object of this class."""

	def __init__(self, body, status_code=200, headers=[('Content-Type', 'text/html')]):
		"""Creates a response object that can hold the data for the HTTP response.
		   Defaults to a '200' response with HTML content but allows user to 
		   override."""
		
		self.body = body
		self.status = "{0} {1}".format(status_code, HTTP_CODES[status_code][0])
		self.headers = headers

	@classmethod
	def error(cls, status_code):
		"""Returns a response object given a response class and a status code."""

		status_reason_phrase = HTTP_CODES[status_code][0]
		status_url = HTTP_CODES[status_code][1]
		body = '<a href="{0}"><h1>{1}: {2}</h1></a>'.format(status_url, status_code, status_reason_phrase)
		return cls(body, status_code)


# TODO: HTTP/WSGI Headers

# Taken from http://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6.1.1.
HTTP_CODES = {
	100: ('Continue', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.1'),
	101: ('Switching Protocols', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.2'),
	200: ('OK', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1'),
	201: ('Created', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.2'),
	202: ('Accepted', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.3'),
	203: ('Non-Authoritative Information', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.4'),
	204: ('No Content', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.5'),
	205: ('Reset Content', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.6'),
	206: ('Partial Content', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.7'),
	300: ('Multiple Choices', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.1'),
	301: ('Moved Permanently', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.2'),
	302: ('Found', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.3'),
	303: ('See Other', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.4'),
	304: ('Not Modified', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.5'),
	305: ('Use Proxy', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.6'),
	307: ('Temporary Redirect', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.8'),
	400: ('Bad Request', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.1'),
	401: ('Unauthorized', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2'),
	402: ('Payment Required', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.3'),
	403: ('Forbidden', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4'),
	404: ('Not Found','http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.5'),
	405: ('Method Not Allowed', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.6'),
	406: ('Not Acceptable', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.7'),
	407: ('Proxy Authentication Required', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.8'),
	408: ('Request Timeout', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.9'),
	409: ('Conflict', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.10'),
	410: ('Gone', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.11'),
	411: ('Length Required', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.12'),
	412: ('Precondition Failed', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.13'),
	413: ('Request Entity Too Large', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.14'),
	414: ('Request-URI Too Long', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.15'),
	415: ('Unsupported Media Type', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.16'),
	416: ('Requested Range Not Satisfiable', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.17'),
	417: ('Expectation Failed', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.18'),
	500: ('Internal Server Error', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.1'),
	501: ('Not Implemented', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.2'),
	502: ('Bad Gateway', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.3'),
	503: ('Service Unavailable', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.4'),
	504: ('Gateway Timeout', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.5'),
	505: ('HTTP Version Not Supported', 'http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.6')
}

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