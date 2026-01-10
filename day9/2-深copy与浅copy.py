# Author: Sean W
# 2026年01月09日11时06分56秒
# wanjx0701@gmail.com

# 深copy与浅copy
# 深copy：复制整个对象及其包含的所有子对象，包括列表、字典、集合等。
# 浅copy：仅复制对象本身，不包含其包含的子对象。

# 以下是深copy与浅copy的示例代码：

# 深copy
a = [1, 2, 3]
b = a.copy()
a.append(4)
print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2, 3]
print(a is b)

print('-' * 50)

# 浅copy
a = [1, 2, 3]
b = a
a.append(4)
print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2, 3, 4]
print(a is b)

# 结论：深copy复制整个对象及其包含的所有子对象，包括列表、字典、集合等，而浅copy仅复制对象本身，不包含其包含的子对象。

print('-' * 50)

# 导入copy模块
import copy

# 使用copy()，浅copy
a = [1, 2, 3]
b = copy.copy(a)  # 使用copy.copy()函数进行深copy, 可以复制任意对象
b[0] = 4
print(a)  # [1, 2, 3]
print(b)  # [4, 2, 3]
print(a is b)

print('-' * 50)

a = [1, 2]
b = [3, 4]
c = [a, b]
d = copy.copy(c)
a[0] = 10
print(c)  # [[10, 2], [3, 4]]
print(d)  # [[10, 2], [3, 4]]
print(c is d)
print(c[0] is d[0])
print(c[1] is d[1])
print('-' * 50)

# 结论：使用copy.copy()函数进行浅copy，可以复制任意对象，但浅copy仅复制对象本身，不包含其包含的子对象。

# 使用copy.deepcopy()，深copy
a = [1, 2]
b = [3, 4]
c = [a, b]
d = copy.deepcopy(c)
a[0] = 10
print(c)  # [[10, 2], [3, 4]]  # 原对象a的子对象a[0]被修改
print(d)  # [[1, 2], [3, 4]]    # 复制对象d的子对象d[0]不受影响
print(c is d)
print(c[0] is d[0])
print(c[1] is d[1])

# 结论：使用copy.deepcopy()函数进行深copy，可以复制任意对象，且深copy复制整个对象及其包含的所有子对象，包括列表、字典、集合等。

print('=' * 50)


class Hero:
    def __init__(self, name, blood):
        self.name = name
        self.blood = blood  # 可以浅copy
        self.equipment = ['sword', 'shield']  # 必须要深copy


old_hero = Hero('Alice', 100)
new_hero = copy.deepcopy(old_hero)
new_hero.blood = 90
new_hero.equipment.append('shoe')

print(old_hero.name, old_hero.blood, old_hero.equipment)  # Alice 100
print(new_hero.name, new_hero.blood, new_hero.equipment)  # Alice 90
