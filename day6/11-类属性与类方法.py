# Author: Sean W
# 2026年01月05日18时27分18秒
# wanjx0701@gmail.com


class Tool:
    count = 0  # 类属性

    def __init__(self, name):
        self.name = name
        Tool.count += 1  # 类方法

    def func(self):
        print(f"{self.name} can do something.")

    @classmethod
    def get_count(cls):
        """
        当你不使用对象属性，只使用类属性，类方法可以作为一种便捷的方法来访问类属性。
        :return:
        """
        print(cls.count)

    @staticmethod
    def help():
        """
        静态方法不需要实例化，可以直接通过类名来调用。不使用对象属性，也不使用类属性
        :return:
        """
        print('这是一个工具类，作用是实例化各种工具对象')


t1 = Tool('锤子')
t2 = Tool('刀')
t3 = Tool('铅笔')

Tool.get_count()  # 3
print(Tool.count)  # 3

Tool.help()  # 这是一个工具类，作用是实例化各种工具对象

# 类方法和静态方法的区别：
# 类方法：需要使用类名来调用，需要实例化对象，可以访问类属性。
# 静态方法：不需要实例化对象，可以直接通过类名来调用，不使用对象属性，也不使用类属性。

del t3  # 删除对象t3，类属性count不变
Tool.get_count()  # 3

Tool.name = 'test'  # 类属性name被修改，但不会影响类属性count  不要在类外，给类增加类属性
print(Tool.name)
Tool.get_count()  # 3

t1.func()  # 锤子 can do something.
Tool.func(t1)  # 锤子 can do something.
Tool.func(t2)  # 刀 can do something.
