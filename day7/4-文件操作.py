# Author: Sean W
# 2026年01月06日10时29分09秒
# wanjx0701@gmail.com
import os


def open_r():
    """
    以只读方式打开文件。文件的指针将会放在文件的开头，这是默认模式。如果文件不存在，抛出异常
    :return:
    """
    file = open('file2.txt', mode='r', encoding='utf-8')
    text = file.read()  # 读出来是字符串
    print(text)
    file.close()


def open_r_jia():
    """
    + 以读写方式打开文件。文件的指针将会放在文件的开头。如果文件不存在，抛出异常(写入时，文件位置指针会跳转到尾部）
    :return:
    """
    file = open('file2.txt', mode='r+', encoding='utf-8')
    text = file.read()  # 读出来是字符串
    print(text)
    file.write('aiaiaiaiai')
    file.close()


def open_w():
    """
    以只写方式打开文件。如果文件存在会被覆盖。如果文件不存在，创建新文件
    :return:
    """
    file = open("file3", mode='w', encoding='utf-8')
    file.write('hello world')
    file.close()


def open_a():
    """
    以追加方式打开文件。如果该文件已存在，文件指针将会放在文件的结尾。如果文件不存在，创建新文件进行写入
    :return:
    """
    file = open("file3", mode='a', encoding='utf-8')
    file.write('how')
    file.close()


def use_readline():
    """
    一次读一行
    :return:
    """
    file = open("file2.txt", mode='r', encoding='utf-8')
    text = file.readline()
    while text:
        print(text, end='')
        text = file.readline()


def seek_start():
    """
    相对于文件起始位置偏移
    :return:
    """
    file = open('file1', mode='r+', encoding='utf8')
    file.seek(5, os.SEEK_SET)  # 相对于开头偏移5个字节，汉字偏移必须是3的整数倍
    text = file.read(5)
    print(text)
    file.close()


def seek_end():
    """
    相对于文件尾部偏移
    :return:
    """
    file = open('file1', mode='r+', encoding='utf8')
    file.seek(0, os.SEEK_END)  # 相对于尾部偏移,文本模式第一个参数只能为0
    text = file.read(5)
    print(text)
    file.close()


def seek_cur():
    """
    相对于当前位置不动
    :return:
    """
    file = open('file1', mode='r+', encoding='utf8')
    file.seek(0, os.SEEK_CUR)  # 相对于当前位置偏移,文本模式第一个参数只能为0
    text = file.read(5)
    print(text)
    file.close()


def seek_b_cur():
    """
    相对于当前位置偏移（读取的是字节流），读取图片，音频，视频
    :return:
    """
    file = open('file1', mode='rb+')
    file.seek(5, os.SEEK_CUR)
    file.seek(-2, os.SEEK_CUR)
    b = file.read()
    print(b)

    file.seek(-3, os.SEEK_END)
    print(file.read())
    file.close()


def copy_file():
    file1 = open('google.png', mode='rb+')
    file2 = open('copy_png.png', mode='wb')
    b = file1.read()
    file2.write(b)
    file1.close()
    file2.close()


# open_r()
# open_r_w()
# open_w()
# open_a()
# use_readline()

# seek_start()
# seek_end()
# seek_cur()
# seek_b_cur()

copy_file()
