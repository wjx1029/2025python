# Aurthor: Sean W
# 2026年01月02日22时29分53秒
# wanjx0701@gmail.com


def print1(n):
    for i in range(n):
        for j in range(i):
            print("*", end='')
        print('\n')


def print2(char, n):
    print(char * n)


def print3():
    for i in range(8):
        print("⬛⬜" * 4 if i % 2 == 0 else "⬜⬛" * 4)


if __name__ == '__main__':
    print2('-', 50)
