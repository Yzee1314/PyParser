#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# __init__.py
# @Author : PengYingzhi
# @Date   : 8/22/2018, 11:58:24 AM


class BaseParser(object):
    """
        解析模块基类
    """

    name = None

    def extract_items(self, content, meta=None):
        """
            extract items from content and meta
        """
        raise NotImplementedError(
            'You must implement `extract_items` method')
