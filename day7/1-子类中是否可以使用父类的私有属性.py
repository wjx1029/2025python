# Author: Sean W
# 2026年01月06日09时22分51秒
# wanjx0701@gmail.com


class Parent:
    def __init__(self):
        self.__private_attr = "I am private"

    def get_private_attr(self):
        return self.__private_attr


class Child(Parent):
    def __init__(self):
        super().__init__()
        self.public_attr = "I am public"

    def get_public_attr(self):
        return self.public_attr


if __name__ == '__main__':
    parent = Parent()
    print(parent.get_private_attr())  # I am private

    child = Child()
    # print(child.private_attr)     # 不能调用父类的私有属性
    print(child.get_private_attr())  # I am private
    print(child.get_public_attr())  # I am public
