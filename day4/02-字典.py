# Author: Sean W
# 2026年01月03日09时26分29秒
# wanjx0701@gmail.com

def dict_api():
    mydict = {'name': 'xiaomi', 'age': 18, 'gender': True, 'height': 1.75, 22: 33}
    print(mydict)

    # 按键查询
    print(mydict.get('name'))
    print(mydict['age'])

    # 删除/随机删除popitem()
    print(mydict.pop(22))
    print(mydict)

    # 增加和修改
    mydict['id'] = '1123556'
    mydict['age'] = 20
    print(mydict)

    # 复制,清除
    copy_dict = mydict.copy()
    print(copy_dict)
    copy_dict.clear()
    print(len(copy_dict))

    # 合并字典
    new_dict = {'age': 23, 'grade': 99}
    mydict.update(new_dict)
    print(mydict)


def dict_iter():
    mydict = {'name': 'xiaomi', 'age': 18, 'gender': True, 'height': 1.75, 22: 33}

    for key in mydict:
        print(key, mydict[key])
    print('-' * 50)
    for kv in mydict.items():  # 以元组形式迭代
        print(kv)
    print('-' * 50)
    for k, v in mydict.items():  # 拆包
        print(k, v)
    print('-' * 50)
    print(mydict.keys())
    print(mydict.values())
    print(mydict.items())


# dict_api()
dict_iter()
