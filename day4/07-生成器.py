# Author: Sean W
# 2026年01月04日18时16分01秒
# wanjx0701@gmail.com


my_tuple1 = (x for x in range(10))
print(my_tuple1)
print(type(my_tuple1))

my_tuple2 = tuple(x for x in range(10))
print(my_tuple2)
print(type(my_tuple2))

my_set = {x for x in 'abcdefgacacad' if x not in 'abc'}
print(my_set)
print(type(my_set))
