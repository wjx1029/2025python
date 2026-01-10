# Aurthor: Sean W
# 2025年12月31日14时52分57秒
# wanjx0701@gmail.com


def sum_odd_between_0_and_100():
    res = 0
    for i in range(1, 101, 2):
        res += i
    return res


def print_multi_table():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print('%d*%d=%d\t' % (j, i, i * j), end='')
        print('\n')


def count_1_in_int():
    num = int(input('Input a number:'))
    print(format(num & 0xffffffffffffffff, '064b'))
    count = 0
    for i in range(64):
        if 1 & num:
            count += 1
        num = num >> 1
    print(count)


res1 = sum_odd_between_0_and_100()
print(res1)
print_multi_table()
count_1_in_int()
