import unittest
from webtest import TestApp

import os
here = os.path.dirname(__file__)

class TestApplication(unittest.TestCase):
    
    def test_simple_app(self):
        import webstruct
        class Application(webstruct.Application):
            templates = [os.path.join(here, 'templates')]

            @webstruct.view(default=True, template='index.html')
            def index(request):
                return {'message': 'This is Top'}

            @webstruct.view(default=True, template='index.html')
            def greeting(request):
                return {'message': 'Hello, world!'}

        app = TestApp(Application)
        res = app.get('/')
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.body, "This is Top")
        res = app.get('/greeting')
        self.assertEqual(res.body, "Hello, world!")



