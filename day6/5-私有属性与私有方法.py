# Author: Sean W
# 2026年01月05日17时32分45秒
# wanjx0701@gmail.com

class Women:
    """
    私有属性和私有方法只能在类的内部使用，外部无法访问
    """

    def __init__(self, name, age):
        self.name = name
        self.__age = age  # 私有属性只能在类的内部使用，外部无法访问

    # 私有方法只能在类的内部使用，外部无法访问
    def __talk(self):
        print("我是女性，我会说话")

    def talk(self):
        self.__talk()

    def boy_friend(self):
        print(f"我是{self.name}的男朋友,我知道她的年龄{self.__age}")


xiaohong = Women("小红", 25)
print(xiaohong.name)  # 小红
# print(xiaohong.__age)  # 报错，无法访问私有属性
# print(xiaohong._Women__age)  # 25，可以通过类名和私有属性名访问私有属性
xiaohong.talk()  # 我是女性，我会说话
# xiaohong.__talk()  # 报错，无法访问私有方法
# xiaohong._Women__talk()  # 可以通过类名和私有属性名访问私有属性
xiaohong.boy_friend()
