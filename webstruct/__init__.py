import sys
import re
from webob import Request, Response
from webob.exc import *
from jinja2 import Environment, FileSystemLoader

class ConfigurationException(Exception):
    def __init__(self, message):
        super(ConfigurationException. self).__init__
        self.message = message

    def __repr__(self):
        return self.message

class ApplicationType(object):
    """ wsgi application type
    """
    def __init__(self, name, bases, dct):
        self.name = name
        self.bases = bases
        self.dct = dct
        
        parent_template = sys._getframe(1).f_locals.get('templates')
        templates = dct.get('templates', parent_template)
        if templates is None:
            raise ConfigurationException('templates is not found')
        environment = Environment(loader=FileSystemLoader(templates))
        for name, value in dct.iteritems():
            if getattr(value, 'is_view', False):
                value.func.jinja2_environment = environment

    def __call__(self, environ, start_response):
        req = Request(environ)
        path = req.path_info_pop()
        if path is None or path == '':
            path = 'index'
        for name, func in self.dct.iteritems():
            if hasattr(func, 'pattern'):
                pattern = getattr(func, 'pattern')
                m = pattern.match(path)
                if m is not None:
                    req.urlvars.update(m.groupdict())
                    res = req.get_response(func)
                    break
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
    is_view = True

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
        if 'pattern' in config:
            wrap.pattern = re.compile(config.get('pattern'))
        return wrap
    return dec

