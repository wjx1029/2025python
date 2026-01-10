# Author: Sean W
# 2026年01月03日19时33分38秒
# wanjx0701@gmail.com


def list_set_slice():
    test_list = [1, 2, 3, 4, 5, 6]
    print(test_list[3:3])

    test_list[3:3] = ['x', 'y', 'z']
    print(test_list)


def list_compare():
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(a == b)
    print(a is b)  # 判断两个对象地址是否一致
    a = b
    print(a is b)  # 判断两个对象地址是否一致


def use_method():
    """
    容器的公共方法
    :return:
    """
    # 1. 索引
    # 2. 切片
    # 3. 迭代
    # 4. 成员资格
    # 5. 长度
    # 6. 追加
    # 7. 移除
    # 8. 计数
    # 9. 排序
    # 10. 反转
    # 11. 复制
    # 12. 转换
    # 13. 其他

    a = (1, 2, 3)
    b = ('a', 'b', 'c')

    print(list(zip(a, b)))
    print(dict(zip(b, a)))
    print(set(zip(a, b)))
    print(tuple(zip(a, b)))
    print('-' * 50)

    # 如何使用enumerat
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    list2 = list(enumerate(seasons))
    print(type(enumerate(seasons)))
    print(list2)
    mydict = dict(list2)
    print({v: k for k, v in mydict.items()})


# list_set_slice()
# list_compare()
use_method()
