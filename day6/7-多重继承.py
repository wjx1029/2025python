# Author: Sean W
# 2026年01月05日17时47分32秒
# wanjx0701@gmail.com


class A:
    def test(self):
        print('A test')

    def demo(self):
        print('A demo')


class B:
    def test(self):
        print('B test')

    def demo(self):
        print('B demo')


class C(A, B):
    def test(self):
        print('C test')


class D(A, B):
    def test(self):
        super().test()
        B.demo(self)
        print('D test')


c = C()
c.test()
c.demo()
d = D()
d.test()

print(C.__mro__)  # 输出C的MRO mro是method resolution order的缩写
print(D.__mro__)  # 输出D的MRO
