#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
断言类型封装，支持json响应断言、数据库断言
"""
import ast
import json
from typing import Text, Dict, Any, Union
from jsonpath import jsonpath
from utils.other_tools.models import AssertMethod
from utils.logging_tool.log_control import ERROR, WARNING
from utils.read_files_tools.regular_control import cache_regular
from utils.other_tools.models import load_module_functions
from utils.assertion import assert_type
from utils.other_tools.exceptions import JsonpathExtractionFailed, SqlNotFound, AssertTypeError
from utils import config


class AssertUtil:

    def __init__(self, assert_data, request_data, response_data, status_code):

        self.response_data = response_data          # 初始化断言内容
        self.request_data = request_data
        #self.sql_data = sql_data
        self.assert_data = assert_data
        #self.sql_switch = config.mysql_db.switch
        self.status_code = status_code

    @staticmethod
    def literal_eval(attr):
        return ast.literal_eval(cache_regular(str(attr)))

    @property
    def get_assert_data(self):
        assert self.assert_data is not None, (
                "'%s' should either include a `assert_data` attribute, "
                % self.__class__.__name__
        )
        return ast.literal_eval(cache_regular(str(self.assert_data)))

    @property
    def get_type(self):
        assert 'type' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `type` 属性 " % self.get_assert_data
        )

        # 获取断言类型对应的枚举值
        name = AssertMethod(self.get_assert_data.get("type")).name
        return name

    @property
    def get_value(self):
        assert 'value' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `value` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("value")    # 获取预期断言值

    @property
    def get_jsonpath(self):
        assert 'jsonpath' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `jsonpath` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("jsonpath")

    @property
    def get_assert_type(self):
        assert 'AssertType' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `AssertType` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("AssertType")

    @property
    def get_message(self):
        """
        获取断言描述，如果未填写，则返回 `None`
        :return:
        """
        return self.get_assert_data.get("message", None)

    @staticmethod
    def functions_mapping():
        return load_module_functions(assert_type)

    @property
    def get_response_data(self):
        return json.loads(self.response_data)   # 将json字符串转换为字典或者列表


    def _assert(self, check_value: Any, expect_value: Any, message: Text = ""):

        self.functions_mapping()[self.get_type](check_value, expect_value, str(message)) # 真正断言的地方

    @property
    def _assert_resp_data(self):
        resp_data = jsonpath(self.get_response_data, self.get_jsonpath) # 通过jsonpath表达式提取到断言数据
        assert resp_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.get_response_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(resp_data) > 1:
            return resp_data    # 提取到多个数据，则返回列表
        return resp_data[0]

    @property
    def _assert_request_data(self):
        req_data = jsonpath(self.request_data, self.get_jsonpath)
        assert req_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.request_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(req_data) > 1:
            return req_data
        return req_data[0]

    def assert_type_handle(self):
        try:
            self._assert(self._assert_resp_data, self.get_value, self.get_message)
        except:
            raise AssertTypeError("断言失败，目前仅支持响应断言")


class Assert(AssertUtil):

    def assert_data_list(self):
        assert_list = []
        for k, v in self.assert_data.items():
            if k == "status_code":  # 断言状态码是否为200
                assert self.status_code == v, "响应状态码断言失败"
            else:
                assert_list.append(v)
        return assert_list

    def assert_type_handle(self):
        for i in self.assert_data_list():   # 有几个断言就断言几次
            self.assert_data = i
            super().assert_type_handle()