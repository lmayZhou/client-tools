#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's Get Logger
# -- 
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月1日 16:20:04
# ----------------------------------------------------------
import logging.config


def logger():
    log = logging.getLogger("eml-to-excel")
    log.setLevel(level=logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(pathname)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s")
    handler = logging.FileHandler("./eml-to-excel.log")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    log.addHandler(handler)
    log.addHandler(console)
    return log
