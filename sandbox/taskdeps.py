def require(*deps):
    def decorator(fn):
        def wrapped(*args, **kwargs):
            for d in deps:
                d.__call__()

            return fn(*args, **kwargs)
        
        wrapped.__require__ = [_ for _ in deps]
        return wrapped

    return decorator


def init():
    print('Init')


def say_hello():
    print('Hello!')


def say_bye():
    print('Bye.')


@require(say_hello, init)  # fixme
def ask():
    print('How are you?')


def answer():
    print('Fine!')


@require(init, say_hello, ask, answer, say_bye)
def evaluate():
    pass


evaluate()
