import asyncio
from aiohttp import web
from marshmallow import fields
from marshmallow import Schema
import mimeparse
import json


def is_acceptable(ct, ua_acceptable=None):
    return mimeparse.best_match([ct], ua_acceptable or '*/*')


def produce(accept, renderer=lambda _: str(_)):
    def decorator(fn):
        async def wrapped(req: web.Request):
            if not is_acceptable(accept, req.headers.get('Accept')):
                return web.Response(status=406)  # raise web.HTTPNotAcceptable
            # await if asyncio.iscoroutinefunction or asyncio.iscoroutine
            res = await fn(req)
            # assert getattr(res, 'data', None)  # io?
            res.text = renderer(res.text)
            res.content_type = accept
            return res
        wrapped.__name__ = fn.__name__  # mimic for resource names
        return wrapped
    return decorator


def produce_json(fn):
    return produce(accept='application/json', renderer=lambda _: json.dumps(_))(fn)


def produce_self(fn):
    async def wrapped(req: web.Request):
        this_url = req.app.router[fn.__name__].url_for()
        print('Self url: {}'.format(this_url))
        res = await fn(req)
        # if isinstance(res.text, dict):
        return res
    wrapped.__name__ = fn.__name__  # mimic for resource names
    return wrapped


# @route wrong wrap
@produce_self
@produce_json  # data dict.update() <- dict(self=self_url)
async def index(req: web.Request):
    return web.Response(body='person'.encode('utf-8'))

    # return web.Response(data=dict(person='person'))
    # marshmallow acceps dict? force serialization validation
    # return dict(a='b')  # iscoroutine, isinstance(data, dict), isinstance(model), return json_renderer(data)


app = web.Application()
app.router.add_route('GET', '/', index, name=index.__name__)


web.run_app(app)
