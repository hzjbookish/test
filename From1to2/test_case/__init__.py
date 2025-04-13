'''
    pytest.main()开始运行后从这里开始执行，执行完成后，将所有的用例数据写入全局变量_cache_config中
'''
from common.setting import ensure_path_sep
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.read_files_tools.get_all_files_path import get_all_files
from utils.cache_process.cache_control import CacheHandler, _cache_config   # 导入存有缓存数据的全局变量

def write_case_process():
    """
    获取所有用例，写入用例池中
    :return:
    """

    # 循环拿到所有存放用例的文件路径
    for i in get_all_files(file_path=ensure_path_sep("\\data"), yaml_data_switch=True):     # 获取所有用例文件路径，这里写true可以实现对yaml文件的过滤
        # 循环读取文件中的数据
        case_process = CaseData(i).case_process(case_id_switch=True)    # 当前i为yaml文件的路径，先实例化，再调用case_process方法，返回一个yaml文件里的所有测试用例数据
        if case_process is not None:
            # 转换数据类型
            for case in case_process:
                for k, v in case.items():   # 将用例名和数据进行遍历，并写入缓存池中
                    # 判断 case_id 是否已存在
                    case_id_exit = k in _cache_config.keys()    # 判断 case_id 是否已存在，返回true则说明 case_id 存在
                    # 如果case_id 不存在，则将用例写入缓存池中
                    if case_id_exit is False:
                        CacheHandler.update_cache(cache_name=k, value=v)
                        # case_data[k] = v
                    # 当 case_id 为 True 存在时，则跑出异常
                    elif case_id_exit is True:
                        raise ValueError(f"case_id: {k} 存在重复项, 请修改case_id\n"
                                         f"文件路径: {i}")


write_case_process()