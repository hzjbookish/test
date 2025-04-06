#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    封装了 Allure 报告相关的操作步骤和附件上传方法，方便在测试用例中记录操作步骤、上传文件或图片等。以下是该文件的详细解析
'''

import json
import allure
from utils.other_tools.models import AllureAttachmentType


def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    """
    with allure.step(step):
        allure.attach(
            json.dumps(
                str(var),               # 将 var 转换为格式化的 JSON 字符串
                ensure_ascii=False,     # 确保非 ASCII 字符（如中文）能够正确显示。
                indent=4),              # 设置缩进为 4 个空格，使 JSON 数据更易读
            step,
            allure.attachment_type.JSON)


def allure_attach(source: str, name: str, extension: str):
    """
    allure报告上传附件、图片、excel等
    :param source: 文件路径，相当于传一个文件
    :param name: 附件名称
    :param extension: 附件的拓展名称
    :return:
    """
    # 获取上传附件的尾缀，判断对应的 attachment_type 枚举值
    _name = name.split('.')[-1].upper()
    _attachment_type = getattr(AllureAttachmentType, _name, None)   # 使用 getattr 方法从 AllureAttachmentType 枚举类中获取对应的附件类型。如果扩展名未定义，则返回 None

    allure.attach.file(
        source=source,
        name=name,
        attachment_type=_attachment_type if _attachment_type is None else _attachment_type.value,
        extension=extension
    )


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass