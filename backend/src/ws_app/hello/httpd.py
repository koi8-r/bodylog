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
    return Response(text='About')


@httpd.route(path='/uuid')
async def about(req: Request):
    assert req.__class__ is Request

    from .uuid_sinleton import uuid as my_uuid
    return Response(text=json.dumps({'uuid': my_uuid}),
                    content_type="application/json")


@httpd.route(path='/io')
async def about(req: Request):
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
