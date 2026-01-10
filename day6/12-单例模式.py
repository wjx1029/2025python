# Author: Sean W
# 2026年01月05日18时37分52秒
# wanjx0701@gmail.com


class MusicPlayer(object):
    instance = None  # 单例模式的实现

    def __new__(cls, *args, **kwargs):
        # 判断是否已经创建过实例
        if cls.instance is None:
            cls.instance = super().__new__(cls)  # 父亲的new类似于C的malloc
        return cls.instance

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    player1 = MusicPlayer('player1')
    player2 = MusicPlayer('player2')
    print(player1.name)
    print(player2.name)
    print(player1 is player2)  # True
