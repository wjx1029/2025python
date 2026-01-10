# Author: Sean W
# 2026年01月06日18时26分20秒
# wanjx0701@gmail.com


import sys


def write_hello(file_path):
    file = open(file_path, 'w+', encoding='utf-8')
    file.write('Hello')
    file.close()


if __name__ == '__main__':
    write_hello(sys.argv[1])
    print(type(sys.argv))
    print(sys.argv)
    print(len(sys.argv))
