'''
    导入工具类时先做一个初始化操作
'''
from utils.read_files_tools.yaml_control import GetYamlData # 先导入可以读取yaml文件的工具类
from common.setting import ensure_path_sep  # 兼容windows和linux不同操作系统的路径分隔符
from utils.other_tools.models import Config # 导入项目的配置信息的枚举模板

_data = GetYamlData(ensure_path_sep("\\common\\config.yaml")).get_yaml_data()   # 得到项目的详细配置信息
config = Config(**_data)    # 将配置信息解包，然后调用Config方法去做格式校验，有嵌套的话会递归解析，如果校验通过实例化类，不通过抛异常

if config.env == "pre":
    config.host = "https://www.wanandroid.com"