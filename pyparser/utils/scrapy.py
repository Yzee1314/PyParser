#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# scrapy.py
# @Author : PengYingzhi
# @Date   : 11/18/2018, 8:12:05 AM

from copy import deepcopy
from datetime import datetime

from utils.string import md5


class Values:

    class TimeUnit:
        minute = 'minute'
        hour = 'hour'
        day = 'day'
        formats = {
            minute: '%Y-%m-%d %H:%M',
            hour: '%Y-%m-%d %H',
            day: '%Y-%m-%d'
        }


class ConfigField:

    class ResultField:
        app_id = 'app_id'
        task_id = 'task_id'
        unikey = 'unikey'
        url = 'url'
        content = 'content'
        result_meta = 'result_meta'


class ResultGenerator(object):
    """
        Generate result from `Scrapy.Response`
    """

    @classmethod
    def get_result_from_response(cls,
                                 response,
                                 time_unit=Values.TimeUnit.hour):
        """
            Get result from `Scrapy.Response`
        """
        time_fmt = Values.TimeUnit.formats.get(
            time_unit, Values.TimeUnit.formats[Values.TimeUnit.hour])
        meta = deepcopy(response.meta)
        url = meta.pop(ConfigField.ResultField.url, None) \
            or response.request.url or response.url
        content = meta.pop(ConfigField.ResultField.content, None) \
            or response.body
        app_id = meta.pop(ConfigField.ResultField.app_id, None)
        if not app_id:
            # This is a necessary field
            return None
        task_id = meta.get(ConfigField.ResultField.task_id, None)
        if not task_id:
            current_time = datetime.now().strftime(time_fmt)
            task_id = md5(current_time)
        unikey = meta.pop(ConfigField.ResultField.unikey, None)
        if not unikey:
            unikey = md5(content)
        result_meta = meta.pop(ConfigField.ResultField.result_meta, None)
        return {
            ConfigField.ResultField.app_id: app_id,
            ConfigField.ResultField.task_id: task_id,
            ConfigField.ResultField.unikey: unikey,
            ConfigField.ResultField.url: url,
            ConfigField.ResultField.content: content,
            ConfigField.ResultField.meta: result_meta
        }


class PyParserPipeline(object):
    """
        pyparser pipeline
    """
    pass
