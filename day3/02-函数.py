# Aurthor: Sean W
# 2026年01月02日10时06分37秒
# wanjx0701@gmail.com


def say_hello(n):
    """
    输出n次Hello
    :param n:
    :return:
    """
    for i in range(n):
        print(f'Hello {i}')


print('执行函数前')
say_hello(3)
print('执行函数后')
print('-' * 50)


def my_sum(num1, num2):
    print(f'求和结果：{num1 + num2}')


my_sum(3, 5)
my_sum('abc', 'def')
print('-' * 50)


# my_sum(1, 'abc')  不能相加


def my_sum2(num1, num2):
    return num1 + num2


print(f'5 + 3 = {my_sum2(3, 5)}')


def test1():
    print('-' * 50)
    print('test 1')
    print('-' * 50)


def tets2():
    print('test 2')
    print('*' * 75)
    test1()
    print('*' * 75)


tets2()
