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

		self.assertEqual(self.app.ROUTES, {})

	def test_add_route(self):
		"""Tests that adding a route actually adds a route to the dictionary."""

		handler = lambda x: x
		self.app.add_route('/index', handler)
		self.assertEqual(self.app.ROUTES, {'/index': (handler, ['GET'])})

	def test_route(self):
		"""Tests that the route decorator also adds a route to the dictionary."""

		@self.app.route('/index')
		def decorator_handler():
			pass

		self.assertEqual(self.app.ROUTES, {'/index': (decorator_handler, ['GET'])})

	def test_request_handler(self):
		"""Tests that the request handler receives a request and returns an
		   appropriate response."""

		# Test to go here when best approach is decided.

	def test_set_template_path(self):
		"""Tests that registering the template path to the app saves it to the app."""

		self.assertEqual(self.app.template_path, 'tiny/templates')

	def test_render(self):
		"""Tests that rendering a given template works."""

		template_content = self.app.render('test.html')
		self.assertEqual(template_content, 'Testing templates')

class TestTinyRequest(unittest.TestCase):
	"""Base class for testing TinyRequest."""

	

if __name__ == "__main__":
	unittest.main()