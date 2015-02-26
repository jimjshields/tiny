import unittest
from tiny import tiny

class TestTinyApp(unittest.TestCase):
	"""Base class for testing TinyApp."""

	def setUp(self):
		"""Starts each test with a new, empty TinyApp object and a handler."""

		self.app = tiny.TinyApp()
		self.app.set_template_path('tiny/templates')

	def tearDown(self):
		"""Ends each test by destroying the TinyApp object."""

		del(self.app)

	def test_app_init(self):
		"""Tests that each app is initialized with an empty routes dict."""

		self.assertEqual(self.app.routes, {})

	def test_add_route(self):
		"""Tests that adding a route actually adds a route to the dictionary."""

		handler = lambda x: x
		self.app.add_route('/index', handler)
		self.assertEqual(self.app.routes, {'/index': (handler, ['GET'])})

	def test_route(self):
		"""Tests that the route decorator also adds a route to the dictionary."""

		@self.app.route('/index')
		def decorator_handler():
			pass

		self.assertEqual(self.app.routes, {'/index': (decorator_handler, ['GET'])})

	def test_set_template_path(self):
		"""Tests that registering the template path to the app saves it to the app."""

		self.assertEqual(self.app.template_path, 'tiny/templates')

	def test_render(self):
		"""Tests that rendering a given template works."""

		template_content = self.app.render('test_render.html', test_var='Testing templates')
		self.assertEqual(template_content, 'Testing templates')

class TestRequestHandler(unittest.TestCase):
	"""Base class for testing the request_handler method."""

	def setUp(self):
		"""Starts each test with a new, empty TinyApp object and a handler."""

		self.app = tiny.TinyApp()
		
		handler = lambda x: tiny.TinyResponse('test')
		self.app.add_route('/index', handler, ['GET', 'POST'])

	def tearDown(self):
		"""Ends each test by destroying the TinyApp object."""

		del(self.app)

	def test_request_handler_working_get_path(self):
		"""Tests that the request handler receives a request for a defined path and
		   the supported 'GET' method and returns an appropriate response."""
		
		environ = create_environ('/index', 'GET')
		response = self.app.request_handler(environ, lambda x, y: None)
		self.assertEqual(response, 'test')

	def test_request_handler_working_post_path(self):
		"""Tests that the request handler receives a request for a defined path and
		   the supported 'POST' method and returns an appropriate response."""
		
		environ = create_environ('/index', 'POST')
		response = self.app.request_handler(environ, lambda x, y: None)
		self.assertEqual(response, 'test')

	def test_request_handler_404(self):
		"""Tests that the request handler receives a request for an undefined path and
		   the supported 'GET' method and returns an appropriate 404 error response."""
		
		environ = create_environ('/nonexistent', 'GET')
		response = self.app.request_handler(environ, lambda x, y: None)
		self.assertEqual(response, '<a href="http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.5"><h1>404: Not Found</h1></a>')

	def test_request_handler_405(self):
		"""Tests that the request handler receives a request for a defined path and
		   the unsupported 'PUT' method and returns an appropriate 405 error response."""
		
		environ = create_environ('/index', 'PUT')
		response = self.app.request_handler(environ, lambda x, y: None)
		self.assertEqual(response, '<a href="http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.6"><h1>405: Method Not Allowed</h1></a>')

class TestTinyRequest(unittest.TestCase):
	"""Base class for testing TinyRequest."""

	def setUp(self):
		"""Starts each test with a new, empty TinyRequest object."""

		self.app = tiny.TinyApp()
		self.environ = create_environ('/index', 'GET')
		self.request = tiny.TinyRequest(self.environ)

	def test_request_init(self):
		"""Tests that the request initializes with the appropriate properties."""

		self.assertEqual(self.request.path, '/index')
		self.assertEqual(self.request.method, 'GET')
		self.assertEqual(self.request._get_data, None)
		self.assertEqual(self.request._post_data, None)

class TestTinyResponse(unittest.TestCase):
	"""Base class for testing TinyResponse."""

	# Tests to go here when best approach is decided for testing connecting to the app and making requests.

def create_environ(path, method):
	"""Helper method that creates an environment to be used for request handler tests."""

	environ = {'PATH_INFO': path, 'REQUEST_METHOD': method}
	return environ

if __name__ == "__main__":
	unittest.main()