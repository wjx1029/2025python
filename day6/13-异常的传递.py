# Author: Sean W
# 2026年01月05日19时03分41秒
# wanjx0701@gmail.com


def func1():
    num = int(input("请输入一个数字："))
    print(f'I am func1, and my number is {num}')
    return num


def func3():
    try:
        num = int(input("请输入一个数字："))
        print(f'I am func3, and my number is {num}')
        return num
    except ValueError:
        print('输入的不是数字，请重新输入！')
        return None


def func2():
    num = func1()
    print(f'I am func2, and my number is {num}')
    num = func3()
    return num


# 调用func2()函数，如果输入的不是数字，会抛出ValueError异常，并被func2()函数捕获，并打印出异常信息。
# 然后，func2()函数会返回None，而func1()函数也会返回None，因为没有返回值。
# 所以，如果func2()函数调用func1()函数，而func1()函数又抛出异常，则会导致异常的传递。
# 这就是异常的传递。

if __name__ == '__main__':
    try:
        func2()
    except Exception as e:
        print(f'Caught an exception: {e}')
