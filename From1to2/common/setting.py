import os

def root_path():
    '''获取根路径'''
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path

def ensure_path_sep(path:str) -> str:
    '''
    兼容windows和linux不同操作系统的路径分隔符
    '''
    if '/' in path: # linux
        path = os.sep.join(path.split('/'))

    if '\\' in path: # windows
        path = os.sep.join(path.split('\\'))
    
    return root_path() + path   # 拼接根路径