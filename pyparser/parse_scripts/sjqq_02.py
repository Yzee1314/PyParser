#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sjqq_02.py
# @Author : PengYingzhi
# @Date   : 10/17/2018, 2:53:15 PM


from . import Parser


class BaseParser(Parser):

    def parse(self, unikey, url, content, meta):
        """
            parse
        """
        crawl_time = meta.get('crawltime', None)
        for word in content.split(' '):
            if word == 'John':
                status = False
                msg = 'people name'
            else:
                status = True
                msg = ''
            yield status, {
                'word': word,
                'url': url,
                'crawltime': crawl_time
            }, msg
