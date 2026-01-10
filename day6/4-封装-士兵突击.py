# Author: Sean W
# 2026年01月05日10时28分10秒
# wanjx0701@gmail.com


class Gun:
    def __init__(self, model):
        self.model = model
        self.bullet = 0

    def add_bullet(self, num):
        self.bullet = num

    def shoot(self):
        if self.bullet > 0:
            self.bullet -= 1
            print("Shoot!")
        else:
            print("No bullet!")


class Soldier:
    def __init__(self, name, gun: Gun):
        self.name = name
        self.gun = gun

    def fire(self):
        if self.gun is None:
            print("No gun!")
            return

        self.gun.shoot()


ak47 = Gun("AK47")
ak47.add_bullet(10)
ak47.shoot()
soldier1 = Soldier("John", ak47)
soldier1.fire()
