from asyncio import get_event_loop, coroutine


def worker():
    while True:
        yield 'Z'


@coroutine
def f():
    w = worker()
    w.send(None)
    r = yield from w
    return r



print(get_event_loop().run_until_complete(f()))
