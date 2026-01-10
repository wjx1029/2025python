# Author: Sean W
# 2026年01月04日18时33分24秒
# wanjx0701@gmail.com


def demo1(*args, **kwargs):
    print(f'demo1 args: {args}')
    print(f'demo1 kwargs: {kwargs}')


def demo(num, age, *args, **kwargs):
    print(type(args))
    print(type(kwargs))
    print(f'demo args: {args}')
    print(f'demo kwargs: {kwargs}')
    demo1(*args, **kwargs)


demo(1, 2, 3, 4, 5, a=4, b=5)
