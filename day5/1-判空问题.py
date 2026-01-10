# Author: Sean W
# 2026年01月04日18时27分54秒
# wanjx0701@gmail.com


# 容器空就是假，非空就是真
# 0、None、False 都是假的
# 容器空 != 0、None、False

if []:
    print("非空列表")
else:
    print("空列表")

if {}:
    print("非空字典")
else:
    print("空字典")

print(bool([]))  # False
print(bool({}))  # False
print(bool(0))  # False
print(bool(None))  # False
print(bool(False))  # False

print([] == None)
print([] == False)
print([] == 0)
