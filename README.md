##Tiny - The tiniest possible web framework. Inspired by [Flask](https://github.com/mitsuhiko/flask), [Bottle](https://github.com/bottlepy/bottle), and [Itty](https://github.com/toastdriven/itty/).

To Install:

    pip install tiny

To create a simple app:

```python
import tiny, os

# Creates the app object.
app = tiny.TinyApp()

# Sets the path for the app to find HTML templates.
app.set_template_path(os.path.abspath('templates'))

## Routing ###

@app.route('/')
def index(request):
    """Defines the index view, accessible at '/'."""
    
    # Creates a response comprised of the content of index.html and rendered template variables.
    content = tiny.TinyResponse(app.render('index.html', template_var="Hello world"))

    # Whatever is returned in a view will display on the page.
    return content # Hello world

## HTTP Errors ##

@app.route('/505')
def error(request):

    content = tiny.TinyResponse('HTTP Version Not Supported', 505)
    return content

if __name__ == '__main__':
    tiny.run_app(app) # Will be accessible at localhost:8080 by default.
```

To create a template:

```html
<!-- index.html -->

{{ template_var }}
```

To run the test suite:

```python
python tests/tests.py

>> ......
>> ----------------------------------------------------------------------
>> Ran 6 tests in 0.001s
>>
>> OK
```


* To Do:
  1. ~~[Implement WSGI interface](https://github.com/jimjshields/tiny/commit/b41241cb2ca3b97bb86be41b81e23fb6e8c8abad)~~
  2. ~~[Parse HTTP GET request](https://github.com/jimjshields/tiny/commit/de0d595db7e0a8357fc504a6e3f19b2149d81eeb)~~
  3. ~~[Set up basic routing in request handler](https://github.com/jimjshields/tiny/commit/de0d595db7e0a8357fc504a6e3f19b2149d81eeb)~~
  4. ~~[Handle non-GET requests](https://github.com/jimjshields/tiny/commit/6ab7452ae689b0089dce8b9ea9619cc60f29d7c0)~~
  5. ~~[Parse queries more cleanly](https://github.com/jimjshields/tiny/commit/6ab7452ae689b0089dce8b9ea9619cc60f29d7c0)~~
  6. ~~[Handle requests more intelligently](https://github.com/jimjshields/tiny/commit/4e2fab42d38475eda23a68483b69ddda3b78e82b)~~
  7. ~~[Handle responses more intelligently](https://github.com/jimjshields/tiny/commit/4e2fab42d38475eda23a68483b69ddda3b78e82b)~~
  8. ~~[Make decorator for creating URLs](https://github.com/jimjshields/tiny/commit/500eabf18e0cd0257d2a066d93fba1a81416aceb)~~
  9. ~~[Store HTTP statuses somewhere](https://github.com/jimjshields/tiny/commit/7de93913d7b7a9b6ce0bc0d41ff5b74ef7b071ca)~~
  10. Move matching URLs into its own method
  11. Refactor rendering template method to be cleaner/more general

* Overall Plan
  1. ~~[WSGI Server](https://github.com/jimjshields/tiny/commit/b41241cb2ca3b97bb86be41b81e23fb6e8c8abad)~~
  2. ~~[Request Handling](https://github.com/jimjshields/tiny/commit/4e2fab42d38475eda23a68483b69ddda3b78e82b)~~
  3. ~~[Response Handling](https://github.com/jimjshields/tiny/commit/4e2fab42d38475eda23a68483b69ddda3b78e82b)~~
  4. ~~[Routing](https://github.com/jimjshields/tiny/commit/9b2089b420b07850fc231c3d855327c635ca8e31)~~
  5. Errors
  6. ~~[Tests](https://github.com/jimjshields/tiny/commit/fe993394624beb93e75925274e61a2f663918f00)~~