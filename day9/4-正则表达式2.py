# Author: Sean W
# 2026年01月09日20时49分44秒
# wanjx0701@gmail.com

import re


def re_research():
    """
    只能搜第一个匹配的结果
    """
    ret = re.search(r"\d+", "阅读次数为 9999,点赞888")
    print(ret.group())


def re_sub():
    """
    替换字符串
    """
    ret = re.sub(r"\d+", '998', "python = 997")
    print(ret)

    ret = re.sub(r"\d+", lambda x:str(int(x.group()) * 2), "python = 997")
    print(ret)
    print('-' * 50)

    # 只替换前两个匹配的结果
    text = "apple apple apple apple"
    pattern = r"apple"
    replacement = "orange"
    ret = re.sub(pattern, replacement, text, count=2)
    print(ret)

    print('-' * 50)

    long_text = """<div>
            <p>岗位职责：</p>
    <p>完成推荐算法、数据统计、接口、后台等服务器端相关工作</p>
    <p><br></p>
    <p>必备要求：</p>
    <p>良好的自我驱动力和职业素养，工作积极主动、结果导向</p>
    <p>&nbsp;<br></p>
    <p>技术要求：</p>
    <p>1、一年以上 Python 开发经验，掌握面向对象分析和设计，了解设计模式</p>
    <p>2、掌握HTTP协议，熟悉MVC、MVVM等概念以及相关WEB开发框架</p>
    <p>3、掌握关系数据库开发设计，掌握 SQL，熟练使用 MySQL/PostgreSQL 中的一种<br></p>
    <p>4、掌握NoSQL、MQ，熟练使用对应技术解决方案</p>
    <p>5、熟悉 Javascript/CSS/HTML5，JQuery、React、Vue.js</p>
    <p>&nbsp;<br></p>
    <p>加分项：</p>
    <p>大数据，数理统计，机器学习，sklearn，高性能，大并发。</p>

            </div>
        """
    pattern = r'<\w*>|</\w*>|&nbsp;|\s|\n'
    ret = re.sub(pattern, '', long_text)
    print(ret)


def find_k_th_match(pattern, text, k):
    """
    找到第k个匹配的结果
    """
    matches = re.finditer(pattern, text)
    match = next(matches)
    for i in range(k-1):
        try:
            match = next(matches)
        except StopIteration:
            return None
    return match.group()


def re_finditer():
    """
    使用finditer
    """
    text = "abc123def456ghi789"
    pattern = r"\d+"
    second_match = find_k_th_match(pattern, text, 2)
    print(second_match)


def re_findall():
    """
    找所有匹配的结果
    """
    s = 'hello world, now is 2020/7/20 18:48, 现在是2020年7月20日18时48分。'
    ret_s = re.sub(r'年|月', r'/', s)
    ret_s = re.sub(r'日', r' ', ret_s)
    ret_s = re.sub(r'时|分', r':', ret_s)
    print(ret_s)
    # findall 内部的设计机制，在分组前面加?:
    pattern = re.compile(r'\d{4}/[01]?[0-9]/[1-3]?[0-9]\s(?:0[0-9]|1[0-9]|2[0-4])\:[0-5][0-9]')
    ret = pattern.findall(ret_s)
    print(ret)
    pattern1 = re.compile(r'\d{4}/[01]?[0-9]/[1-3]?[0-9]\s(0[0-9]|1[0-9]|2[0-4])\:[0-5][0-9]')
    # search 没问题
    ret1 = pattern1.search(ret_s)
    print(ret1.group())


def re_split():
    """
    字符串分割
    """
    ret = re.split(r"[: ]", "info:xiaoZhang 33 shandong")
    print(ret)


def use_greedy():
    s = "This is a number 234-235-22-423"
    ret = re.match(r".+?(\d+-\d+-\d+-\d+)", s)
    print(ret.group(1))
    print(re.match(r"aa(\d+)", "aa2343ddd").group(1))

    print(re.match(r"aa(\d+?)", "aa2343ddd").group(1))

    print(re.match(r"aa(\d+)ddd", "aa2343ddd").group(1))

    print(re.match(r"aa(\d+?)ddd", "aa2343ddd").group(1))


def use_r():
    """
    r的作用, 原生字串
    :return:
    """
    mm = "c:\\a\\b\\c"
    print(mm)
    print(re.match(r"c:\\", mm).group())


def use_option():
    print(re.match(r'\w*','abc函',flags=re.A).group())
    print(re.match(r'\w*', 'abc函').group())
    print('-'*50)
    print(re.match(r'a*', 'aaaAaA',flags=re.I).group())
    print(re.match(r'a*','aaaAaA').group())
    print('-' * 50)
    print(re.match(r'.*','abc\ndef',flags=re.S).group())
    print(re.match(r'.*', 'abc\ndef').group())



if __name__ == '__main__':
    # re_research()
    # re_sub()
    # re_finditer()
    # re_findall()
    # re_split()
    # use_greedy()
    # use_r()
    use_option()