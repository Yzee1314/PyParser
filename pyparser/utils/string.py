#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# string.py
# @Author : PengYingzhi
# @Date   : 11/20/2018, 3:00:24 PM


from hashlib import md5


def md5(string):
    """
    
    Params:
    * string        (str) - original value

    Returns:
    * md5_value:    (str) - new value
    """
    m = md5()
    m.update(string)
    return m.hexdigest()
