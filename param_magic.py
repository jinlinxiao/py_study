# encoding: utf-8
"""
@author: jinlin.xiao
@file: param_magic.py
@time: 2019/7/11 2:47 PM
@desc:

参数传递的魔法
不同的参数传递方式

"""


def send_req(account, product_id, *args, **kwargs):
    print("account=%s&product_id=%s" % (account, product_id))
    if args:
        print("%s" % args)
    if kwargs:
        print("%s" % kwargs)


def send_get(account, product_id, wait=12, **kwargs):
    print("account=%s&product_id=%s&wait=%s" % (account, product_id, wait))
    if kwargs:
        print("%s" % kwargs)


def test_send_req():
    send_req('aaa', 123)


def test_send_req_args():
    param = ['bbb', 345, 567]
    send_req(*param)


def test_send_req_kwargs():
    param = {
        'account': 'ccc',
        'product_id': 888,
        'other': 'other'
    }
    send_req(**param)


def test_send_req_kwargs_no_sort():
    param = {
        'first': 123,
        'account': 'ccc',
        'other': 'other',
        'product_id': 888,
        'other2': 'other2'
    }
    send_req(**param)


def test_send_get_kwargs():
    param = {
        'account': 'ccc',
        'product_id': 888,
        'other': 'other'
    }
    send_get(**param)


def test_send_get_kwargs_no_sort():
    param = {
        'first': 123,
        'account': 'ccc',
        'other': 'other',
        'product_id': 888,
        'other2': 'other2'
    }
    send_get(**param)
