#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- Excel 文件工具类
# --
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2021年1月12日 18:14:02
# ----------------------------------------------------------
import csv
import datetime

import xlrd
import xlwt

from core import LOG


def read_excel(excel_file, sheet_index):
    """
    读取excel数据

    :param excel_file: excel文件
    :param sheet_index: sheet索引
    :return: list
    """
    records = []
    data = xlrd.open_workbook(excel_file)
    table = data.sheet_by_index(sheet_index)
    # 获取表头作为key
    table_key = table.row_values(0)
    for row in range(table.nrows - 1):
        dt = {}
        # 行数据
        values = table.row_values(row + 1)
        for col in range(table.ncols):
            dt[table_key[col]] = values[col]
        records.append(dt)
    LOG.info("读取excel, 加载[{}]数据".format(len(records)))
    return records


def write_excel(excel_file, sheet_name, records):
    """
    写入excel数据

    :param excel_file: 保存文件
    :param sheet_name: sheet 名称
    :param records: 数据
    :return:
    """
    LOG.info("[{}]条数据, 写入excel文件: {}".format(len(records), excel_file))
    # 创建一个workbook设置编码
    workbook = xlwt.Workbook("utf-8")
    # 创建一个worksheet
    worksheet = workbook.add_sheet(sheet_name)
    # 写入excel参数对应 行, 列, 值
    row = 0
    for record in records:
        col = 0
        for key in record:
            # 写入excel参数对应 行, 列, 值
            if 0 == row:
                # 表头
                worksheet.write(row, col, key)
            value = record[key]
            # 判断是否dict类型
            if isinstance(value, dict):
                worksheet.write(row + 1, col, str(value))
            else:
                worksheet.write(row + 1, col, value)
            col += 1
        row += 1
    # 保存
    workbook.save(excel_file)


def write_csv(csv_file, header, records, signal_out=None):
    """
    写入CSV文件

    :param csv_file:    CSV文件
    :param header:      表头
    :param records:     记录
    :param signal_out:  界面打印
    :return:
    """
    with open(csv_file, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(records)
        LOG.info("写入CSV文件: {}, [{}]条数据".format(csv_file, len(records)))
        if signal_out:
            signal_out.emit(
                "{} 写入CSV文件: {}, [{}]条数据".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), csv_file,
                                                len(records)))
