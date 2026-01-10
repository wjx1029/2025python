# Aurthor: Sean W
# 2026年01月02日09时00分30秒
# wanjx0701@gmail.com
import random


def use_branch():
    a = int(input('input a number:'))
    b = int(input('input another number:'))

    if a > b:
        print('%d > %d' % (a, b))
    elif a < b:
        print('%d < %d' % (a, b))
    else:
        print('%d = %d' % (a, b))

    # 安检演练
    has_ticket = True
    knife_length = 18
    has_bomb = False

    if has_ticket:
        if knife_length <= 18 and not has_bomb:
            print('通过安检')
        else:
            print('未通过安检')
    else:
        print('未购票')
    # 安检演练

    # 石头剪刀布
    while True:
        player = int(input('请出拳（1.石头，2.剪刀，3.布，4.结束）:'))
        if player == 4:
            break
        computer = random.randint(1, 3)

        if (player == 1 and computer == 2) or (player == 2 and computer == 3) or (player == 3 and computer == 1):
            print('欧耶，我赢了')
        elif player == computer:
            print('平局，再来一盘')
        else:
            print('你只是运气好罢了')
    # 石头剪刀布


def func_for(n):
    mylist = [3, 5, 9, 16]
    for i in mylist:
        print(i, end=' ')
    print('\n%d' % i)  # for循环中的i可以在循环外使用

    # for_else
    for i in range(10):
        if i == n:
            print('find')
            break
    else:
        print('not find')


def func_while(n):
    while n > 0:
        print('hello python')
        n = n - 1
    print(f'循环结束，n的值:{n}')


# use_branch()
func_for(12)
# func_while(5)
