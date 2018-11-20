#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sjqq_02.py
# @Author : PengYingzhi
# @Date   : 10/17/2018, 2:53:15 PM

import random as rd

from . import Parser


class BaseParser(Parser):

    class Model:
        uri = 'mongodb://localhost:27017/'
        db = 'spider'
        col = 'test_01'

    def parse(self, unikey, url, content, meta):
        """
            parse
        """
        crawl_time = meta.get('crawltime', None)
        for i, word in enumerate(content.split(' ')):
            unikey = rd.randint(0, 20)
            yield True, {
                'unikey': unikey,
                'num': rd.randint(0, 4),
                'word': word,
                'url': url,
                'crawltime': crawl_time
            }, ''

    def validate(self, data):
        """
            validate
        """
        if 'num' not in data:
            return False, 'missing num'
        else:
            if data['num'] % 2 == 0:
                return True, 'success'
            else:
                return False, 'wrong value'
