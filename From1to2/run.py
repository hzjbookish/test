import os
import sys
import traceback
import pytest
#from utils.other_tools.allure_data.allure_report_data import AllureFileClean    # 报告数据清洗
from utils.logging_tool.log_control import INFO # 选择日志等级为INFO的生成器
#from utils.other_tools.allure_data.error_case_excel import ErrorCaseExcel
from utils import config    # utils初始化时解包后的配置信息

def run():
    # 从配置文件中获取项目名称
    try:
        INFO.logger.info("开始执行{}项目".format(config.project_name))
        pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning','--alluredir', './report/tmp', "--clean-alluredir"])
        """
                   --reruns: 失败重跑次数
                   --count: 重复执行次数
                   -v: 显示错误位置以及错误的详细信息
                   -s: 等价于 pytest --capture=no 可以捕获print函数的输出
                   -q: 简化输出信息
                   -m: 运行指定标签的测试用例
                   -x: 一旦错误，则停止运行
                   --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
                    "--reruns=3", "--reruns-delay=2"
                   """
        os.system(r"allure generate ./report/tmp -o ./report/html --clean")

        # allure_data = AllureFileClean().get_case_count()    # 获取测试报告数据,数据清洗容易出问题，先注释掉
        # if config.excel_report:
        #     ErrorCaseExcel().write_case()
        
        # 程序运行之后，自动启动报告，如果不想启动报告，可注释这段代码
        #os.system(f"allure serve ./report/tmp -h 127.0.0.1 -p 9999")

    except Exception:
        # 如有异常，相关异常发送邮件
        e = traceback.format_exc()
        #send_email = SendEmail(AllureFileClean.get_case_count())
        #send_email.error_mail(e)
        raise



if __name__ == "__main__":
    run()