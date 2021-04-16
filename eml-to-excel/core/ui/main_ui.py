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

from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QWidget, QGridLayout, QPushButton, \
    QListWidget, QLabel, QFileDialog, QLineEdit, QRadioButton

from core.handler.sync_handler import SyncThread


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initQMainWindow()

    def initQMainWindow(self):
        """
            初始化界面

            :return:
        """
        self.creatFormGroupBox()
        self.createGridGroupBox()
        main_layout = QVBoxLayout()
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.grid_group_excel)
        main_layout.addWidget(self.form_group_box)
        main_layout.addLayout(hbox_layout)
        self.setLayout(main_layout)
        self.setFixedSize(640, 520)
        self.setWindowTitle("EML文件解析")
        self.setWindowIcon(QIcon("./favicon.ico"))

    def creatFormGroupBox(self):
        """
            UI 日志输出区域

            :return:
        """
        self.form_group_box = QGroupBox("输出区域")
        layout = QFormLayout()
        self.text_edit = QListWidget()
        self.text_edit.setFixedSize(600, 400)
        layout.addRow(self.text_edit)
        self.form_group_box.setLayout(layout)

    def createGridGroupBox(self):
        """
            EML 操作区域

            :return:
        """
        self.grid_group_excel = QGroupBox("EML 操作区域")
        layout = QGridLayout()

        eml_dir_label = QLabel("EML目录:")
        self.content_type = QLineEdit()
        self.content_type.setReadOnly(True)
        self.content_type.setPlaceholderText("处理EML目录")
        btn_eml_change = QPushButton("选择")
        btn_eml_change.clicked.connect(self.changeEmlDir)

        csv_dir_label = QLabel("生成目录:")
        self.csv_dir = QLineEdit()
        self.csv_dir.setReadOnly(True)
        self.csv_dir.setPlaceholderText("生成excel存放目录")
        btn_csv_change = QPushButton("选择")
        btn_csv_change.clicked.connect(self.changeCsvDir)

        type_label = QLabel("解析类型:")
        self.t1 = QRadioButton(self)
        self.t1.setText("文本")
        self.t1.setChecked(True)
        self.t2 = QRadioButton(self)
        self.t2.setText("HTML")

        total_label = QLabel("处理数量:")
        self.total = QLineEdit()
        self.total.setText("10000")
        self.total.setValidator(QIntValidator())
        self.total.setPlaceholderText("处理数量,默认10000")

        btn_parsing = QPushButton("解析")
        btn_parsing.clicked.connect(self.execute)
        layout.addWidget(eml_dir_label, 0, 0)
        layout.addWidget(self.content_type, 0, 1)
        layout.addWidget(btn_eml_change, 0, 2)
        layout.addWidget(csv_dir_label, 0, 3)
        layout.addWidget(self.csv_dir, 0, 4)
        layout.addWidget(btn_csv_change, 0, 5)

        layout.addWidget(type_label, 1, 0)
        layout.addWidget(self.t1, 1, 1)
        layout.addWidget(self.t2, 1, 2)
        layout.addWidget(total_label, 1, 3)
        layout.addWidget(self.total, 1, 4)
        layout.addWidget(btn_parsing, 1, 5)
        layout.setColumnStretch(5, 1)
        self.grid_group_excel.setLayout(layout)

    def changeEmlDir(self):
        """
            文件选择器

            :return:
        """
        directory = QFileDialog.getExistingDirectory(self)
        if not directory:
            return
        self.printMsg("{} 选中目录: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), directory))
        self.content_type.setText(directory)

    def changeCsvDir(self):
        """
            文件选择器

            :return:
        """
        directory = QFileDialog.getExistingDirectory(self)
        if not directory:
            return
        self.printMsg("{} 选中目录: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), directory))
        self.csv_dir.setText(directory)

    def printMsg(self, log):
        """
            界面打印日志

            :param log: 日志
            :return:
        """
        self.text_edit.addItem(log)
        # 自动滚动
        self.text_edit.setCurrentRow(self.text_edit.count() - 1)

    def execute(self):
        """
            执行处理信号槽

            :return:
        """
        eml_path = self.content_type.text().strip()
        out_path = self.csv_dir.text().strip()
        content_type = "text/plain"
        if self.t2.isChecked():
            content_type = "text/html"
        total = self.total.text().strip()
        if not eml_path:
            self.printMsg("{} 请选择要解析的EML文件目录...".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return
        if not out_path:
            self.printMsg("{} 请选择要解析文件存储目录...".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return
        if total and int(total) <= 0:
            self.printMsg("{} 处理数量必须大于0...".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return
        self.t3 = SyncThread()
        self.t3.set_param(eml_path, out_path, content_type, total)
        self.t3.signal_out.connect(self.printMsg)
        self.t3.start()
