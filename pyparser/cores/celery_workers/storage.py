#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# storage.py
# @Author : PengYingzhi
# @Date   : 11/7/2018, 11:37:21 AM


"""
    db storage workers
"""


import os

from celery import Task
import simplejson as json

from . import app
from parse_scripts import ScriptManager
from settings import (
    STORAGE_WORKER_CONFIG,
    VALIDATE_WORKER_CONFIG
)
from utils.mongo import MongoManager
from utils.logger import LoggerManager


class ConfigField:

    class Path:
        root = 'path'
        validate_success_dir_path = 'validate_success_dir_path'
        storage_fail_dir_path = 'storage_fail_dir_path'

    class Mongo:
        root = 'mongo'
        uri = 'uri'
        unikey = 'unikey'


class StorageTask(Task):
    """
        StroageTask
    """
    def __init__(self):
        self.logger = LoggerManager.get_logger(__file__)
        self.script_manager = ScriptManager()
        self.mongo_clients = {}
        self.validate_success_path = VALIDATE_WORKER_CONFIG.get(
            ConfigField.Path.validate_success_dir_path, 'validate_success')
        self.storage_fail_dir_path = STORAGE_WORKER_CONFIG.get(
            ConfigField.Path.storage_fail_dir_path, 'storage_fail_dir_path')


@app.task(bind=True, base=StorageTask)
def storage(self, app_id, task_id, unikey):
    """
        db storage
    """
    validate_success_path = os.path.join(
        self.validate_success_path,
        app_id,
        task_id,
        unikey
    )
    if not os.path.exists(self.validate_success_path):
        self.logger.info(
            '[ValidateSuccessPathDoesNotExsits] {}'.format(
                self.validate_success_path)
        )
        return
    task_storage_fail_dir = os.path.join(
        self.storage_fail_dir_path, app_id)
    if not os.path.exists(task_storage_fail_dir):
        os.makedirs(task_storage_fail_dir)
    task_storage_fail_path = os.path.join(
        task_storage_fail_dir, task_id)
    parser = self.script_manager.get_parser_instance(app_id)
    if not parser:
        self.logger.info(
            '[ParserIsNone] {}'.format(app_id)
        )
        return
    model = parser.get_model()
    if not model:
        self.logger.info(
            '[ModelIsNone] {}'.format(app_id)
        )
        return
    uri = model.uri
    db = model.db
    col = model.col
    if not (uri and db and col):
        self.logger.info(
            '[ModelConfigIsNone] {} {} {}'.format(
                uri, db, col)
        )
        return
    if app_id not in self.mongo_clients:
        self.mongo_clients[app_id] = MongoManager.get_mongo_client(
            uri, db, col)
    client = self.mongo_clients[app_id]
    with open(validate_success_path, 'r') as rfp:
        for line in rfp:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                unikey = data.get(ConfigField.Mongo.unikey, None)
                if not unikey:
                    continue
                client.update_one(
                    {
                        ConfigField.Mongo.unikey: unikey
                    },
                    {
                        '$set': data
                    },
                    upsert=True
                )
            except Exception as e:
                with open(task_storage_fail_path, 'a') as wfp:
                    content = {
                        'content': line,
                        'mes': repr(e)
                    }
                    wfp.write(json.dumps(content) + '\n')
