from functools import wraps

def decorator(a):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            print('inside decorator')
            func(*args, **kwargs)
        return inner
    return wrapper

@decorator(a=1)
def test(a):
    print('inside test')
    print(a)


test(a=1)
