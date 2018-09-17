#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# yaml.py
# @Author : PengYingzhi
# @Date   : 9/17/2018, 5:21:25 PM

import os

import yaml


def load_yaml_config(path):
    """
        读取YAML文件
    """
    if not os.path.exists(path):
        return {}
    with open(path) as fp:
        return yaml.load(fp)
