#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    1、定义了一系列数据模型和枚举类，用于描述自动化测试框架中的各种数据结构。这些模型和枚举类基于 Enum、dataclass 和 pydantic 库实现，提供了类型安全性和数据验证能力。
    2、枚举成员是唯一的，避免了使用字符串或其他类型时可能出现的拼写错误
    3、枚举成员具有描述性名称，使代码更易读和维护。
    4、可以轻松添加新的枚举成员，而不会影响现有代码。
    5、提供了丰富的内置方法，如 name、value、describe 等，方便操作和调试。
'''
import types
from enum import Enum, unique
from typing import Text, Dict, Callable, Union, Optional, List, Any
from dataclasses import dataclass
from pydantic import BaseModel, Field

class NotificationType(Enum):   
    """ 自动化通知方式 """
    DEFAULT = '0'           
    DING_TALK = '1'
    WECHAT = '2'
    EMAIL = '3'
    FEI_SHU = '4'

@dataclass  # 简化类的定义，自动生成常用的方法，并提供类型检查和默认值支持
class TestMetrics:
    """ 用例执行数据 """
    passed: int
    failed: int
    broken: int
    skipped: int
    total: int
    pass_rate: float
    time: Text


class RequestType(Enum):
    """
    request请求发送，请求参数的数据类型
    """
    JSON = "JSON"
    PARAMS = "PARAMS"
    DATA = "DATA"
    FILE = 'FILE'
    EXPORT = "EXPORT"
    NONE = "NONE"


class TestCaseEnum(Enum):
    '''定义了测试用例中各个字段的名称及其是否为必填项。'''
    URL = ("url", True)
    HOST = ("host", True)
    METHOD = ("method", True)
    DETAIL = ("detail", True)
    IS_RUN = ("is_run", True)
    HEADERS = ("headers", True)
    REQUEST_TYPE = ("requestType", True)
    DATA = ("data", True)
    DE_CASE = ("dependence_case", True)
    DE_CASE_DATA = ("dependence_case_data", False)
    CURRENT_RE_SET_CACHE = ("current_request_set_cache", False)
    SQL = ("sql", False)
    ASSERT_DATA = ("assert", True)
    SETUP_SQL = ("setup_sql", False)
    TEARDOWN = ("teardown", False)
    TEARDOWN_SQL = ("teardown_sql", False)
    SLEEP = ("sleep", False)


class Method(Enum):
    '''定义了 HTTP 请求方法。'''
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTION = "OPTION"


def load_module_functions(module) -> Dict[Text, Callable]:  # 返回值：一个字典，键为函数名，值为函数对象。
    """ 获取 module中方法的名称和所在的内存地址 """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item
    return module_functions


@unique     # unique装饰器，用于保证枚举类的值是唯一的。
class DependentType(Enum):
    """
    数据依赖相关枚举
    """
    RESPONSE = 'response'   # 依赖于接口响应数据。
    REQUEST = 'request'     # 依赖于请求数据。
    SQL_DATA = 'sqlData'    # 依赖于数据库查询结果。
    CACHE = "cache"         # 依赖于缓存数据。


class Assert(BaseModel):    # BaseModel在实例化时可以自动验证各个参数的格式是否正确
    '''描述断言信息'''
    jsonpath: Text                          # jsonpath：JSON 路径表达式。
    type: Text                              # type：断言类型。
    value: Any                              # value：期望值。
    AssertType: Union[None, Text] = None    # AssertType：可选的断言类型。


class DependentData(BaseModel):
    '''描述依赖数据的信息'''
    dependent_type: Text
    jsonpath: Text
    set_cache: Optional[Text]
    replace_key: Optional[Text]


class DependentCaseData(BaseModel):
    case_id: Text
    # dependent_data: List[DependentData]
    dependent_data: Union[None, List[DependentData]] = None


class ParamPrepare(BaseModel):
    dependent_type: Text
    jsonpath: Text
    set_cache: Text


class SendRequest(BaseModel):
    dependent_type: Text
    jsonpath: Optional[Text]
    cache_data: Optional[Text]
    set_cache: Optional[Text]
    replace_key: Optional[Text]


class TearDown(BaseModel):
    case_id: Text
    param_prepare: Optional[List["ParamPrepare"]]
    send_request: Optional[List["SendRequest"]]


class CurrentRequestSetCache(BaseModel):
    type: Text
    jsonpath: Text
    name: Text


class TestCase(BaseModel):
    '''描述测试用例的详细信息'''
    url: Text                                                                               # url：接口地址。
    method: Text                                                                            # method：请求方法。
    detail: Text                                                                            # detail：用例描述。
    # assert_data: Union[Dict, Text] = Field(..., alias="assert")
    assert_data: Union[Dict, Text]                                                          # assert_data: 断言数据
    headers: Union[None, Dict, Text] = {}                                                   # headers：请求头。
    requestType: Text                                                                       # requestType：请求类型。  
    is_run: Union[None, bool, Text] = None                                                  # is_run：是否执行该用例。
    data: Any = None                                                                        # data：请求体数据。  
    dependence_case: Union[None, bool] = False                                              # dependence_case：依赖的用例。
    dependence_case_data: Optional[Union[None, List["DependentCaseData"], Text]] = None     # dependence_case_data：依赖的用例数据。
    sql: List = None                                                                        # sql：数据库查询语句。 
    setup_sql: List = None                                                                  # setup_sql：数据库前置查询语句。
    status_code: Optional[int] = None                                                       # status_code：接口状态码。
    teardown_sql: Optional[List] = None                                                     # teardown_sql：数据库后置查询语句。
    teardown: Union[List["TearDown"], None] = None                                          # teardown：后置操作。
    current_request_set_cache: Optional[List["CurrentRequestSetCache"]]                     # current_request_set_cache：当前请求设置缓存。
    sleep: Optional[Union[int, float]]                                                      # sleep：接口请求等待时间。 


class ResponseData(BaseModel):
    url: Text
    is_run: Union[None, bool, Text]
    detail: Text
    response_data: Text
    request_body: Any
    method: Text
    sql_data: Dict
    yaml_data: "TestCase"
    headers: Dict
    cookie: Dict
    assert_data: Dict
    res_time: Union[int, float]
    status_code: int
    teardown: List["TearDown"] = None
    teardown_sql: Union[None, List]
    body: Any


class DingTalk(BaseModel):
    webhook: Union[Text, None]      # Union 是 typing 模块中的一个泛型类型，表示字段可以是多种类型之一。None：表示字段可以为 None
    secret: Union[Text, None]


class MySqlDB(BaseModel):
    switch: bool = False
    host: Union[Text, None] = None
    user: Union[Text, None] = None
    password: Union[Text, None] = None
    port: Union[int, None] = 3306


class Webhook(BaseModel):
    webhook: Union[Text, None]


class Email(BaseModel):
    send_user: Union[Text, None]
    email_host: Union[Text, None]
    stamp_key: Union[Text, None]
    # 收件人
    send_list: Union[Text, None]


class Config(BaseModel):
    project_name: Text                                  # 项目名称
    env: Text                                           # 环境（如开发、测试、生产）
    tester_name: Text                                   # 测试人员
    notification_type: Text = '0'                       # 通知方式
    excel_report: bool                                  # 是否生成excel报告
    ding_talk: "DingTalk"                               # 钉钉  
    mysql_db: "MySqlDB"                                 # mysql
    mirror_source: Text                                 # 镜像源
    wechat: "Webhook"                                   # 微信
    email: "Email"                                      # 邮箱
    lark: "Webhook"                                     # 飞书
    real_time_update_test_cases: bool = False           # 实时更新测试用例
    host: Text                                          # host接口域名
    app_host: Union[Text, None]                         # app_host接口域名


@unique
class AllureAttachmentType(Enum):
    """
    allure 报告的文件类型枚举
    """
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"


@unique
class AssertMethod(Enum):
    """断言类型"""
    equals = "=="
    less_than = "lt"
    less_than_or_equals = "le"
    greater_than = "gt"
    greater_than_or_equals = "ge"
    not_equals = "not_eq"
    string_equals = "str_eq"
    length_equals = "len_eq"
    length_greater_than = "len_gt"
    length_greater_than_or_equals = 'len_ge'
    length_less_than = "len_lt"
    length_less_than_or_equals = 'len_le'
    contains = "contains"
    contained_by = 'contained_by'
    startswith = 'startswith'
    endswith = 'endswith'