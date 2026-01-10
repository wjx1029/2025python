# Author: Sean W
# 2026年01月03日09时07分52秒
# wanjx0701@gmail.com


def tuple_api():
    mytuple = ('sean', 18, 98.5, '12568369')
    a = ()  # empty tuple

    print(mytuple.count('sean'))
    print(mytuple.count(2))
    print(mytuple.index(18))
    # print(mytuple.index(2))

    # 遍历
    for i in mytuple:
        print(i)
    for i in range(len(mytuple)):
        print(mytuple[i])

    # 多数据格式化
    print("name:%s age:%d grade:%.2f id:%s" % mytuple)


def list_to_tuple():
    a = [1, 2, 3]
    print(type(a))
    b = tuple(a)
    print(type(b))
    c = list(b)
    print(type(c))

    print(a)
    print(b)
    print(c)

    print(id(a))
    print(id(b))
    print(id(c))


def use_tuple_error():
    a = []
    b = ()
    print(type(a))
    print(type(b))

    a = [1]
    b = (1)
    c = (1,)
    print(type(a))
    print(type(b))
    print(type(c))


tuple_api()
use_tuple_error()
list_to_tuple()
