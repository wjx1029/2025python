# Author: Sean W
# 2026年01月09日19时42分57秒
# wanjx0701@gmail.com
import re


def simple():
    """
    简单匹配
    """
    result = re.match(r'hello', 'hello world')
    if result:
        print(result.group())
    else:
        print('No match')


def single():
    """
    单个字符匹配
    """
    ret = re.match(".", "M")
    print(ret.group())

    ret = re.match("t.o", "too")
    print(ret.group())

    ret = re.match("t.o", "two")
    print(ret.group())

    print('-' * 50)

    # 大小写h都可以的情况
    ret = re.match('[hH]','hello world')
    print(ret.group())

    ret = re.match("[hH]", "Hello Python")
    print(ret.group())

    ret = re.match("[hH]ello Python", "Hello Python")
    print(ret.group())

    # 匹配0-9
    ret = re.match("[0-9]Hello Python", "6Hello Python")
    print(ret.group())

    ret = re.match("[0-35-9]Hello Python", "6Hello Python")
    print(ret.group())
    print('-' * 50)

    # 使用\d进行匹配
    ret = re.match(r"嫦娥\d号", "嫦娥1号发射成功")
    print(ret.group())

    ret = re.match(r"嫦娥\d号", "嫦娥2号发射成功")
    print(ret.group())

    ret = re.match(r"嫦娥\d号", "嫦娥3号发射成功")
    print(ret.group())
    print('-' * 50)

    # 使用\D进行匹配
    try:
        ret = re.match(r"嫦娥\D号", "嫦娥2号发射成功")
        print(ret.group())
    except:
        print('No match')
    print('-' * 50)

    # 使用\w进行匹配
    ret = re.match(r"\w+Python", "HelloPython")
    print(ret.group())

    ret = re.match(r"\w+Python", "Hello_Python")
    print(ret.group())

    ret = re.match(r"\w+Python", "Hello9Python")
    print(ret.group())
    print('-' * 50)

    # 使用\W进行匹配
    ret = re.match(r"\W+Python", " -Python")
    print(ret.group())

    try:
        ret = re.match(r"\W+Python", "HelloPython")
        print(ret.group())
    except:
        print('No match')
    print('-' * 50)

    # 使用\s进行匹配
    ret = re.match(r"\s+Python", "  Python")
    print(ret.group())

    ret = re.match(r"\s+Python", "      Python")
    print(ret.group())

    ret = re.match(r"\s+Python", "\tPython")
    print(ret.group())
    print('-' * 50)

    # 使用\S进行匹配
    ret = re.match(r"\S+Python", "HelloPython")
    print(ret.group())

    try:
        ret = re.match(r"\S+Python", "  Python")
        print(ret.group())
    except:
        print('No match')
    print('-' * 50)


def more_char():
    r"""
    匹配更多字符
    * 匹配0个或多个字符
    + 匹配1个或多个字符
    ? 匹配0个或1个字符
    {n} 匹配n个字符
    {n,} 匹配n个或多个字符
    {n,m} 匹配n-m个字符
    [] 匹配字符集
    [^] 匹配不在字符集中的字符
    | 匹配或
    () 分组
    \ 转义字符
    ^ 匹配字符串开始
    $ 匹配字符串结束
    """
    ret = re.match("[A-Z][a-z]*", "M")
    print(ret.group())

    ret = re.match("[A-Z][a-z]*", "MnnM")
    print(ret.group())

    ret = re.match("[A-Z][a-z]*", "Aabcdef")
    print(ret.group())
    print('-' * 50)

    names = ["name1", "_name", "2_name", "__name__"]
    for name in names:
        ret = re.match(r'[a-zA-Z_]+\w*', name)
        if ret:
            print(f'{ret.group()} 是正确的')
        else:
            print(f'{name} 不符合命名规范')
    print('-' * 50)

    ret = re.match(r'[1-9]?[0-9]','7')
    print(ret.group())

    ret = re.match(r'[1-9]?\d','33')
    print(ret.group())

    ret = re.match(r'[1-9]?\d','09')
    print(ret.group())
    print('-' * 50)

    ret = re.match("[a-zA-Z0-9_]{6}", "12a3g45678")
    print(ret.group())

    ret = re.match("[a-zA-Z0-9_]{8,20}", "1ad12f23s*34455ff66")
    print(ret.group())

    ret = re.match("[a-zA-Z0-9_]{8,20}", "1ad12f23s34455ff66")
    print(ret.group())


