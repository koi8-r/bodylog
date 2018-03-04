from aiohttp import web as _httpd
from aiohttp.web import Request, Response, HTTPRequestEntityTooLarge
from aiohttp.streams import StreamReader
import types
import logging
import json


__all__ = ['httpd']

log = logging.getLogger()


def route(this, verb='GET', path='/'):
    """Add decorated handler to this.app routes"""

    def decorator(fn):
        this.router.add_route(verb, path, fn)
        return fn

    return decorator


def run(this):
    _httpd.run_app(this)


httpd = _httpd.Application()
# noinspection PyArgumentList
httpd.route = types.MethodType(route, httpd)
# noinspection PyArgumentList
httpd.run = types.MethodType(run, httpd)

httpd.MAX_UPLOAD_SIZE = 1024  # 1024**2 = 1M


@httpd.route(path='/')
async def index(req: Request):
    assert req.__class__ is Request
    return Response(text='index')


@httpd.route(path='/about')
async def about(req: Request):
    assert req.__class__ is Request
    return Response(text='Ab111out')


@httpd.route(path='/guid')
async def guid(req: Request):
    assert req.__class__ is Request

    accept = req.headers.get('accept') or '*/*'
    from .uuid_sinleton import guid as my_guid

    res =\
        dict(text=json.dumps({'uuid': my_guid}),
             content_type='application/json') \
        if accept in ['application/json', '*/*']\
        else \
        dict(text=my_guid,
             content_type='text/plain')

    return Response(**res)


@httpd.route(verb='GET', path='/health')
async def health_check(req: Request):
    assert req.__class__ is Request
    from .health import state
    return Response(status=200 if not state['failed'] else 500)


@httpd.route(verb='POST', path='/health')
async def health_toggle(req: Request):
    assert req.__class__ is Request
    from .health import state
    state['failed'] = not state['failed']
    return Response(status=200)


@httpd.route(verb='POST', path='/io')
async def io(req: Request):
    assert isinstance(req.content, StreamReader, )

    body = bytearray()
    while True:
        chunk = await req.content.read(1)

        if len(body) + len(chunk) > req.app.MAX_UPLOAD_SIZE:
            raise HTTPRequestEntityTooLarge

        body.extend(chunk)
        if not chunk:
            break

    return Response(status=200, body=body)  # text=body.decode('utf-8')


@httpd.route(verb='GET', path='/hostname')
async def default_ip_address(req: Request):
    assert req.__class__ is Request
    from socket import gethostname
    return Response(status=200, text=gethostname())


@httpd.route(verb='GET', path='/ip')
async def default_ip_address(req: Request):
    assert req.__class__ is Request
    from socket import socket, AF_INET, SOCK_DGRAM
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(('8.8.8.8', 0, ))
    return Response(status=200, text=s.getsockname()[0])
