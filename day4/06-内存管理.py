# Author: Sean W
# 2026年01月03日19时48分50秒
# wanjx0701@gmail.com

a = 2
b = 2
print(a is b)
a = 'hello'
print(id(a))
del a
b = 'hello'
print(id(b))

print('-' * 50)

a = 100000000000
b = 100000000000
c = b
print(a is b)
print(a is c)
