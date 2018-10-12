#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# parse.py
# @Author : PengYingzhi
# @Date   : 9/18/2018, 11:12:16 AM

"""
    Parse Layer, includes the following workers:
        1. save worker
        2. parse worker
"""


import simplejson as json

from cores.celery_workers.save import save_to_local_file
from cores.celery_workers.parser import parse
from utils.logger import LoggerManager


class ConfigField:

    class TaskConfig:
        root = 'task_config'
        app_id = 'app_id'
        task_id = 'task_id'

    class SaveConfig:
        root = 'save_config'
        need_save = 'need_save'
        save_type = 'save_type'

    class ResultInfo:
        root = 'result_info'
        url = 'url'
        uniqkey = 'uniqkey'
        content = 'content'
        meta = 'meta'
        timestamp = 'timestamp'

    class ParseConfig:
        root = 'parse_config'
        parse_template = 'parse_template'


class Values:

    class SaveType:
        local_file = 'local_file'
        oss_file = 'oss_file'


class ParseLayer(object):

    def __init__(self):
        self.logger = LoggerManager.get_logger(__file__)

    def input(self, item):
        """
            Parse layer input
        """
        task_config = item.pop(
            ConfigField.TaskConfig.root, {})
        app_id = task_config.get(
            ConfigField.TaskConfig.app_id, None)
        task_id = task_config.get(
            ConfigField.TaskConfig.task_id, None)
        if not app_id or not task_config:
            self.logger.info(
                '[EmptyTaskConfig] {} {}'.format(task_id, app_id)
            )
            return
        result_info = item.pop(
            ConfigField.ResultInfo.root, {})
        url = result_info.get(
            ConfigField.ResultInfo.root, None)
        unikey = result_info.get(
            ConfigField.ResultInfo.uniqkey, None)
        content = result_info.get(
            ConfigField.ResultInfo.content, None)
        meta = result_info.get(
            ConfigField.ResultInfo.meta, None)
        if not unikey or not content:
            self.logger.info(
                '[EmptyResultInfo] {} {}'.format(unikey, content)
            )
            return
        persist_config = item.pop(
            ConfigField.SaveConfig.root, {})
        need_save = persist_config.get(
            ConfigField.SaveConfig.need_save, True)
        save_type = persist_config.get(
            ConfigField.SaveConfig.save_type,
            Values.SaveType.local_file
        )
        if need_save:
            if save_type == Values.SaveType.local_file:
                save_to_local_file.apply_async(
                    {
                        'app_id': app_id,
                        'task_id': task_id,
                        'url': url,
                        'unikey': unikey,
                        'content': content,
                        'meta': meta
                    }
                )
            else:
                self.logger.info(
                    '[WrongSaveType] {}'.format(save_type)
                )

    def output(self):
        """
            Parse layer output
        """
        pass
