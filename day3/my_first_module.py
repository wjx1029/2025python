# Aurthor: Sean W
# 2026年01月02日10时54分04秒
# wanjx0701@gmail.com

# 模块名不能与系统模块名重名

name = 'Sean'


def print_line(char, n):
    print(char * n)
    # print(num)


if __name__ == '__main__':
    a = '*'
    times = 50
    print_line(a, times)
    num = 10
