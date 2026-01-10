# Author: Sean W
# 2026年01月04日18时37分58秒
# wanjx0701@gmail.com

import sys

sys.setrecursionlimit(1000000)


def factorial(n):
    if n == 0:
        return 1
    else:
        return n + factorial(n - 1)


print(factorial(199999))
