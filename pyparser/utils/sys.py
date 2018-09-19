#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sys.py
# @Author : PengYingzhi
# @Date   : 9/19/2018, 11:17:43 AM


def run_in_subprocess(func, *args, **kwargs):
    """
        Run function in subprocess
    """
    from multiprocessing import Process
    process = Process(target=func, args=args, kwargs=kwargs)
    process.daemon = True
    process.start()
    return process
