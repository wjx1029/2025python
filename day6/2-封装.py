# Author: Sean W
# 2026年01月05日09时57分41秒
# wanjx0701@gmail.com


class Person:
    """
    人类
    """

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        """
        打印对象信息,返回值是字符串
        """
        return f"姓名：{self.name}, 体重：{self.weight}公斤"

    def run(self):
        self.weight -= 0.5
        print(f"{self.name}正在奔跑... 体重减少0.5公斤,现有体重{self.weight}公斤")

    def eat(self):
        self.weight += 1
        print(f"{self.name}正在吃, 体重增加1公斤,现有体重{self.weight}公斤")


if __name__ == '__main__':
    person = Person("小明", 70)
    print(person)
    person.run()
    person.eat()
    print('-' * 50)
    person2 = Person("小红", 60)
    print(person2)
    person2.eat()
    person2.run()
