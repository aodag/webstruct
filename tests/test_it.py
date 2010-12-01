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

                class sub_contents(webstruct.Application):
                    @webstruct.view(template='index.html')
                    def index(request):
                        return {'message': 'This is subsub'}
                
        app = TestApp(Application)
        res = app.get('/sub_contents/')
        self.assertEqual(res.body, "This is sub")

        res = app.get('/sub_contents/more')
        self.assertEqual(res.body, "more")

        res = app.get('/sub_contents/sub_contents')
        self.assertEqual(res.body, "This is subsub")

    def test_pattern_match1(self):
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

    def test_pattern_match2(self):
        import webstruct
        class Application(webstruct.Application):
            templates = [os.path.join(here, 'templates')]

            @webstruct.view(template='index.html')
            def index(request):
                return {'message': 'This is Top'}
                
            class users(webstruct.Application):
                class user_view(webstruct.Application):
                    pattern=r'(?P<username>\w+)'
                    @webstruct.view(template='user.html', )
                    def index(request):
                        name = request.urlvars['username']
                        return dict(name=name)
                    @webstruct.view(template='index.html', )
                    def edit(request):
                        name = request.urlvars['username']
                        return dict(message='edit %s' % name)



        app = TestApp(Application)
        res = app.get('/users/aodag')
        self.assertEqual(res.body, "This is aodag")
        res = app.get('/users/aodag/edit')
        self.assertEqual(res.body, "edit aodag")

    def test_db(self):
        import webstruct
        class Application(webstruct.Application):
            db_url = 'sqlite:///'
            templates = [os.path.join(here, 'templates')]

            @webstruct.view(template='index.html')
            def index(request):
                return {'message': 'This is Top'}
            class users(webstruct.Application):
                @webstruct.view(template='show_user.html', pattern=r'(?P<username>\w+)')
                def show_user(request):
                    name = request.urlvars['username']
                    user = webstruct.query(User).one()
                    return dict(user=user)
        from sqlalchemy import Column, Integer, String, UnicodeText
        class User(webstruct.Model):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            username = Column(String(255), unique=True)
            description = Column(UnicodeText)
        webstruct.metadata.create_all()
        user = webstruct.new_data(User, username='aodag', description=u"this is test")
        webstruct.transaction.commit()
        app = TestApp(Application)
        res = app.get('/users/aodag')
        self.assert_('aodag' in res.body)
        self.assert_('this is test' in res.body)

