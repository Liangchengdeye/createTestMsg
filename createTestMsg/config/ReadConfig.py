#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: ReadConfig.py 
@time: 2018/9/25 19:51 
@describe: 读取各类配置文件
"""
import sys
import os
from yaml import load
import platform
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


class ReadConfig:
    """ 读取各类YAM配置文件"""

    @staticmethod
    def get_conf(path_name):
        system = platform.system()
        if system == 'Windows':
            config_path = os.path.join(os.path.dirname(__file__).replace('\config', ''), path_name)
        if system == 'Linux':
            config_path = os.path.join(os.path.dirname(__file__).replace('/config', ''), path_name)
        with open(config_path, encoding="utf-8") as f:
            cont = f.read()
        return load(cont)
