#!/usr/bin/python3
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: test.py
@time: 2020/12/17 20:24
@describe: 测试方法
"""
import sys
import os

from config.MysqlContent import DBHelper
from msgStaticClass import MsgStaticClass

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")

def test():
    # 生成姓名
    for i in range(10):
        print(c.random_name())
        print(c.name())
    # 生成性别
    print(c.random_sex())
    # 生成地址
    print(c.address())
if __name__ == '__main__':
    c = MsgStaticClass("zh_cn")
    test()
