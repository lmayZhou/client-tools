#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- EML 文件工具类
# --
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2021/3/4 15:22
# Email lmay@lmaye.com
# ----------------------------------------------------------
import email
import math
import os


def read_eml(eml_file, content_type="text/html", annex_save=False, annex_path=None):
    """
    读取EML文件信息

    :param eml_file:        EML文件
    :param content_type:    内容类型
    :param annex_save:      附件保存
    :param annex_path:      附件路径
    :return: {}
    """
    try:
        eml = open(eml_file, "r")
        email_content = email.message_from_file(eml)
        subject_ = email_content.get("subject")
        # 特殊格式处理
        if subject_.find("utf-8") > 0 or subject_.find("UTF-8") > 0:
            sub_decode = email.header.decode_header(subject_)
            # 信息解析
            subject = sub_decode[0][0].decode("utf-8")
        elif subject_.find("iso-2022-jp") > 0 or subject_.find("ISO-2022-JP") > 0:
            sub_decode = email.header.decode_header(subject_)
            # 信息解析
            subject = sub_decode[0][0].decode("iso-2022-jp")
        else:
            # 解码
            sub_header = email.header.Header(subject_)
            sub_decode = email.header.decode_header(sub_header)
            subject = str(sub_decode[0][0], "utf-8")
        from_ = email.utils.parseaddr(email_content.get("from"))[1]
        to_ = email.utils.parseaddr(email_content.get("to"))[1]
        content = ""
        # 遍历信件中的mime数据块
        for par in email_content.walk():
            # 是否是Multipart
            if not par.is_multipart():
                # 是否是附件
                annex_name = par.get_param("name")
                if annex_name:
                    if annex_save:
                        # 附件处理
                        file = open(os.path.join(annex_path, subject + " - " + annex_name), "wb")
                        file.write(par.get_payload(decode=True))
                else:
                    # 文本内容
                    if content_type == par.get_content_type():
                        # content = par.get_payload()
                        # 解密
                        content = str(par.get_payload(decode=True), encoding=par.get_content_charset())
        eml.close()
        data = [subject, from_, to_]
        contents = split_text(content, 30000)
        for it in contents:
            data.append(it)
        return data
        # return {"subject": subject, "from": from_, "to": to_, "content": content}
    except BaseException as e:
        # LOG.error("读取EML文件, 异常 : [{}] ---> {}".format(eml_file, e))
        return None


def split_text(text, length):
    text_list = []
    group_num = len(text) / int(length)
    # 向上取整
    group_num = math.ceil(group_num)
    for i in range(group_num):
        text_list.append(text[i * int(length):i * int(length) + int(length)])
    return text_list
