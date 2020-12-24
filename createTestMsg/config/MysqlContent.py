#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@site:
@software: PyCharm
@file: dbhelper.py
@time: 2018/1/17 17:46
@describe: 数据库操作助手

"""
import sys
import os
import pymysql
import logging

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from config.Logger import Logger
from config.ReadConfig import ReadConfig as RC

SETTING = RC().get_conf("./config.yaml")
logger = Logger("mysql.log", logging.WARNING, logging.DEBUG)


class DBHelper():
    """连接信息"""

    def __init__(self):
        self.settings = SETTING['mysqlContent']  # 获取settings配置，设置需要的信息
        self.host = self.settings['host']
        self.port = self.settings['port']
        self.user = self.settings['user']
        self.passwd = self.settings['passwd']
        self.db = self.settings['db']

    # 连接到mysql，不是连接到具体的数据库
    def connectMysql(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               charset='utf8')
        return conn

    # 连接到具体的数据库
    def connectDatabase(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')
        return conn

    # 创建数据库
    def createDatabase(self):
        conn = self.connectMysql()  # 连接数据库
        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)  # 执行sql语句
        cur.close()
        conn.close()

    # 创建表
    def createTable(self, sql):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 插入数据
    def insert(self, sql, *params):
        """

        :param sql:
        :param params: 元组， params=('data_1','data_2')
        :return:
        """
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    # 批量插入数据
    def insert_many(self, sql, params):
        """
        :param sql: insert into test(name, age) value(%s, %s)
        :param params: [['xiaohong','18'], ['xiaowang', '19']]
        :return:
        """
        try:
            conn = self.connectDatabase()
            cur = conn.cursor()
            cur.executemany(sql, params)
            conn.commit()
        except Exception as e:
            logger.error_msg(e, 'INSERT-MANY')
        finally:
            cur.close()
            conn.close()

    # 更新数据
    def update(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    # 删除数据
    def delete(self, sql, *params):
        try:
            conn = self.connectDatabase()
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
        except Exception as e:
            logger.error_msg(e, 'DELETE')
        finally:
            cur.close()
            conn.close()

    # 查询数据
    def select(self, sql):
        conn = self.connectDatabase()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            # 获取所有记录列表
            results = cur.fetchall()
            list_id = []
            for str_id in results:
                list_id.append(str_id)
            return list_id
        except Exception as e:
            logger.error_msg(e, "UNABLE-TO-FETCH-DATA")
        finally:
            cur.close()
            conn.close()
