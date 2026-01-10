# Author: Sean W
# 2026年01月06日18时34分55秒
# wanjx0701@gmail.com

def read_conf():
    """
    读取配置文件
    :return:
    """
    file = open('file5', 'r+', encoding='utf-8')
    text_info = file.read()
    print(text_info)
    my_dict = eval(text_info)
    print(my_dict)
    print(type(my_dict))
    file.close()


read_conf()
