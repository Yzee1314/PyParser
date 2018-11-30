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


from pyparser.cores.celery_workers.parser import parse
from pyparser.cores.celery_workers.save import save_to_local_file
from pyparser.utils.logger import LoggerManager


class ConfigField:

    class TaskConfig:
        app_id = 'app_id'
        task_id = 'task_id'

    class SaveConfig:
        need_save = 'need_save'
        save_type = 'save_type'

    class ResultInfo:
        url = 'url'
        unikey = 'unikey'
        content = 'content'
        result_meta = 'result_meta'
        timestamp = 'timestamp'

    class ParseConfig:
        root = 'parse_config'
        parse_template = 'parse_template'


class Values:

    class SaveType:
        local_file = 'local_file'
        oss_file = 'oss_file'


class ParseProcessor(object):

    def __init__(self):
        self.logger = LoggerManager.get_logger(__file__)

    def handle(self, item):
        """
            handle
        """
        app_id = item.get(
            ConfigField.TaskConfig.app_id, None)
        task_id = item.get(
            ConfigField.TaskConfig.task_id, None)
        if (not app_id) or (not task_id):
            self.logger.info(
                '[EmptyTaskConfig] {} {}'.format(task_id, app_id)
            )
            return
        url = item.get(
            ConfigField.ResultInfo.url, None)
        unikey = item.get(
            ConfigField.ResultInfo.unikey, None)
        content = item.get(
            ConfigField.ResultInfo.content, None)
        result_meta = item.get(
            ConfigField.ResultInfo.result_meta, None)
        if not unikey or not content:
            self.logger.info(
                '[EmptyResultInfo] {} {}'.format(unikey, content)
            )
            return
        need_save = item.get(
            ConfigField.SaveConfig.need_save, True)
        save_type = item.get(
            ConfigField.SaveConfig.save_type,
            Values.SaveType.local_file
        )
        if need_save:
            if save_type == Values.SaveType.local_file:
                save_to_local_file.apply_async(
                    kwargs={
                        'app_id': app_id,
                        'task_id': task_id,
                        'url': url,
                        'unikey': unikey,
                        'content': content,
                        'result_meta': result_meta
                    }
                )
            else:
                self.logger.info(
                    '[WrongSaveType] {}'.format(save_type)
                )
        parse.apply_async(
            kwargs={
                'app_id': app_id,
                'task_id': task_id,
                'unikey': unikey,
                'url': url,
                'content': content,
                'result_meta': result_meta
            }
        )
