# Aurthor: Sean W
# 2025年12月31日14时06分27秒
# wanjx0701@gmail.com


def use_character():
    str1 = 'a'
    str2 = 'abc'

    print(type(str1))
    print(type(str2))

    str3 = "abc\'dfg"
    print(str3)

    str4 = 'abc\nfdg'
    print(str4)

    str5 = "abc\'\"bac"
    print(str5)

    str6 = "abc\\\\\\bacd"
    print(str6)

    print('-' * 50)
    print(ord('0'))  # 字符0的整型值
    print(chr(66))  # 将66转换为字符


def use_input_output():
    a = input("请输入内容：")
    print(a)
    print(type(a))
    print(type(ord(a) + 32))

    b = input("Please input a number:")
    print(float(b) + 5)
    # print(int(b))     # ValueError

    # standard output
    score = 98.2
    name = 'Sean W'
    age = 23
    print('name: %s score: %.2f age: %d' % (name, score, age))
    print('name: %10s\t\tscore: %.2f\t\tage: %d' % (name, score, age))
    print('name: %10s\t\tscore: %.2f\t\tage: %d' % ('John', 78, 23))


def use_operation():
    """
    学习算术运算符
    :return:
    """
    a = 5 / 2
    print(a)
    a = 5 // 2
    print(a)

    print(3 > 5)
    print(3 < 5)

    print(3 and 5)  # 短路运算
    print(0 and 3)
    print(3 and 0)
    print(0 or 3)
    print(1 or 3)
    print(3 or 0)

    a = False
    a and print('you cannot see me')  # replace if
    a or print('you can see me')
    a = True
    a and print('you can see me')
    a or print("you cannot see me")

    a = format(95, '08b')
    b = format(27, '08b')
    print(a)
    print(b)
    print('%s & %s = %s' % (a, b, format(95 & 27, '08b')))
    #
    print(format(95 | 27, '08b'))
    print(format(95 ^ 27, '08b'))
    print(format(~95, '08b'))
    # left shift
    print(format(27 << 1, '08b'))
    print(format(-27 << 1, '08b'))
    # right shift
    # 右移正数高位补0，负数高位补1,低位丢弃
    print('%s >> 1 : %s' % (a, format(95 >> 1, '08b')))
    print('%s >> 1 : %s' % (format(-95, '08b'), format(-95 >> 1, '08b')))

    print(5 ^ 0)
    print(5 ^ 5)

    print(2 ** 5)
    print(2 ** 10)


use_character()
print('*' * 50)
# use_input_output()
print('*' * 50)
use_operation()
