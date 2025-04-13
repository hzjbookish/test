#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志装饰器，控制程序日志输入，默认为 True
如设置 False，则程序不会打印日志
"""
import ast
from functools import wraps
from utils.read_files_tools.regular_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR


def log_decorator(switch: bool):    # 这是一个外部函数，接收一个布尔值参数 switch，用于控制日志开关，返回一个内部装饰器函数 decorator
    """
    封装日志装饰器, 打印请求信息
    :param switch: 定义日志开关
    :return:
    """
    def decorator(func):    # 这是一个内部函数，接收被装饰的函数 func，返回另一个内部函数 swapper
        @wraps(func)    # 使用 functools.wraps 装饰 swapper 函数，确保被装饰函数的元信息（如名称、文档字符串等）不会丢失
        def swapper(*args, **kwargs):   # 这是装饰器的核心逻辑部分，实际执行被装饰函数 func，并根据条件决定是否打印日志。

            # 判断日志为开启状态，才打印日志
            res = func(*args, **kwargs)
            # 判断日志开关为开启状态
            if switch:
                _log_msg = f"\n======================================================\n" \
                               f"用例标题: {res.detail}\n" \
                               f"请求路径: {res.url}\n" \
                               f"请求方式: {res.method}\n" \
                               f"请求头:   {res.headers}\n" \
                               f"请求内容: {res.request_body}\n" \
                               f"接口响应内容: {res.response_data}\n" \
                               f"接口响应时长: {res.res_time} ms\n" \
                               f"Http状态码: {res.status_code}\n" \
                               "====================================================="
                _is_run = ast.literal_eval(cache_regular(str(res.is_run)))      # 使用 cache_regular 函数对 res.is_run 的值进行正则处理。使用 ast.literal_eval 将字符串安全地转换为 Python 数据类型（如布尔值或 None）
                # 判断正常打印的日志，控制台输出绿色
                if _is_run in (True, None) and res.status_code == 200:
                    INFO.logger.info(_log_msg)
                else:
                    # 失败的用例，控制台打印红色
                    ERROR.logger.error(_log_msg)
            return res
        return swapper
    return decorator