#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sjqq_01.py
# @Author : PengYingzhi
# @Date   : 8/22/2018, 12:03:30 PM

import json
import traceback

from parse_lib import BaseParser
from transfer_lib.common import camel_to_underline


class Sjqq_01(BaseParser):

    def extract_items(self, content, meta=None):
        """
            extract_items
        """
        try:
            obj = json.loads(content)
            for item in obj.get('obj', {}).get('appDetails', []):
                result = {}
                for key, value in item.items():
                    result[camel_to_underline(key)] = value
                app_rating_info = result.pop('app_rating_info', {})
                result['average_rating'] = \
                    app_rating_info['average_rating']
                result['rating_distribution'] = \
                    app_rating_info['rating_distribution']
                result['rating_count'] = \
                    app_rating_info['rating_count']
                yield result
        except ValueError as e:
            traceback.print_exc()
