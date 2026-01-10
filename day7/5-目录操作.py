# Author: Sean W
# 2026年01月06日17时11分30秒
# wanjx0701@gmail.com

import os


def use_rename():
    try:
        os.rename('file3', 'file4')
    except Exception:
        os.rename('file4', 'file3')


def use_remove():
    os.remove('file3')


def use_dir_func():
    file_list = os.listdir('')
    print(file_list)
    # os.mkdir('dir1')
    # os.mkdir('dir2')
    print(os.getcwd())

    os.chdir('dir2')
    # os.mkdir('dir3')
    file = open('file', 'wb')
    file.close()
    print(os.path.isdir('dir3'))


# use_rename()
# use_remove()
use_dir_func()
