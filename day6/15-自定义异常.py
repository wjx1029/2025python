# Author: Sean W
# 2026年01月05日19时12分32秒
# wanjx0701@gmail.com


def input_password():
    # 1. 提示用户输入密码
    pwd = input("请输入密码：")

    # 2. 判断密码长度 >= 8，返回用户输入的密码
    if len(pwd) >= 8:
        return pwd
    raise Exception("密码长度必须大于等于8位！")


if __name__ == '__main__':
    try:
        password = input_password()
        print("密码为：", password)
    except Exception as e:
        print(e)

    try:
        assert 1 == 2, "1不等于2"
    except Exception as e:
        print(e)
