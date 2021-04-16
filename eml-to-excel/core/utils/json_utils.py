#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- 
# --
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2021/3/10 15:17
# Email lmay@lmaye.com
# ----------------------------------------------------------
import json

from core import LOG


def write_json(json_file, records):
    with open(json_file, "w", encoding="utf-8-sig") as file:
        json_dirt = {"RECORDS": records}
        json_str = json.dumps(json_dirt)
        file.write(json_str)
        LOG.info("写入CSV文件: {}, [{}]数据".format(json_file, len(records)))
