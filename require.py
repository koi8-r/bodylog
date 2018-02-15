class Task(object):
    def __init__(self, fn, deps=tuple()) -> None:
        assert type(fn).__name__ == 'function', '{} is not a function'.format(fn)
        self.fn = fn
        self.deps = deps
        self.__name__ = fn.__name__

    def __call__(self):
        def _mkdepgr(t):
            # return set([d] if not len(d.deps) else _mkdepgr(d) for d in t.deps)
            res = list()  # todo: set
            for d in t.deps:
                res.extend([d] if not len(d.deps) else _mkdepgr(d))

            return res

        for _ in _mkdepgr(self):
            _.__call__()

        return self.fn.__call__()


class Require(object):
    # todo: class to function, erase uses of self.deps
    def __init__(self, *deps) -> None:
        self.deps = tuple(_ if isinstance(_, Task) else Task(_) for _ in deps)

    def __call__(self, fn):
        for d in self.deps:
            assert type(d) is Task, '{} is not a Task object'.format(d)
            print('Add dependency {} to {}'.format(d.__name__, fn.__name__))

        return Task(fn, self.deps)


require = Require


def init():
    print('Init')


@require(init)
def hello():
    print('Hi!')


@require(hello)
def ask():
    print('How are you?')


@require(ask)
def answer():
    print('Fine :)')


@require(hello)
def bye():
    print('Bye.')


assert type(bye) is Task
bye()
