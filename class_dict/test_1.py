# encoding: utf-8
"""
@author: jinlin.xiao
@file: test_1.py
@time: 2019/6/28 9:03 AM
@desc:

将字典转成类
这种方法不能通过 instance 直接获取 属性，需要记住属性名字，不方便

"""


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def test_1():
    args = {'a': 1, 'b': 2}
    s = Struct(**args)
    print(s.a)
    print(s.b)


