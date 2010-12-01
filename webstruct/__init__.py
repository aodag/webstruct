from webob import Request, Response

class ApplicationType(object):
    """ wsgi application type
    """
    def __init__(self, name, bases, dct):
        self.name = name
        self.bases = bases
        self.dct = dct

    def __call__(self, environ, start_response):
        req = Request(environ)
        res = Response()
        return res(environ, start_response)



class Application(object):
    """ WSGI Application constructor

    """
    __metaclass__ = ApplicationType

def conf(**config):
    """ view func configurator
    """
    def dec(func):
        return func
    return dec

