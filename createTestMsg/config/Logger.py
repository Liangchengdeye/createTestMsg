#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@site:
@software: PyCharm
@file: logger.py
@time: 2018/3/23 14:30
@describe: log日志编写-支持以天为单位
"""

import logging
import time
import os
import re
import datetime
from logging.handlers import TimedRotatingFileHandler

cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个
logName = os.path.join(log_path, '%s' % time.strftime('%Y-%m-%d'))  # 文件的命名
try:
    import codecs
except ImportError:
    codecs = None


class MultiprocessHandler(logging.FileHandler):
    """支持多进程的TimedRotatingFileHandler"""

    def __init__(self, filename, when='D', backupCount=1, encoding=None, delay=False):
        """filename 日志文件名,when 时间间隔的单位,backupCount 保留文件个数
        delay 是否开启 OutSteam缓存
            True 表示开启缓存，OutStream输出到缓存，待缓存区满后，刷新缓存区，并输出缓存数据到文件。
            False表示不缓存，OutStrea直接输出到文件"""
        self.prefix = filename
        self.backupCount = backupCount
        self.when = when.upper()
        # 正则匹配 年-月-日
        self.extMath = r"^\d{4}-\d{2}-\d{2}"

        # S 每秒建立一个新文件
        # M 每分钟建立一个新文件
        # H 每天建立一个新文件
        # D 每天建立一个新文件
        self.when_dict = {
            'S': "%Y-%m-%d-%H-%M-%S",
            'M': "%Y-%m-%d-%H-%M",
            'H': "%Y-%m-%d-%H",
            'D': "%Y-%m-%d"
        }
        # 日志文件日期后缀
        self.suffix = self.when_dict.get(when)
        if not self.suffix:
            raise ValueError(u"指定的日期间隔单位无效: %s" % self.when)
        # 拼接文件路径 格式化字符串
        self.filefmt = os.path.join("./logs", "%s.%s" % (self.prefix, self.suffix))
        # 使用当前时间，格式化文件格式化字符串
        self.filePath = datetime.datetime.now().strftime(self.filefmt)
        # 获得文件夹路径
        _dir = os.path.dirname(self.filefmt)
        try:
            # 如果日志文件夹不存在，则创建文件夹
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        except Exception:
            print(u"创建文件夹失败")
            print(u"文件夹路径：" + self.filePath)
            pass

        if codecs is None:
            encoding = None

        logging.FileHandler.__init__(self, self.filePath + '.log', 'a+', encoding, delay)

    def shouldChangeFileToWrite(self):
        """更改日志写入目的写入文件
        :return True 表示已更改，False 表示未更改"""
        # 以当前时间获得新日志文件路径
        _filePath = datetime.datetime.now().strftime(self.filefmt)
        if _filePath != self.filePath:
            self.filePath = _filePath
            return True
        return False

    def doChangeFile(self):
        """输出信息到日志文件，并删除多于保留个数的所有日志文件"""
        # 日志文件的绝对路径
        self.baseFilename = os.path.abspath(self.filePath + '.log')
        if self.stream:
            # flush close 都会刷新缓冲区，flush不会关闭stream，close则关闭stream
            # self.stream.flush()
            self.stream.close()
            # 关闭stream后必须重新设置stream为None，否则会造成对已关闭文件进行IO操作。
            self.stream = None
        # delay 为False 表示 不OutStream不缓存数据 直接输出所有，只需要关闭OutStream即可
        if not self.delay:
            # 这个地方如果关闭colse那么就会造成进程往已关闭的文件中写数据，从而造成IO错误
            # delay == False 表示的就是 不缓存直接写入磁盘
            # 我们需要重新在打开一次stream
            # self.stream.close()
            self.stream = self._open()
        # 删除多于保留个数的所有日志文件
        if self.backupCount > 0:
            print('删除日志')
            for s in self.getFilesToDelete():
                print("delete", s)
                os.remove(s)

    def getFilesToDelete(self):
        """获得过期需要删除的日志文件"""
        dirName, _ = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        # self.prefix 为日志文件名 列如：mylog.2017-03-19 中的 mylog
        # 加上 点号 . 方便获取点号后面的日期
        prefix = self.prefix + '.'
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if re.compile(self.extMath).match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        #   删除多于保留文件个数 backupCount的所有前面的日志文件。
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def emit(self, record):
        """发送一个日志记录
        覆盖FileHandler中的emit方法，logging会自动调用此方法"""
        try:
            if self.shouldChangeFileToWrite():
                self.doChangeFile()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class Logger:
    def __init__(self, logName=logName, level=logging.INFO, log=None):
        if '.log' in logName:
            logName = logName.replace(".log", "")
        self.path = os.path.join(log_path, logName)
        # 日志打印格式
        # self.log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        self.log_fmt = '[%(levelname)s]\t%(asctime)s\tFile \"%(filename)s\":\t %(message)s'
        self.formatter = logging.Formatter(self.log_fmt)
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger()
        self.log_file_handler = MultiprocessHandler(filename=logName, when="D", backupCount=3,
                                                    encoding="utf-8")
        self.log_file_handler.setFormatter(self.formatter)

    def __console(self, level, message):
        """
        创建TimedRotatingFileHandler对象
            参数说明：
                filename：日志文件名的prefix；
                when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下：
                “S”: Seconds
                “M”: Minutes
                “H”: Hours
                “D”: Days
                “W”: Week day (0=Monday)
                “midnight”: Roll over at midnight
                backupCount: 表示日志文件的保留个数；
        :param level: 日志级别
        :param message: 日志格式
        :return:
        """

        self.log.addHandler(self.log_file_handler)
        if level == 'info':
            self.log.info(message)
        elif level == 'debug':
            self.log.debug(message)
        elif level == 'warning':
            self.log.warning(message)
        elif level == 'error':
            self.log.error(message)

        self.log.removeHandler(self.log_file_handler)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def war(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def error_msg(self, e, message=None):
        """
        详细错误信息
        :param e: 错误原因
        :param msg: 自定义错误类型
        :return: [错误文件路径] [错误行数line:76] [自定义错误类型] 错误原因
        """
        ERROR_FILE_NAME = '[' + str(e.__traceback__.tb_frame.f_globals["__file__"]) + '] '
        ERROR_LINE = '[line:' + str(e.__traceback__.tb_lineno) + '] '
        ERROR_SOURCE = str(e)
        if message is None:
            message = ""
        ERROR = ERROR_LINE + '[' + message + '] ' + ERROR_SOURCE
        # self.logger.error(ERROR)
        self.__console('error', ERROR)
