#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: TimeStamp.py 
@time: 2019/5/16 15:05 
@describe: 时间戳等时间操作类方法
"""
import sys
import os
from datetime import datetime
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


class TimeStamp:

    @staticmethod
    def now_time_format(msg, msg_flag=1, type_flag=None):
        """
        日期时间戳
        :param msg: 消息体
        :param msg_flag: 消息体位置，0：消息在左，时间跟后；1：时间戳在前，消息在后
        :param type_flag: 打印时间格式：默认：年/月/日；0：时-分-秒；1：年/月/日 时-分-秒
        :return:
        """
        now_time = datetime.now()
        if msg_flag == 0:
            if type_flag is None:
                msg_back = msg + " [" + now_time.strftime('%Y/%m/%d') + "]"
            elif type_flag == 0:
                msg_back = msg + " [" + now_time.strftime('%H:%M:%S') + "]"
            elif type_flag == 1:
                msg_back = msg + " [" + now_time.strftime('%Y/%m/%d %H:%M:%S') + "]"
            else:
                raise Exception("type_flag only is 0 or 1")
        elif msg_flag == 1:
            if type_flag is None:
                msg_back = "[" + now_time.strftime('%Y/%m/%d') + "] " + msg
            elif type_flag == 0:
                msg_back = "[" + now_time.strftime('%H:%M:%S') + "] " + msg
            elif type_flag == 1:
                msg_back = "[" + now_time.strftime('%Y/%m/%d %H:%M:%S') + "] " + msg
            else:
                raise Exception("type_flag only is 0 or 1")
        else:
            raise Exception("flag is 0 or 1")
        return msg_back

    @staticmethod
    def now_timestamp(flag=None) -> str:
        """
        当前系统时间时间戳
        :param flag: None默认毫秒级别，"s" 秒级别
        :return:
        """
        if flag is None:
            timestamp = int(round(time.time() * 1000))
        elif flag is "s":
            timestamp = int(time.time())
        else:
            raise Exception("flag only is 's' or None")
        return timestamp

    @staticmethod
    def time_secition():
        return datetime.now()

    @staticmethod
    def time_diff(start_time: datetime, end_time: datetime, flag=None):
        """
        时间差值计算
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param flag: 差值模式：
                    默认：秒；
                    ‘d’: 天；
                    ‘m’: 分钟；
                    ‘ms’: 毫秒；
                    ‘mms’: 微秒；
                    ‘h’: 小时
        :return:
        """
        if flag is None:
            return (end_time - start_time).seconds  # 秒
        elif flag is 'd':
            return (end_time - start_time).days  # 天
        elif flag is 'm':
            return float((end_time - start_time).seconds) / 60  # 分钟
        elif flag is "mms":
            return (end_time - start_time).microseconds  # 微秒
        elif flag is "ms":
            return float((end_time-start_time).microseconds)/1000  # 毫秒
        elif flag is "h":
            return float((end_time - start_time).seconds) / 3600  # 小时
        else:
            raise Exception("choice mod is error")

    def now_time(self, flag=0) -> str:
        """
        返回当前时间
        :param flag: 0：日期，时分秒；1：日期
        :return:
        """
        if flag== 0:
            return time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        elif flag ==1:
            return time.strftime('%Y-%m-%d', time.localtime(time.time()))
        else:
            raise Exception("Flag is only (0, 1)")