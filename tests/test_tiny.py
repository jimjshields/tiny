import unittest
from tiny import tiny

class TestTinyApp(unittest.TestCase):
	"""Base class for testing TinyApp."""

	def setUp(self):
		"""Starts each test with a new, empty TinyApp object and a handler."""

		self.app = tiny.TinyApp()
		self.handler = lambda x: x

	def tearDown(self):
		"""Ends each test by destroying the TinyApp object."""

		del(self.app)
		del(self.handler)

	def test_app_init(self):
		"""Tests that each app is initialized with an empty routes dict."""

		self.assertEqual(self.app.ROUTES, {})

	def test_add_route(self):
		"""Tests that adding a route actually adds a route to the dictionary."""

		self.app.add_route('/index', self.handler)
		self.assertEqual({'/index': (self.handler, ['GET'])}, self.app.ROUTES)

	def test_route(self):
		"""Tests that the route decorator also adds a route to the dictionary."""

		@self.app.route('/index')
		def decorator_handler():
			pass

		self.assertEqual({'/index': (decorator_handler, ['GET'])}, self.app.ROUTES)

if __name__ == "__main__":
	unittest.main()