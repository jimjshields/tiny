"""
tiny.py is a practice project that implements the 
most basic possible web framework in Python.
"""

# TODO: WSGI Server

def demo_app(environ, start_response):
	"""Creates a demo WSGI app."""

	status = '200 OK'
	headers = [('Content-type', 'text/plain')]
	start_response(status, headers)

	return ['Hello world!']

def wsgiref_server(app, host='', port=8080):
	"""Implements a WSGIref server and serves continuously.
	   Can override default host and port if desired."""
	
	from wsgiref.simple_server import make_server
	server = make_server(host, port, app)
	server.serve_forever()

def run_app(app):
	"""Runs a given app with a WSGIref server."""

	wsgiref_server(app)

# TODO: HTTP

# TODO: Request class

# TODO: Response class

# TODO: Headers

# TODO: Routing

# TODO: Error handling