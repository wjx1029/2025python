# Author: Sean W
# 2026年01月05日18时14分26秒
# wanjx0701@gmail.com


# 多态是面向对象编程的重要特性，它允许不同类的对象对同一消息作出不同的响应。
# 多态的实现方法有两种：
# 1. 重载（Overloading）：在同一个类中，可以有多个同名方法，根据不同的参数列表调用不同的方法。
# 2. 重写（Override）：子类可以对父类的方法进行重新定义，使得子类对象在调用父类的方法时，执行子类的定义。

# 以下是Python中多态的示例代码：

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass


class Plant:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        print(f"{self.name} says woof!")


class Cat(Animal):
    def speak(self):
        print(f"{self.name} says meow!")


# class Tree(Plant):
#     def speak(self):
#         print(f"{self.name} ... (it's a tree!)")


class Person:
    def __init__(self, name):
        self.name = name

    def talk(self, animal):
        print(f"{self.name} talks to {animal.name}")
        animal.speak()

    # def talk(self, plant):
    #     print(f"{self.name} talks to {plant.name}")
    #     plant.speak()


dog = Dog("wangcai")
cat = Cat("miaomiao")
person = Person("Alice")
# tree = Tree("oak")

person.talk(dog)  # Alice talks to wangcai says woof!
person.talk(cat)  # Alice talks to miaomiao says meow!
# person.talk(tree)  # Alice talks to oak ... (it's a tree!)
