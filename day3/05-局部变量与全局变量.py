# Aurthor: Sean W
# 2026年01月02日11时49分46秒
# wanjx0701@gmail.com

# 1.执行到需要全局变量时，全局变量必须已经定义了
# 2.就近原则
# 3.函数内修改全局变量需要加 global

def demo1():
    num = 5
    print(id(num))
    print(num)


def demo2():
    global num
    print(num)
    print(id(num))
    num = 2
    print(id(num))


num = 10
print(id(num))
demo1()
print(id(num))
print('-' * 50)

print(id(num))
demo2()
print(num)
print(id(num))
