# Author: Sean W
# 2026年01月03日11时22分04秒
# wanjx0701@gmail.com


set1 = {1, 2, 3.6, 'abc'}
set2 = set()
set3 = {}
print(type(set3))
print(type(set2))

set1.add(3)
print(set1)
print('-' * 50)

set2 = set1.copy()
print(set2)
print('-' * 50)

set2.clear()
print(set2)
print('-' * 50)

# .difference()
x = {'apple', 'banana', 'cherry'}
y = {'google', 'mircosoft', 'apple'}
z = x.difference(y)
print(f'差集{z}')
print('-' * 50)

# .difference_update()
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
x.difference_update(y)
print(x)
print('-' * 50)

# .discard()
fruits = {"apple", "banana", "cherry"}
fruits.discard("banana")
print(fruits)
print('-' * 50)

# .intersection()   求交集
x = {"a", "b", "c"}
y = {"c", "d", "e"}
z = {"f", "g", "c"}
result = x.intersection(y, z)
print(result)
print('-' * 50)

# .symmetric_difference()
x = {"apple", "banana", "cherry"}
y = {"google", "runoob", "apple"}
z = x.symmetric_difference(y)
print(z)
print('-' * 50)

# .union()
x = {"apple", "banana", "cherry"}
y = {"google", "runoob", "apple"}
z = x.union(y)
print(z)
print('-' * 50)

# 集合运算
x = {1, 2, 3, 4, 5}
y = {4, 5, 6, 7, 8}

print(x.union(y))  # 并集
print(x.intersection(y))  # 交集
print(x.difference(y))  # 差集
print(x.symmetric_difference(y))  # 对称差集

print('apple' in z)

print(x - y)
print(x ^ y)
print(x & y)
print(x | y)
