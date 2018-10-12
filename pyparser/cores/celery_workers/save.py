#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# save.py
# @Author : PengYingzhi
# @Date   : 9/27/2018, 10:46:17 AM


import os

from celery import Task
import simplejson as json

from . import app
from settings import PROJECT_PATH, SAVE_WORKER_CONFIG
from utils.logger import (
    FormatFactory,
    FileLoggerFactory,
    LoggerManager
)


class ConfigField:

    class Path:
        root = 'path'
        result_save_dir_path = 'result_save_dir_path'
        log_save_dir_path = 'log_save_dir_path'


class SaveTask(Task):
    """
        Save content task
    """
    def __init__(self):
        self.logger = LoggerManager.get_logger(__file__)
        self.save_path_config = SAVE_WORKER_CONFIG.get(
            ConfigField.Path.root,
            {}
        )
        self.result_save_dir_path = self.save_path_config.get(
            ConfigField.Path.result_save_dir_path,
            os.path.join(PROJECT_PATH, 'result')
        )
        self.log_save_dir_path = SAVE_WORKER_CONFIG.get(
            ConfigField.Path.log_save_dir_path,
            os.path.join(PROJECT_PATH, 'log')
        )


@app.task(bind=True, base=SaveTask)
def save_to_local_file(self,
                       app_id,
                       task_id,
                       unikey,
                       content,
                       url,
                       meta=None):
    """
        Save content to local file

        Params:
        * app_id
        * task_id
        * unikey
        * content
        * url
        * meta
    """
    result_dir_path = os.path.join(
        self.result_save_dir_path, app_id, task_id)
    if not os.path.exists(result_dir_path):
        os.makedirs(result_dir_path)
    file_path = os.path.join(result_dir_path, unikey)
    with open(file_path, 'w') as fp:
        fp.write(content)
    log_dir = os.path.join(self.log_save_dir_path, app_id)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = os.path.join(log_dir, task_id + '.log')
    record = {
        'app_id': app_id,
        'task_id': task_id,
        'unikey': unikey,
        'url': url,
        'meta': meta
    }
    with open(log_path, 'a') as fp:
        fp.write(json.dumps(record) + '\n')
