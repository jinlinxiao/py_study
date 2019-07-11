# encoding: utf-8
"""
@author: jinlin.xiao
@file: recipe.py
@time: 2019/7/4 6:23 PM
@desc:

根据param初始化不同实例

"""


class A(object):
    def __init__(self):
        print('This is A')

    def foo(self):
        self.ret()
        print("foo")

    def ret(self):
        print("A ret")


class B(object):
    def __init__(self):
        print('This is B')

    def foo(self):
        self.ret()
        print("bar")

    def ret(self):
        print("B ret")


def get_object(cond):
    if cond:
        classname = 'A'
    else:
        classname = 'B'
    obj = globals()[classname]
    return obj()


myobject = get_object(1)
myobject.foo()
# print dir(myobject)
#
# print

a = A()
a.foo()
# print dir(a)
#
# print

myobject = get_object(0)
# myobject.ret()
myobject.foo()
# print dir(myobject)
#
# print

b = B()
b.foo()
# print dir(b)
