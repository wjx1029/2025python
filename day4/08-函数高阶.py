# Author: Sean W
# 2026年01月04日18时20分33秒
# wanjx0701@gmail.com


def measure():
    """
    掌握返回多个值时，如何去处理
    :return:
    """

    print("开始测量...")
    temp = 39
    wetness = 10
    print("测量结束...")

    return temp, wetness


def demo(num, num_list):
    print("函数内部代码")

    # num = num + num
    num += num
    # num_list.extend(num_list) 由于是调用方法，所以不会修改变量的引用
    # 函数执行结束后，外部数据同样会发生变化
    num_list += [4, 5, 6]

    print(num)
    print(num_list)
    print("函数代码完成")


def kw_argument(name, age=18):
    print("姓名：", name)
    print("年龄：", age)


# 测试函数返回多个值
ret1 = measure()
print(ret1)
print('----------------------------')

# 测试函数内部修改全局变量
gl_num = 9
gl_list = [1, 2, 3]
demo(gl_num, gl_list)
print(gl_num)
print(gl_list)
print('----------------------------')

# 测试关键字参数
kw_argument("小明")
kw_argument("小红", 20)
print('----------------------------')

# 交换两个变量的值
a = 10
b = 5
a, b = b, a
print(a, b)
