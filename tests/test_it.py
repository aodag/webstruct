import unittest
from webtest import TestApp

import os
here = os.path.dirname(__file__)

class TestApplication(unittest.TestCase):
    
    def test_init_app(self):
        import webstruct
        class Application(webstruct.Application):
            templates = [os.path.join(here, 'templates')]

            @webstruct.conf(default=True, template='index.html')
            def index(request):
                return {}
        app = TestApp(Application)
        res = app.get('/')
        self.assertEqual(res.status_int, 200)


