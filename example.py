import webstruct

class application(webstruct.Application):
    db_url = "sqlite:///"
    templates = ['example_templates']

    @webstruct.view(template='index.html')
    def index(req):
        return dict()

    class users(webstruct.Application):
        @webstruct.view(template="users.html")
        def index(req):
            users = webstruct.query(User).all()
            return dict(users=users)

        @webstruct.view(template="show_user.html", pattern=r'(?P<username>\w+)')
        def show_user(req):
            username = req.urlvars['username']
            user = webstruct.query_one_or_404(User, username=username)
            return dict(user=user)

from sqlalchemy import *

class User(webstruct.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    description = Column(UnicodeText)

webstruct.metadata.create_all()
webstruct.new_data(User, username='aodag', description=u"""aodag is creator of webstruct.
""")
webstruct.transaction.commit()
webstruct.run(application)
