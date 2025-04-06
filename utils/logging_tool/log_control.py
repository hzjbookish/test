#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    日志封装，获取当天时间，并创建了三种级别的日志对象
'''
import logging
from logging import handlers
import time
import colorlog
#import os
#import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))    # 以上三句调试使用
from common.setting import ensure_path_sep  # 导入公共方法，根据不同系统去保证路径的斜杠正确


class LogHandler:
    '''日志打印封装'''
    # 日志关系级别映射
    level_relations = {
        'debug': logging.DEBUG, # 详细信息，通常仅在调试时使用。
        'info': logging.INFO,   # 一般信息，通常用于记录程序运行时的关键信息。
        'warning': logging.WARNING, # 警告信息，通常用于记录程序中可能引起错误的情况。
        'error': logging.ERROR, # 错误信息，通常用于记录程序中发生错误的情况。
        'crit': logging.CRITICAL    # 严重错误信息，通常用于记录程序中发生严重错误的情况。
    }

    def __init__(
        self,
        filename: str,          # 日志文件名
        level: str = 'info',    # 默认日志级别
        when: str = 'D',        # 日志轮转时间，天
        fmt: str = "%(levelname)-8s%(asctime)s%(name)s:%(filename)s:%(lineno)d %(message)s" # 日志格式，默认包含日志级别、时间、模块名、文件名、行号和消息内容。
    ):
        self.logger = logging.getLogger(filename)   # 创建日志记录器，使用文件名作为日志记录器的名称。

        formatter = self.log_color()
        
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往屏幕上输出
        screen_output = logging.StreamHandler()
        # 设置屏幕上显示的格式
        screen_output.setFormatter(formatter)
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        time_rotating = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=3,
            encoding='utf-8'
        )
        # 设置文件里写入的格式
        time_rotating.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(screen_output)
        self.logger.addHandler(time_rotating)
        self.log_path = ensure_path_sep('\\logs\\log.log')

    
    @classmethod
    def log_color(cls):
        """ 设置日志颜色 """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',   #%(log_color)s：表示日志颜色。%(asctime)s：表示日志记录的时间。%(name)s：表示日志记录器的名称。%(levelname)s：表示日志级别（如 DEBUG、INFO 等）。%(message)s：表示日志消息内容。
            log_colors=log_colors_config    # 日志颜色配置
        )
        return formatter

now_time_day = time.strftime("%Y-%m-%d", time.localtime())
INFO = LogHandler(ensure_path_sep(f"\\logs\\info-{now_time_day}.log"), level='info')    # 分别创建了三个全局日志对象，对应不同级别的日志记录。
ERROR = LogHandler(ensure_path_sep(f"\\logs\\error-{now_time_day}.log"), level='error')
WARNING = LogHandler(ensure_path_sep(f'\\logs\\warning-{now_time_day}.log'))

if __name__ == '__main__':
    ERROR.logger.error("测试")