# Author: Sean W
# 2026年01月05日18时41分36秒
# wanjx0701@gmail.com

import test_exception_module as tem


def use_exception1():
    try:
        num = int(input("请输入一个数字："))
        print("你输入的数字是：", num)
    except:
        print("输入的必须是一个整型数字，请重新输入！")


def use_exception2():
    """
    掌握不同的异常类型，可以跳转到不同的分支上
    :return:
    """
    try:
        num = int(input("请输入一个数字："))
        res = 10 / num
        print(res)
    except ZeroDivisionError:
        print("不能除以0！")
    except ValueError:
        print("输入的必须是一个整型数字，请重新输入！")


def use_exception3():
    """
        掌握不同的异常类型，可以跳转到不同的分支上
        :return:
        """
    try:
        num = int(input("请输入一个数字："))
        res = 10 / num
        print(res)
    except ZeroDivisionError:
        print("不能除以0！")
    except Exception as e:  # 捕获所有异常,e 代表异常对象的别名
        print("出现了未知错误：", e)


def use_exception4():
    """
    学习else和finally
    :return:
    """
    try:
        num = int(input("请输入一个数字："))
        res = 10 / num
        print(res)
    except ValueError:
        print("请输入正确的整数")
    except ZeroDivisionError:
        print("不能除以0！")
    except Exception as e:  # 捕获所有异常,e 代表异常对象的别名
        print("出现了未知错误：", e)
    else:
        print("程序正常执行")  # 只有没有异常才会执行
    finally:
        print("程序执行结束")  # 不受return影响，无论是否有异常都执行


def use_exception5():
    """
    如何捕获异常发生的文件（模块）和具体行数
    :return:
    """
    try:
        tem.test()
    except Exception as e:
        tb = e.__traceback__
        while tb.tb_next:
            tb = tb.tb_next
        print("出现异常：", e)
        print("异常发生在文件：", tb.tb_frame.f_code.co_filename)
        print("异常发生在第", tb.tb_lineno, "行")


def use_exception6():
    """
    如何捕获异常发生的文件（模块）和具体行数
    :return:
    """
    try:
        tem.test()
    except Exception as e:
        import traceback
        # 打印异常信息
        print("异常信息：", e)

        # 获取完整的回溯信息
        tb = e.__traceback__
        while tb.tb_next:  # 循环到异常发生的最后一层，即 test 函数内部
            tb = tb.tb_next

        # 输出异常发生的文件、行号和代码内容
        filename = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno
        func_name = tb.tb_frame.f_code.co_name

        print(f"异常发生的文件：{filename}")
        print(f"异常发生的函数：{func_name}")
        print(f"异常发生的行数：{lineno}")

        # 如果需要打印具体行内容，可以用 open 读取
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"发生异常的代码：{lines[lineno - 1].strip()}")


# use_exception1()
# use_exception2()
# use_exception3()
# use_exception4()
# use_exception5()
use_exception6()
