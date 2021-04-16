#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 应用启动程序 - 邮件解析工具
# -- pyinstaller -F -w app.py -i "E:\workspace\Java\widget\eml-to-excel\favicon.ico" --version-file=E:\workspace\Java\widget\eml-to-excel\version.txt -n EmlToExcel.exe
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2021/4/14 9:45
# Email lmay@lmaye.com
# ----------------------------------------------------------
import sys

from PyQt5.QtWidgets import QApplication

from core.ui.main_ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appMain = MainWindow()
    appMain.show()
    sys.exit(app.exec_())

