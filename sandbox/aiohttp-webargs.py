import asyncio
from aiohttp import web
from webargs import fields
from marshmallow import fields
from marshmallow import Schema
from webargs.aiohttpparser import parser, use_args, use_kwargs


class PersonSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(missing='')

    class Meta:
        strict = True


@asyncio.coroutine
@use_kwargs({'name': fields.Str(missing='',
                                location='query'),
             'slug': fields.Str(missing='',
                                location='match_info')})
def index(request: web.Request, name, slug):
    print(name + slug)
    return web.Response(body='index'.encode('utf-8'))


@asyncio.coroutine
@use_args(PersonSchema())
def post_person(request: web.Request, person):
    print(person)
    return web.Response(body='person'.encode('utf-8'))


app = web.Application()
app.router.add_route('GET', '/{slug:[^/]*}', index)
app.router.add_route('POST', '/p/person', post_person)


web.run_app(app)
