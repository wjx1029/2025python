# Author: Sean W
# 2026年01月05日17时40分19秒
# wanjx0701@gmail.com


class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")

    def drink(self):
        print(f"{self.name} is drinking.")

    def run(self):
        print(f"{self.name} is running.")

    def sleep(self):
        print(f"{self.name} is sleeping.")


class Dog(Animal):
    def __init__(self, name, color):
        super().__init__(name)  # 调用父类的构造函数
        self.color = color

    def bark(self):
        print(f"{self.name} is barking.")

    def run(self):
        super().run()  # 调用父类的run方法
        print(f"{self.name} is running very fast.")


class XiaoTianQuan(Dog):
    def __init__(self, name, color, age):
        super().__init__(name, color)  # 调用父类的构造函数
        self.age = age

    def run(self):
        super().run()  # 调用父类的run方法
        print(f"{self.name} is running very fast and agile.")

    def bark(self):
        super().bark()  # 调用父类的bark方法
        print(f"{self.name} is barking very loudly.")

    def fly(self):
        print(f"{self.name} is flying.")


dog = Dog("Wangcai", "white")
dog.run()
dog.bark()
dog.eat()
dog.drink()
dog.sleep()
print('-' * 50)
xiao_tian_quan = XiaoTianQuan("XiaoTianQuan", "black", 300)
xiao_tian_quan.run()
xiao_tian_quan.bark()
xiao_tian_quan.fly()
xiao_tian_quan.eat()
