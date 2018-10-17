#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sjqq_02.py
# @Author : PengYingzhi
# @Date   : 10/17/2018, 2:53:15 PM


class BaseParser(object):

    app_id = '10'

    def say_hello(self):
        print('Hello 1', self.app_id)
