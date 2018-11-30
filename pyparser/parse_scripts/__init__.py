#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# __init__.py
# @Author : PengYingzhi
# @Date   : 8/22/2018, 11:59:23 AM

import importlib
import os
import pickle
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from pyparser.settings import PROJECT_PATH, SCRIPT_MANAGER_CONFIG
from pyparser.utils.redis import RedisManager


class ConfigField:

    class RedisConfig:
        root = 'redis_config'
        host = 'host'
        port = 'port'


redis_config = SCRIPT_MANAGER_CONFIG.get(
    ConfigField.RedisConfig.root, {})
redis_conn = RedisManager.get_redis_conn(
    host=redis_config.pop(ConfigField.RedisConfig.host, '127.0.0.1'),
    port=redis_config.pop(ConfigField.RedisConfig.port, 6379),
    **redis_config
)


class ScriptWatchHandler(FileSystemEventHandler):

    def on_modified(self, event):
        """
            on_modified
        """
        if event.src_path.endswith('__init__.py') \
                or 'pycache' in event.src_path:
            return
        app_id = os.path.basename(event.src_path).rstrip('.py')
        parser = ScriptManager.load_parser_instance(app_id)
        if parser:
            ScriptManager.pickle_parser_to_redis(app_id, parser)
            ScriptManager.update_script_status(
                app_id, ScriptManager.Status.change)


class ScriptManager(object):
    """
        Load the parser scripts. Once the script has changed, the manager
        would load the parser instance to the redis.
    """

    class Status:
        change = 1
        no_change = 0

    SAVE_SCRIPT_KEY = 'pyparser:scripts'
    UPDATE_STATUS_KEY = 'pyparser:scripts:update:status'
    parser_instances = {}

    def __init__(self):
        self.__init_scripts()

    def __init_scripts(self):
        """
            Init the scripts.
        """
        script_dir_path = SCRIPT_MANAGER_CONFIG.get(
            'script_dir_path', None)
        if not script_dir_path:
            script_dir_path = os.path.join(
                PROJECT_PATH, 'parse_scripts')
        for fname in os.listdir(script_dir_path):
            if fname != '__init__.py' \
                    and (not fname.startswith('__')):
                app_id = fname.rstrip('.py')
                parser = ScriptManager.load_parser_instance(
                    app_id, reload=False)
                self.pickle_parser_to_redis(app_id, parser)
                ScriptManager.update_script_status(
                    app_id, ScriptManager.Status.no_change)
                self.parser_instances[app_id] = parser

    @classmethod
    def load_parser_instance(cls, app_id, reload=True):
        """
            Load module
        """
        module = importlib.import_module(
            'pyparser.parse_scripts.{}'.format(app_id))
        if reload:
            importlib.reload(module)
        for attr in dir(module):
            if 'Parser' in attr \
                    and attr != 'Parser':
                parser = getattr(module, attr)()
                return parser
        return None

    @classmethod
    def pickle_parser_to_redis(cls, app_id, parser):
        """
            Pickle parser to redis.
        """
        redis_conn.hset(
            cls.SAVE_SCRIPT_KEY,
            app_id,
            pickle.dumps(parser)
        )

    @classmethod
    def update_script_status(cls, app_id, status):
        """
            Update script status.
        """
        redis_conn.hset(
            cls.UPDATE_STATUS_KEY,
            app_id,
            status
        )

    def get_parser_instance(self, app_id):
        """
            Return a parser instance
        """
        status = redis_conn.hget(self.UPDATE_STATUS_KEY, app_id)
        if status \
                and status.isdigit() \
                and int(status) == ScriptManager.Status.change:
            parser = ScriptManager.load_parser_instance(app_id)
            ScriptManager.pickle_parser_to_redis(app_id, parser)
            ScriptManager.update_script_status(
                app_id, ScriptManager.Status.no_change)
            parser = redis_conn.hget(
                self.SAVE_SCRIPT_KEY, app_id)
            self.parser_instances[app_id] = pickle.loads(parser)
        return self.parser_instances.get(app_id, None)

    def run(self):
        """
            run
        """
        script_dir_path = SCRIPT_MANAGER_CONFIG.get(
            'script_dir_path', None)
        if not script_dir_path:
            script_dir_path = os.path.join(
                PROJECT_PATH, 'parse_scripts')
        print(script_dir_path)
        event_handler = ScriptWatchHandler()
        observer = Observer()
        observer.schedule(
            event_handler, path=script_dir_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class Parser(object):

    class ResultType:
        IGNORE = 'IGNORE'
        NORMAL = 'NORMAL'

    class Model(object):
        uri = 'mongodb://localhost:27017/'
        db = None
        col = None

    def get_model(self):
        """
            Return the parser model
        """
        if not hasattr(self, 'model'):
            self.model = self.Model()
        if not self.model:
            self.model = self.Model()
        return self.model

    def parse(self,
              unikey,
              url,
              content,
              meta):
        """
            Params:
            * unikey:    (string) - A unique key of the content.
            * url:       (string) - Where the content comes from.
            * content:   (string) - Content.
            * meta:      (dict)   - Other information of content.

            Returns:
            * ok:        (bool)                - the status of result
            * result:    (dict|list|generator) - result
        """
        pass
