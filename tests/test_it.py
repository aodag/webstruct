import unittest
from webtest import TestApp

import os
here = os.path.dirname(__file__)

class TestApplication(unittest.TestCase):
    
    def test_simple_app(self):
        import webstruct
        class Application(webstruct.Application):
            templates = [os.path.join(here, 'templates')]

            @webstruct.view(template='index.html')
            def index(request):
                return {'message': 'This is Top'}

            @webstruct.view(template='index.html')
            def greeting(request):
                return {'message': 'Hello, world!'}

        app = TestApp(Application)
        res = app.get('/')
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.body, "This is Top")
        res = app.get('/greeting')
        self.assertEqual(res.body, "Hello, world!")

    def test_submount(self):
        import webstruct
        class Application(webstruct.Application):
            templates = [os.path.join(here, 'templates')]

            @webstruct.view(template='index.html')
            def index(request):
                return {'message': 'This is Top'}

            class sub_contents(webstruct.Application):
                @webstruct.view(template='index.html')
                def index(request):
                    return {'message': 'This is sub'}
                @webstruct.view(template='index.html')
                def more(request):
                    return {'message': 'more'}
                
        app = TestApp(Application)
        res = app.get('/sub_contents/')
        self.assertEqual(res.body, "This is sub")

        res = app.get('/sub_contents/more')
        self.assertEqual(res.body, "more")

    def test_pattern(self):
        import webstruct
        class Application(webstruct.Application):
            templates = [os.path.join(here, 'templates')]

            @webstruct.view(template='index.html')
            def index(request):
                return {'message': 'This is Top'}
            class users(webstruct.Application):
                @webstruct.view(template='user.html', pattern=r'(?P<username>\w+)')
                def user_view(request):
                    name = request.urlvars['username']
                    return dict(name=name)


        app = TestApp(Application)
        res = app.get('/users/aodag')
        self.assertEqual(res.body, "This is aodag")
