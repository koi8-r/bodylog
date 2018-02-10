from aiohttp import web as _httpd
from aiohttp.web import Request, Response
import types


__all__ = ['httpd']


def route(this, verb='GET', path='/'):
    """Add decorated handler to this.app routes"""
    def decorator(fn):
        this.router.add_route(verb, path, fn)
        return fn
    return decorator


def run(this):
    _httpd.run_app(this)


httpd = _httpd.Application()
httpd.route = types.MethodType(route, httpd)
httpd.run = types.MethodType(run, httpd)


@httpd.route(path='/')
async def index(req:Request):
    assert req.__class__ is Request
    return Response(text='Hello, World!')

@httpd.route(path='/about')
async def about(req:Request):
    return Response(text='About')
