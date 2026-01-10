# Author: Sean W
# 2026年01月05日17时57分08秒
# wanjx0701@gmail.com

class Father:
    def __init__(self, height, *args):
        self.height = height
        super().__init__(*args)


class Mother:
    def __init__(self, weight):
        self.weight = weight


class Son1(Father, Mother):
    def __init__(self, age, *args):
        self.age = age
        super().__init__(*args)


class Son2(Father, Mother):
    def __init__(self, score, *args):
        self.score = score
        super().__init__(*args)


class Grandson(Son1, Son2):
    def __init__(self, name, *args):
        self.name = name
        super().__init__(*args)


if __name__ == '__main__':
    xiaoming = Grandson('xiaoming', 18, 90, 170, 85)
    print(xiaoming.name)
    print(xiaoming.age)
    print(xiaoming.score)
    print(xiaoming.height)
    print(xiaoming.weight)
    print(Grandson.__mro__)
