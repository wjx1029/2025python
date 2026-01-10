# Author: Sean W
# 2026年01月06日17时46分52秒
# wanjx0701@gmail.com

import os
from time import strftime
from time import gmtime


def scan_dir(cur_path, width):
    file_list = os.listdir(cur_path)
    for file in file_list:
        print(' ' * width, file)
        new_path = cur_path + '/' + file  # 把当前路径和文件名拼接在一起
        if os.path.isdir(new_path):
            scan_dir(new_path, width + 4)


def use_stat(file_path):
    file_info = os.stat(file_path)
    print('文件名:', file_path)
    print('文件大小:', file_info.st_size, '字节')
    print('文件权限:', oct(file_info.st_mode))
    print('文件创建时间:', strftime('%Y-%m-%d %H:%M:%S', gmtime(file_info.st_ctime)))
    print('文件最后访问时间:', strftime('%Y-%m-%d %H:%M:%S', gmtime(file_info.st_atime)))
    print('文件最后修改时间:', strftime('%Y-%m-%d %H:%M:%S', gmtime(file_info.st_mtime)))
    print('-' * 50)


# scan_dir('dir_for_iter', 0)
# print('-' * 50)
# scan_dir('.', 0)

use_stat('file1')
use_stat('file2.txt')
use_stat('dir_for_iter')
