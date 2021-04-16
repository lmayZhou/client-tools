#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 线程处理
# --
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2021/4/14 9:47
# Email lmay@lmaye.com
# ----------------------------------------------------------
import datetime
import math
import threading
import time

from core import LOG
from core.utils import eml_utils, excel_utils


def thread_list(threads, _file_names, eml_path_, csv_path, lens=50000, content_type="text/html", signal_out=None):
    """
        添加到线程池

        :param threads:         线程池
        :param _file_names:     文件名
        :param eml_path_:       eml路径
        :param csv_path:        生成路径
        :param lens:            处理数量
        :param content_type:    内容类型
        :param signal_out:      打印日志信号
        :return:
    """
    for i in range(math.ceil(len(_file_names) / lens)):
        records = _file_names[i * lens:(i + 1) * lens]
        thread = threading.Thread(target=write_file, args=(i, records, eml_path_, csv_path, content_type, signal_out))
        threads.append(thread)


def write_file(x, _file_names, eml_path_, csv_path, content_type="text/html", signal_out=None):
    """
        写入文件

        :param x:               线程序号
        :param _file_names:     文件名
        :param eml_path_:       eml路径
        :param csv_path:        生成路径
        :param content_type:    内容类型
        :param signal_out:      打印日志信号
        :return:
    """
    LOG.info(
        "[{}] - 线程[{}]执行中... - [{}]".format(x + 1, threading.currentThread().name, threading.currentThread().ident))
    if signal_out:
        signal_out.emit("{} [{}] - 线程[{}]执行中...".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                        x + 1, threading.currentThread().name))
    records = []
    for file_name in _file_names:
        eml_file = eml_path_ + file_name
        eml = eml_utils.read_eml(eml_file, content_type, annex_save=True, annex_path=csv_path)
        if eml:
            records.append(eml)
            LOG.info("线程[{}]处理了[{}]".format(threading.currentThread().name, len(records)))
    header = ["subject", "from", "to", "content"]
    excel_utils.write_csv(csv_path + str(round(time.time() * 1000)) + ".csv", header, records, signal_out)
