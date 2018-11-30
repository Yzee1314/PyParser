#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# validate.py
# @Author : PengYingzhi
# @Date   : 10/20/2018, 12:23:40 PM


import os
import traceback

from celery import Task
import simplejson as json

from . import app
from .storage import storage
from pyparser.parse_scripts import ScriptManager
from pyparser.settings import (
    PARSER_WORKER_CONFIG,
    VALIDATE_WORKER_CONFIG
)
from pyparser.utils.logger import LoggerManager


class ConfigField:

    class Path:
        root = 'path'
        parse_result_dir_path = 'parse_result_dir_path'
        validate_failed_dir_path = 'validate_failed_dir_path'
        validate_success_dir_path = 'validate_success_dir_path'

    class Others:
        err_msg = 'err_msg'


class ValidateTask(Task):
    """
        ValidateTask
    """
    def __init__(self):
        self.logger = LoggerManager.get_logger(__file__)
        self.script_manager = ScriptManager()
        self.parse_result_config = PARSER_WORKER_CONFIG.get(
            ConfigField.Path.root,
            {}
        )
        self.parse_result_dir_path = self.parse_result_config.get(
            ConfigField.Path.parse_result_dir_path,
            'parse_result'
        )
        self.validate_worker_paths = VALIDATE_WORKER_CONFIG.get(
            ConfigField.Path.root,
            {}
        )
        self.validate_failed_dir_path = self.validate_worker_paths.get(
            ConfigField.Path.validate_failed_dir_path,
            'validate_failed'
        )
        self.validate_sucesss_dir_path = self.validate_worker_paths.get(
            ConfigField.Path.validate_success_dir_path,
            'validate_success'
        )


@app.task(bind=True, base=ValidateTask)
def validate(self, app_id, task_id, unikey):
    """
        validate the results
    """
    task_parse_result_path = os.path.join(
        self.parse_result_dir_path,
        app_id,
        task_id,
        unikey
    )
    if not os.path.exists(task_parse_result_path):
        self.logger.info(
            '[ParseResultDoesNotExists] {}'.format(task_parse_result_path)
        )
        return
    task_validate_failed_dir = os.path.join(
        self.validate_failed_dir_path,
        app_id,
    )
    task_validate_failed_path = os.path.join(
        task_validate_failed_dir,
        task_id,
    )
    if not os.path.exists(task_validate_failed_dir):
        os.makedirs(task_validate_failed_dir)
    task_validate_success_dir = os.path.join(
        self.validate_sucesss_dir_path,
        app_id,
        task_id
    )
    if not os.path.exists(task_validate_success_dir):
        os.makedirs(task_validate_success_dir)
    task_validate_success_path = os.path.join(
        task_validate_success_dir,
        unikey
    )
    try:
        parser = self.script_manager.get_parser_instance(
            app_id)
        with open(task_parse_result_path, 'r') as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line.strip())
                ok, msg = parser.validate(data)
                if ok:
                    with open(task_validate_success_path, 'a') as _fp:
                        _fp.write(line + '\n')
                else:
                    with open(task_validate_failed_path, 'a') as _fp:
                        data[ConfigField.Others.err_msg] = msg
                        _fp.write(json.dumps(data) + '\n')
        storage.apply_async(
            kwargs={
                'app_id': app_id,
                'task_id': task_id,
                'unikey': unikey
            }
        )
    except Exception as e:
        traceback.print_exc()
