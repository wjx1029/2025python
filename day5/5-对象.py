# Author: Sean W
# 2026年01月04日18时41分17秒
# wanjx0701@gmail.com


class Person:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def say_hello(self):
        print("Hello, my name is " + self.name + "!")

    def say_age(self):
        print("I am " + str(self.age) + " years old.")

    def say_weight(self):
        print("I weigh " + str(self.weight) + " pounds.")


p1 = Person("Alice", 25, 120)
print(p1.name, p1.age, p1.weight)
p1.say_hello()
p1.say_age()

p1.name = "Bob"
p1.say_hello()

print('-' * 50)
print(dir(p1))
print('-' * 50)
print(dir(Person))
