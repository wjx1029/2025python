# Author: Sean W
# 2026年01月05日10时08分54秒
# wanjx0701@gmail.com


class Houseitem:
    def __init__(self, name, area):
        """
        初始化方法
        :param name: 家具名字
        :param area: 占地面积
        """
        self.name = name
        self.area = area

    def __str__(self):
        """
        打印方法
        :return:
        """
        return f"{self.name}占地{self.area}平方米"


class House:
    def __init__(self, house_type, area):
        """
        初始化方法
        """
        self.house_type = house_type
        self.area = area
        self.free_area = area
        self.items = []

    def __str__(self):
        """
        打印方法
        """
        return ("户型：%s\n总面积：%.2f\n空闲面积：%.2f\n家具：%s" % (
            self.house_type, self.area, self.free_area, self.items))

    def add_item(self, item):
        """
        添加家具
        :param item: 家具对象
        """
        if item.area <= self.free_area:
            self.items.append(item.name)
            self.free_area -= item.area
        else:
            print("家具占地面积超过房屋空闲面积")


bed = Houseitem("床", 5)
table = Houseitem("桌子", 2)
chair = Houseitem("椅子", 0.5)
print(bed)
print('-' * 50)

house = House("一室一厅", 10)
print(house)
house.add_item(bed)
house.add_item(table)
print(house)

house.add_item(bed)
