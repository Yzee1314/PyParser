#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# __init__.py
# @Author : PengYingzhi
# @Date   : 11/13/2018, 11:58:22 AM


class Model(object):

    def __init__(self,
                 uri='mongodb://localhost:27017/',
                 db=None,
                 col=None):
        self.uri = uri
        self.db = db
        self.col = col
