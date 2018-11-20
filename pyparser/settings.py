#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# settings.py
# @Author : PengYingzhi
# @Date   : 9/17/2018, 5:20:26 PM

import os

from utils.yaml import load_yaml_config


def get_project_path():
    """
        return project path
    """
    current = os.path.abspath(__file__)
    return os.path.dirname(current)


PROJECT_PATH = get_project_path()
REDIS_MONITOR_CONFIG = load_yaml_config(
    os.path.join(
        PROJECT_PATH,
        'configs',
        'redis_monitor.yaml'
    )
)
SAVE_WORKER_CONFIG = load_yaml_config(
    os.path.join(
        PROJECT_PATH,
        'configs',
        'save_worker.yaml'
    )
)
PARSER_WORKER_CONFIG = load_yaml_config(
    os.path.join(
        PROJECT_PATH,
        'configs',
        'parse_worker.yaml'
    )
)
VALIDATE_WORKER_CONFIG = load_yaml_config(
    os.path.join(
        PROJECT_PATH,
        'configs',
        'validate_worker.yaml'
    )
)
STORAGE_WORKER_CONFIG = load_yaml_config(
    os.path.join(
        PROJECT_PATH,
        'configs',
        'storage_worker.yaml'
    )
)
SCRIPT_MANAGER_CONFIG = load_yaml_config(
    os.path.join(
        PROJECT_PATH,
        'configs',
        'script_manager.yaml'
    )
)
