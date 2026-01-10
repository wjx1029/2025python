# Aurthor: Sean W
# 2026年01月02日19时41分36秒
# wanjx0701@gmail.com

def list_api():
    mylist = []

    # .append()
    mylist.append(1)
    mylist.append(2)
    mylist.append(3)
    print(mylist)

    # .insert()
    mylist.insert(2, 6)
    print(mylist)

    # .extend()
    list2 = [5, 6, 7]
    mylist.extend(list2)
    print(mylist)

    # 查找
    print(mylist.index(5))
    print(mylist[5])
    # print(mylist.index(8))

    # 修改
    mylist[3] = 'hi'
    print(mylist)

    # .remove()
    mylist.remove('hi')
    print(mylist)
    # mylist.remove('ii')

    # .pop()
    mylist.pop()
    print(mylist)
    mylist.pop(2)
    print(mylist)

    # .copy()
    copy_list = mylist.copy()
    print(copy_list)

    # .clear()
    copy_list.clear()
    print(copy_list)
    print(mylist)

    # .count()
    print(mylist.count(3))
    mylist.extend([2, 2, 2])
    print(mylist)
    print(mylist.count(2))
    print(len(mylist))

    # .reverse()
    print(mylist)
    mylist.reverse()  # 列表反转
    print(mylist)

    # .sort()
    print(mylist)
    mylist.sort()  # 升序
    print(mylist)
    mylist.sort(reverse=True)  # 降序
    print(mylist)

    # 遍历（修改或删除列表中的元素，用while更方便）
    for i in mylist:
        print(i)


def list_generator():
    mylist = [x for x in range(10)]
    print(mylist)

    a = [j for i in range(10) for j in range(i)]
    print(a)

    b = [[col * row for col in range(5)] for row in range(5)]
    print(b)
    print(b[2][2])

    # 二维转一维
    c = [j for x in b for j in x]
    print(c)

    # if条件
    d = [x for x in range(10) if x % 2 == 0]
    print(d)

    # if-else条件
    e = [-x if x % 2 == 0 else x for x in range(10)]
    print(e)


def list_operation():
    a = [x for x in range(1, 6)]
    b = [x for x in range(6, 10)]
    print(a)
    print(a * 2)
    print(a + b)

    print(id(a))
    a = a + b  # a被重新赋值，地址改变
    print(id(a))
    a += b  # 等价于a.extend(b)    a的地址不变
    print(id(a))
    a.extend(b)  # a的地址不变
    print(id(a))

    # del
    print(a)
    del a[0]
    
    # 切片
    print(a)
    print(a[2:6])


# list_api()
# list_generator()
list_operation()
