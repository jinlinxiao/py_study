# encoding: utf-8
"""
@author: jinlin.xiao
@file: test_namedtuple.py
@time: 2019/6/28 9:07 AM
@desc:
"""

from collections import namedtuple

# 定义一个namedtuple类型User，并包含name，sex和age属性。
User = namedtuple('User', ['name', 'sex', 'age'])


def test_1():
    # 创建一个User对象
    user1 = User(name='kongxx', sex='male', age=21)
    print(user1)

    # 也可以通过一个list来创建一个User对象，这里注意需要使用"_make"方法
    user = User._make(['kongxx', 'male', 21])

    print(user)
    # User(name='user1', sex='male', age=21)

    # 获取用户的属性
    print(user.name)
    print(user.sex)
    print(user.age)

    # 修改对象属性，注意要使用"_replace"方法
    user = user._replace(age=22)
    print(user)
    # User(name='user1', sex='male', age=21)

    # 将User对象转换成字典，注意要使用"_asdict"
    print(user._asdict())
    # OrderedDict([('name', 'kongxx'), ('sex', 'male'), ('age', 22)])


def test_2():
    test_d = {
        'name': 'name1',
        'sex': 'male',
        'age': 22
    }
    user = User(**test_d)
    print(user)


def test_unexpect_key():
    test_e = {
        'name': 'name1',
        'sex': 'male',
        'age': 22,
        'aaa': 344
    }
    user = User(**test_e)
    print(user)

