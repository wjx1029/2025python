# Aurthor: Sean W
# 2026年01月02日11时10分23秒
# wanjx0701@gmail.com

# 引例1
a = 1
b = a
a = 2
print(a)
print(b)


# 引例2(不可变类型): int bool float str tuple
def cannot_change(num):  # num = a           把a赋值给num
    print(f'num={num}, num_address={id(num)}')
    num = 5
    print(f'num={num}, num_address={id(num)}')


a = 10
print(f'调用函数前，a的地址{id(a)}')
cannot_change(a)
print(f'调用函数后，a的值为{a}')


# 可变类型: list set dict
def can_change(mylist):
    # mylist = [4, 5, 6]
    print(id(mylist))
    mylist[0] = 9
    print(id(mylist))
    mylist = [4, 5, 6]
    print(mylist)
    print(id(mylist))


list1 = [1, 2, 3, 4, 5]  # 可变类型
print(list1)
print(id(list1))
can_change(list1)
print(list1)
print(id(list1))
