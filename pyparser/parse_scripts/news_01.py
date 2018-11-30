#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sjqq_02.py
# @Author : PengYingzhi
# @Date   : 10/17/2018, 2:53:15 PM


from pyquery import PyQuery

from . import Parser
from pyparser.utils.string import md5


class BaseParser(Parser):

    class Model:
        uri = 'mongodb://localhost:27017/'
        db = 'spider'
        col = 'news'

    def parse(self, unikey, url, content, meta):
        """
            parse
        """
        if 'news.baidu.com' not in url:
            yield False, None, self.ResultType.IGNORE
            return
        doc = PyQuery(content)
        for item in doc('.ulist a').items():
            yield True, {
                'unikey': md5(item.attr('href')),
                'url': item.attr('href'),
                'title': item.text().strip()
            }, self.ResultType.NORMAL

    def validate(self, data):
        """
            validate
        """
        if data.get('url', None) \
                and data.get('title', None):
            return True, self.ResultType.NORMAL
        else:
            return False, 'missing url or title'
