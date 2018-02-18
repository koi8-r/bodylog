import asyncio
from time import sleep


async def worker_a():
    sleep(5)
    return 'A'


async def worker_b():
    raise Exception('Error')


async def worker_c():
    return 'B'


async def main():
    complete, pending = await asyncio.wait([worker_c(), worker_b(), worker_a()])
    print('\n'.join(_.result() for _ in complete))
    #print(await worker_a())
    #print(await worker_b())


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main())
finally:
    event_loop.close()
