#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# producer.py
# @Author : PengYingzhi
# @Date   : 9/21/2018, 2:40:14 PM


class BaseProducer(object):

    def __init__(self, *args, **kwargs):
        pass

    def produce(self, item, **kwargs):
        """
            produce item
        """
        raise NotImplementedError('You must implement `produce` method.')
