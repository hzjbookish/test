#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
    将接口请求或响应中的内容提取出来，并存入缓存中，以便后续测试用例或其他模块使用。
'''

import json
from typing import Text
from jsonpath import jsonpath
from utils.other_tools.exceptions import ValueNotFoundError
from utils.cache_process.cache_control import CacheHandler


class SetCurrentRequestCache:
    """将用例中的请求或者响应内容存入缓存"""

    def __init__(
            self,
            current_request_set_cache,  # 一个列表，包含需要缓存的配置信息（如提取的字段路径、缓存名称等）。
            request_data,               # 接口请求的数据
            response_data               # 接口响应的数据（通常是一个 Response 对象）
    ):
        self.current_request_set_cache = current_request_set_cache  # 存储缓存配置信息
        self.request_data = {"data": request_data}                  # 将请求数据封装为字典形式，键为 "data"
        self.response_data = response_data.text                     # 从响应对象中提取的文本内容

    def set_request_cache(
            self,
            jsonpath_value: Text,
            cache_name: Text) -> None:
        """将接口的请求参数存入缓存"""
        _request_data = jsonpath(
            self.request_data,
            jsonpath_value
        )
        if _request_data is not False:
            CacheHandler.update_cache(cache_name=cache_name, value=_request_data[0])    # 如果提取成功，则调用 CacheHandler.update_cache 将数据存入缓存
            # Cache(cache_name).set_caches(_request_data[0])
        else:
            raise ValueNotFoundError(
                "缓存设置失败，程序中未检测到需要缓存的数据。"
                f"请求参数: {self.request_data}"
                f"提取的 jsonpath 内容: {jsonpath_value}"
            )

    def set_response_cache(
            self,
            jsonpath_value: Text,
            cache_name
    ):
        """将响应结果存入缓存"""
        _response_data = jsonpath(json.loads(self.response_data), jsonpath_value)   # 使用 json.loads 将响应文本转换为 JSON 格式
        if _response_data is not False:
            CacheHandler.update_cache(cache_name=cache_name, value=_response_data[0])
            # Cache(cache_name).set_caches(_response_data[0])
        else:
            raise ValueNotFoundError("缓存设置失败，程序中未检测到需要缓存的数据。"
                                     f"请求参数: {self.response_data}"
                                     f"提取的 jsonpath 内容: {jsonpath_value}")

    def set_caches_main(self):  # 遍历 current_request_set_cache 列表，根据每个缓存配置项的类型（request 或 response），调用对应的缓存设置方法
        """设置缓存"""
        if self.current_request_set_cache is not None:
            for i in self.current_request_set_cache:
                _jsonpath = i.jsonpath
                _cache_name = i.name
                if i.type == 'request':
                    self.set_request_cache(jsonpath_value=_jsonpath, cache_name=_cache_name)
                elif i.type == 'response':
                    self.set_response_cache(jsonpath_value=_jsonpath, cache_name=_cache_name)