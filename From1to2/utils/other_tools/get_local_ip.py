#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    获取本机IP
'''

import socket


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    _s = None
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # 创建一个UDP的socket，socket.AF_INET：表示使用IPv4地址族。socket.SOCK_DGRAM：表示使用UDP协议。
        _s.connect(('8.8.8.8', 80))     # 连接到Google的DNS服务器的80端口。
        l_host = _s.getsockname()[0]    # 返回套接字的本地地址，格式为 (local_ip, local_port)。[0]：提取本地IP地址。
    finally:
        _s.close()

    return l_host   # 返回本地IP地址