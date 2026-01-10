# Author: Sean W
# 2026年01月05日09时28分28秒
# wanjx0701@gmail.com


class Cat(object):
    """这是一个猫类"""

    # 初始化方法
    def __init__(self, name):
        self.name = name
        print('%s 来了' % self.name)

    # 对象从内存中被销毁前，会自动调用该方法
    def __del__(self):
        print('%s被销毁了' % self.name)

    # 返回对象的描述信息,print()打印对象时调用该方法
    def __str__(self):
        return f'我是小猫{self.name}'

    def eat(self):
        print("小猫%s爱吃鱼" % self.name)

    def drink(self):
        print("小猫%s在喝水" % self.name)


tom = Cat('Tom')
lazy_cat = Cat('Lazy')
tom.drink()
lazy_cat.eat()
print(tom is lazy_cat)
print('--' * 25)
# tom.name = 'Tom'  # 不规范编程，不要在类外设置属性
# print(tom.name)

del lazy_cat
print('--' * 25)

print(tom)
