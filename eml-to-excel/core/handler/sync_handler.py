#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# --
# --
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2021/4/14 11:13
# Email lmay@lmaye.com
# ----------------------------------------------------------
import datetime
import os
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, QThread

from core.constant.sys_enum import SysEnum
from core.handler.thread_handler import thread_list


class SyncThread(QThread):
    """
        SyncExecuteThread

        -- 同步执行线程
    """
    signal_out = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SyncThread, self).__init__(parent)
        self.threadName = "MyThread"
        self.rows = None

    def set_param(self, eml_path, out_path, content_type, total):
        self.eml_path = eml_path
        self.out_path = out_path
        self.content_type = content_type
        self.lens = total if total else 10000

    def run(self):
        """
            执行
        """
        self.signal_out.emit("{} -->>> 开始执行 ...".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        try:
            threads = []
            for root, dirs, files in os.walk(self.eml_path):
                if 0 < len(files):
                    file_names = os.listdir(root)
                    csv_path = Path(self.out_path + root.replace(self.eml_path, ""))
                    if not csv_path.exists():
                        os.makedirs(csv_path)
                    thread_list(threads, file_names, root + SysEnum.SEPARATOR.value, str(csv_path) + SysEnum.SEPARATOR.value,
                                int(self.lens), self.content_type, self.signal_out)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        except Exception as e:
            self.signal_out.emit("{} 执行异常: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e))
            return None
        self.signal_out.emit("======================= 执行完成 =======================")
