#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# settings.py
# @Author : PengYingzhi
# @Date   : 9/17/2018, 5:20:26 PM


from pyparser.utils.yaml import load_yaml_config


REDIS_MONITOR_CONFIG = load_yaml_config('configs/redis_monitor.yaml')
