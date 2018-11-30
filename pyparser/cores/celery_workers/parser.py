#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# parser.py
# @Author : PengYingzhi
# @Date   : 9/27/2018, 10:54:36 AM

import os
import traceback

from celery import Task
import simplejson as json

from . import app
from pyparser.cores.celery_workers.validator import validate
from pyparser.parse_scripts import Parser, ScriptManager
from pyparser.settings import PARSER_WORKER_CONFIG
from pyparser.utils.logger import LoggerManager


class ConfigField:

    class Path:
        root = 'path'
        parse_result_dir_path = 'parse_result_dir_path'
        parse_failed_log_dir_path = 'parse_failed_log_dir_path'


class ParseTask(Task):
    """
        Parse content task
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
        self.parse_failed_log_dir_path = self.parse_result_config.get(
            ConfigField.Path.parse_failed_log_dir_path,
            'parse_failed_log'
        )


@app.task(bind=True, base=ParseTask)
def parse(self,
          app_id,
          task_id,
          unikey,
          url,
          content,
          result_meta):
    task_parse_result_dir = os.path.join(
        self.parse_result_dir_path,
        app_id,
        task_id
    )
    if not os.path.exists(task_parse_result_dir):
        os.makedirs(task_parse_result_dir)
    task_parse_failed_log_dir = os.path.join(
        self.parse_failed_log_dir_path,
        app_id
    )
    if not os.path.exists(task_parse_failed_log_dir):
        os.makedirs(task_parse_failed_log_dir)
    task_parse_failed_log_path = os.path.join(
        task_parse_failed_log_dir,
        task_id + '.log'
    )
    failed_message = {
        'app_id': app_id,
        'task_id': task_id,
        'unikey': unikey,
        'error': None,
        'result': None
    }
    try:
        parser = self.script_manager.get_parser_instance(app_id)
        for ok, result, msg in parser.parse(unikey, url, content, result_meta):
            if msg == Parser.ResultType.IGNORE:
                continue
            if ok:
                result_path = os.path.join(task_parse_result_dir, unikey)
                with open(result_path, 'a') as fp:
                    fp.write(json.dumps(result) + '\n')
            else:
                failed_message['error'] = msg
                failed_message['result'] = result
                with open(task_parse_failed_log_path, 'a') as fp:
                    fp.write(json.dumps(failed_message) + '\n')
        validate.apply_async(
            kwargs={
                'app_id': app_id,
                'task_id': task_id,
                'unikey': unikey
            }
        )
    except Exception as e:
        traceback.print_exc()
        failed_message['error'] = repr(e)
        with open(task_parse_failed_log_path, 'a') as fp:
            fp.write(json.dumps(failed_message) + '\n')
