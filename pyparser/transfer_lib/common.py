#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# common.py
# @Author : PengYingzhi
# @Date   : 8/22/2018, 12:08:07 PM


def camel_to_underline(string):
    """
        驼峰字符串转成下划线
    """
    ret = []
    for i, c in enumerate(string):
        if i < (len(string) - 1):
            if c.islower():
                ret.append(c)
            else:
                ret.append('_')
                ret.append(c.lower())
        else:
            ret.append(c)
    return ''.join(ret)
