# Aurthor: Sean W
# 2026年01月02日22时21分04秒
# wanjx0701@gmail.com
import module_for_print as mfp


def find_1_times_in_seven_numbers():
    l = [2, 2, 3, 1, 3, 4, 4]
    res = 0
    for i in l:
        res = res ^ i
    print(l)
    print(res)


def print_20_numbers_in_a_line():
    for i in range(1, 21):
        print(i, end=' ')


def print_hello(n):
    """
    print n times hello
    :param n: n times
    :return: None
    """
    for i in range(n):
        print('hello')


def find_2_numbers_of_1_times_in_eight_numbers():
    l = [3, 5, 5, 6, 7, 6, 9, 9]
    res = 0
    for i in l:
        res = res ^ i
    # 分治
    res1, res2 = 0, 0
    flag = res & -res
    for i in l:
        if flag & i:
            res1 = res1 ^ i
        else:
            res2 = res2 ^ i

    print(res1, res2)


find_1_times_in_seven_numbers()
print('-' * 50)
print_20_numbers_in_a_line()
print('\n' + '-' * 50)
print_hello(3)
print('-' * 50)
mfp.print1(5)
mfp.print2('&', 25)
mfp.print3()
mfp.print2('-', 50)

find_2_numbers_of_1_times_in_eight_numbers()