def start_end():
    """
    匹配字符串开始和结束
    """

    # 符合163的邮箱找出来
    email_list = ["xiaoWang@163.com", "xiaoWang@163.comheihei", ".com.xiaowang@qq.com"]
    for email in email_list:
        ret = re.match(r'\w{4,20}@163\.com$', email)    # 注意这里的\. 不是. ,  $ 匹配字符串结束
        if ret:
            print(f'{email} 是163邮箱')
        else:
            print(f'{email} 不是163邮箱')
    print('-' * 50)

    # 匹配0到99
    ret = re.match(r'[1-9]?\d$','99')
    if ret:
        print(f'{ret.group()} 是0到99的数字')
    else:
        print(f'不是0到99的数字')

    ret = re.match(r'[1-9]?\d$','0')
    if ret:
        print(f'{ret.group()} 是0到99的数字')
    else:
        print(f'不是0到99的数字')

    ret = re.match(r'[1-9]?\d$','100')
    if ret:
        print(f'{ret.group()} 是0到99的数字')
    else:
        print('不是0到99的数字')


def match_group():
    """
    匹配分组
    """

    # 匹配0到100的数字
    ret = re.match(r'[1-9]?\d$|100', '99')
    if ret:
        print(f'{ret.group()} 是0到100的数字')
    else:
        print(f'不是0到100的数字')

    ret = re.match(r'[1-9]?\d$|100', '100')
    if ret:
        print(f'{ret.group()} 是0到100的数字')
    else:
        print(f'不是0到100的数字')

    ret = re.match(r'[1-9]?\d$|100', '101')
    if ret:
        print(f'{ret.group()} 是0到100的数字')
    else:
        print('不是0到100的数字')
    print('-' * 50)

    # 匹配1到99,匹配分组，依次匹配，写到前面的会先匹配
    ret =re.match(r'[1-9][0-9]|[1-9]','11')
    if ret:
        print(f'{ret.group()} 是1到99的数字')
    else:
        print(f'不是1到99的数字')

    ret = re.match(r'[1-9][0-9]|[1-9]','0')
    if ret:
        print(f'{ret.group()} 是1到99的数字')
    else:
        print(f'不是1到99的数字')
    print('-' * 50)

    # 匹配163、126、qq邮箱
    ret = re.match(r"\w{4,20}@(163|126|qq)\.com", "test@qq.com")
    print(ret.group())

    ret = re.match(r"\w{4,20}@(163|126|qq)\.com", "test@126.com")
    print(ret.group())
    print('-' * 50)

    # 代表没有遇到小横杠 - 就一直进行匹配，一直匹配下去
    ret = re.match(r'([^-]+)-(\d+)','010-12345678')
    print(ret.group())
    print(ret.group(0))
    print(ret.group(1))
    print(ret.group(2))
    print('-' * 50)

    ret = re.match(r"<[a-zA-Z]*>\w*</[a-zA-Z]*>", "<html>hh</htmla>")
    print(ret.group())

    # \1 引用分组
    ret = re.match(r"<([a-zA-Z]*)>\w*</\1*>", "<html>hh</html>")
    print(ret.group())

    # ?P<name> 匹配分组并命名, 后面使用(?P=name) 引用分组
    ret = re.match(r"<(?P<tag>[a-zA-Z]*)>\w*</(?P=tag)>", "<html>hh</html>")
    print(ret.group())
    print('-' * 50)

    labels = ["<html><h1>www.cskaoyan.com</h1></html>", "<html><h1>www.cskaoyan.com</h2></html>"]
    for label in labels:
        ret = re.match(r'<(\w*)><(\w*)>.*</\2></\1>', label)
        if ret:
            print(f'{label} 是正确的标签')
        else:
            print(f'{label} 不是正确的标签')
    print('+'*50)
    for label in labels:
        ret = re.match(r'<(?P<tag1>\w*)><(?P<tag2>\w*)>.*</(?P=tag2)></(?P=tag1)>',label)
        if ret:
            print(f'{label} 是正确的标签')
        else:
            print(f'{label} 不是正确的标签')
    print('-' * 50)



if __name__ == '__main__':
    # simple()
    # single()
    # more_char()
    # start_end()
    match_group()