# Author: Sean W
# 2026年01月08日19时57分44秒
# wanjx0701@gmail.com
import random
import time
import sys

sys.setrecursionlimit(1000000)


class Sort:
    def __init__(self, n):
        """
        n是排序的数的数量
        :param n:
        """
        self.arr = [0] * n  # 长度为n，值为全0的列表
        self.len = n
        self.random_create()

    def __str__(self):
        return str(self.arr)

    def random_create(self):
        for i in range(self.len):
            self.arr[i] = random.randint(0, 99)

    def partition(self, left, right):
        arr = self.arr
        k = left
        random_pos = random.randint(left, right)  # 如何避免陷入最坏时间复杂度
        arr[random_pos], arr[right] = arr[right], arr[random_pos]
        for i in range(left, right):
            if arr[i] < arr[right]:
                arr[k], arr[i] = arr[i], arr[k]  # 某个位置的值小于分割值，就拿它和k指向的位置交换
                k += 1
        arr[k], arr[right] = arr[right], arr[k]
        return k

    def quick_sort(self, left, right):
        if left < right:
            mid = self.partition(left, right)
            self.quick_sort(left, mid - 1)
            self.quick_sort(mid + 1, right)

    def adjust_heap(self, index, arr_len):
        """
        把某个子树调整为大根堆
        :param pos: 被调整的元素位置，是父亲
        :param arr_len: 当时列表总长度
        :return:
        """
        arr = self.arr
        dad = index
        son = dad * 2 + 1
        while son < arr_len:  # 左孩子小于列表长度
            if son + 1 < arr_len and arr[son] < arr[son + 1]:  # 判断右孩子存在，且右孩子大于左孩子
                son += 1
            if arr[son] > arr[dad]:
                arr[son], arr[dad] = arr[dad], arr[son]
                dad = son
                son = dad * 2 + 1
            else:
                break

    def heap_sort(self):
        arr = self.arr
        len = self.len
        # 建立大根堆
        for i in range(self.len // 2 - 1, -1, -1):
            self.adjust_heap(i, self.len)

        for i in range(self.len - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            len -= 1
            self.adjust_heap(0, len)

    def count_time(self, sort_func, *args, **kwargs):
        """
        回调函数
        :param sort_func:
        :param args:
        :param kwargs:
        :return:
        """
        start = time.time()
        sort_func(*args, **kwargs)
        end = time.time()
        print(end - start)


def main(n):
    list1 = Sort(n)
    list2 = Sort(n)
    print(f'original:\t{list1}')
    list1.quick_sort(0, list1.len - 1)
    print(f'quick sort: {list1}')

    print(f'original:\t{list2}')
    list2.heap_sort()
    print(f'heap_sort:  {list2}')

    print('-' * 50)

    list1 = Sort(100000)
    list2 = Sort(100000)
    list1.count_time(list1.quick_sort, 0, list1.len - 1)
    list2.count_time(list2.heap_sort)


if __name__ == '__main__':
    main(10)
