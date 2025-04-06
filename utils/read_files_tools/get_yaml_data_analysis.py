#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
    对yaml文件的数据做检查看是否合规
'''

from enum import Enum
from typing import Union, Text, Dict, List
from utils.read_files_tools.yaml_control import GetYamlData
from utils.other_tools.models import TestCase
from utils.other_tools.exceptions import ValueNotFoundError     # 还未实现
from utils.cache_process.cache_control import CacheHandler
from utils import config
from utils.other_tools.models import RequestType, Method, TestCaseEnum  # 导入请求类型，请求方法和测试用例枚举
import os


class CaseDataCheck:
    """
    yaml 数据解析, 判断数据填写是否符合规范
    """

    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(self.file_path) is False:
            raise FileNotFoundError("用例地址未找到")

        self.case_data = None
        self.case_id = None

    def _assert(self, attr: Text):
        assert attr in self.case_data.keys(), (         # 断言信息为真时，不会打印报错信息
            f"用例ID为 {self.case_id} 的用例中缺少 {attr} 参数，请确认用例内容是否编写规范."
            f"当前用例文件路径：{self.file_path}"
        )

    def check_params_exit(self):    # 遍历 TestCaseEnum 枚举中的所有字段，检查当前用例数据中是否缺少必要的参数。
        for enum in list(TestCaseEnum._value2member_map_.keys()):   # 遍历枚举，看下有枚举值是否为空，主要遍历TestCaseEnum枚举中的键，如url、hsot等
            if enum[1]:     # 用例中的参数写为false时，不会去执行检查，相当于开关
                self._assert(enum[0])   

    def check_params_right(self, enum_name, attr):
        _member_names_ = enum_name._member_names_   # 获取枚举的成员名称列表
        assert attr.upper() in _member_names_, (
            f"用例ID为 {self.case_id} 的用例中 {attr} 填写不正确，"
            f"当前框架中只支持 {_member_names_} 类型."
            f"如需新增 method 类型，请联系管理员."
            f"当前用例文件路径：{self.file_path}"
        )
        return attr.upper() # 返回大写后的请求方法 

    @property   # 将方法转换为只读属性，可以通过对象直接访问（如 obj.get_method），而无需调用方法（如 obj.get_method()）。
    def get_method(self) -> Text:

        return self.check_params_right(
            Method,
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    def get_host(self) -> Text: # 把host和URL作拼接
        host = (
                self.case_data.get(TestCaseEnum.HOST.value[0]) +
                self.case_data.get(TestCaseEnum.URL.value[0])
        )
        return host

    @property
    def get_request_type(self):
        return self.check_params_right(
            RequestType,
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    @property
    def get_dependence_case_data(self):
        _dep_data = self.case_data.get(TestCaseEnum.DE_CASE.value[0])
        if _dep_data:
            assert self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0]) is not None, (
                f"程序中检测到您的 case_id 为 {self.case_id} 的用例存在依赖，但是 {_dep_data} 缺少依赖数据."
                f"如已填写，请检查缩进是否正确， 用例路径: {self.file_path}"
            )
        return self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0])

    @property
    def get_assert(self):
        _assert_data = self.case_data.get(TestCaseEnum.ASSERT_DATA.value[0])
        assert _assert_data is not None, (
            f"用例ID 为 {self.case_id} 未添加断言，用例路径: {self.file_path}"
        )
        return _assert_data

    @property
    def get_sql(self):
        _sql = self.case_data.get(TestCaseEnum.SQL.value[0])
        # 判断数据库开关为开启状态，并且sql不为空
        if config.mysql_db.switch and _sql is None:
            return None
        return _sql


class CaseData(CaseDataCheck):  # 继承了父类，实例化时先从父类CaseDataCheck开始初始化

    def case_process(self, case_id_switch: Union[None, bool] = None):   # case_id_switch为一个布尔值或 None，默认为 None
        data = GetYamlData(self.file_path).get_yaml_data()  # 解析测试用例yaml中的测试数据
        case_list = []
        for key, values in data.items():    # data.items() 此时通常代表 用例名称：用例数据
            # 公共配置中的数据，与用例数据不同，需要单独处理，分为公共参数解析和用例解析
            if key != 'case_common':
                self.case_data = values # 获取用例数据
                self.case_id = key      # 获取用例ID
                super().check_params_exit() # 调用父类的参数检查方法
                case_date = {   # 获取用例数据，同时加入了一些用例参数检查操作
                    'method': self.get_method,  # 相当于直接调用get_method()方法，把请求方法和定义好的几种请求方法做比对，看是否合规
                    'is_run': self.case_data.get(TestCaseEnum.IS_RUN.value[0]), # 直接取值
                    'url': self.get_host,   # 把host和URL拼接
                    'detail': self.case_data.get(TestCaseEnum.DETAIL.value[0]), # 直接取值
                    'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),   # 直接取值
                    'requestType': super().get_request_type,    # 和method一样的校验方式
                    'data': self.case_data.get(TestCaseEnum.DATA.value[0]), # 直接取值
                    'dependence_case': self.case_data.get(TestCaseEnum.DE_CASE.value[0]),   # 直接取值
                    'dependence_case_data': self.get_dependence_case_data,
                    "current_request_set_cache": self.case_data.get(TestCaseEnum.CURRENT_RE_SET_CACHE.value[0]),    # 直接取值
                    "sql": self.get_sql,
                    "assert_data": self.get_assert,
                    "setup_sql": self.case_data.get(TestCaseEnum.SETUP_SQL.value[0]),   # 直接取值
                    "teardown": self.case_data.get(TestCaseEnum.TEARDOWN.value[0]),     # 直接取值
                    "teardown_sql": self.case_data.get(TestCaseEnum.TEARDOWN_SQL.value[0]), # 直接取值
                    "sleep": self.case_data.get(TestCaseEnum.SLEEP.value[0]),   # 直接取值
                }
                if case_id_switch is True:
                    case_list.append({key: TestCase(**case_date).dict()})   # 当 case_id_switch 参数为 True 时，方法会将每个用例的数据封装在一个字典中，并以用例ID作为键。
                else:
                    case_list.append(TestCase(**case_date).dict())  # 使用 case_date 字典中的键值对来初始化 TestCase 对象, 然后再用 .dict() 方法将 TestCase 对象会被转换为一个普通的 Python 字典

        return case_list


class GetTestCase:

    @staticmethod
    def case_data(case_id_lists: List):
        case_lists = []
        for i in case_id_lists:
            _data = CacheHandler.get_cache(i)
            case_lists.append(_data)
            #case_lists.append(i)

        return case_lists