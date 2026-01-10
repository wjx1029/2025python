# Author: Sean W
# 2026年01月03日10时00分40秒
# wanjx0701@gmail.com


def check_type():
    """
    判断字符串类型
    :return:
    """
    s1 = 'abc_'
    print(s1.isalnum())
    s2 = '123'
    print(s2.isdecimal())
    print(s1.upper())


def str_find():
    """
    字符串查找与替换
    :return:
    """
    s1 = 'abcdefgcdcd'
    print(s1.find('cd'))
    print(s1.find('cdf'))
    print(s1.find('z'))
    print(s1.find('c', 3, 6))

    s2 = s1.replace('cd', 'CD', 2)
    print(s2)


def split_join():
    """
    字符串分割与链接
    :return:
    """
    s1 = 'abc def scc'
    print(s1.split())
    s1 = 'abc,def,scc'
    print(s1.split(','))

    s2 = 'abc\nbcd\nkkk'
    print(s2)
    print(s2.splitlines())
    print(s2.split('\n'))

    str_list = ['abc', 'd', 'csaca', 'hhhhhh']
    print(''.join(str_list))
    print('-'.join(str_list))


def str_slice():
    """
    字符串的切片
    :return:
    """
    nums_str = '0123456789'
    print(nums_str[2:6])
    print(nums_str[2:])
    print(nums_str[:6])
    print(nums_str[:])
    print(nums_str[::2])
    print(nums_str[1::2])
    print(nums_str[-1])
    print(nums_str[2:-1])
    print(nums_str[-2:])
    print(nums_str[::-1])  # 逆序


# check_type()
# str_find()
# split_join()
str_slice()
