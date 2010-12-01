from webob import Request, Response
from webob.exc import *
from jinja2 import Environment, FileSystemLoader

class ApplicationType(object):
    """ wsgi application type
    """
    def __init__(self, name, bases, dct):
        self.name = name
        self.bases = bases
        self.dct = dct
        environment = Environment(loader=FileSystemLoader(dct['templates']))
        for name, value in dct.iteritems():
            if getattr(value, 'is_view', False):
                value.func.jinja2_environment = environment

    def __call__(self, environ, start_response):
        req = Request(environ)
        path = req.path_info_pop()
        if path is None or path == '':
            path = 'index'
        for name, func in self.dct.iteritems():
            if callable(func) and name == path:
                
                res = req.get_response(func)
                break
        else:
            res = HTTPNotFound()
        return res(environ, start_response)



class Application(object):
    """ WSGI Application constructor

    """
    __metaclass__ = ApplicationType
    templates = []

import functools

def view(**config):
    """ view func configurator
    """
    def dec(func):
        @functools.wraps(func)
        def wrap(environ, start_response):
            request = Request(environ)
            data = func(request)
            tmpl = func.jinja2_environment.get_template(config['template'])
            response = Response(tmpl.render(data))
            return response(environ, start_response)
        wrap.func = func
        wrap.is_view = True
        return wrap
    return dec

