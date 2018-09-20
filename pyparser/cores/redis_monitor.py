#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# redis_monitor.py
# @Author : PengYingzhi
# @Date   : 9/10/2018, 4:58:07 PM


from concurrent.futures import ProcessPoolExecutor
import time
import traceback

from pyparser.cores.layers.parse import ParseLayerProducer
from pyparser.utils.redis import RedisManager
from settings import REDIS_MONITOR_CONFIG


class ConfigField:

    class RedisInstanceConfig:
        root = 'redis_instance_list'
        host = 'host'
        port = 'port'
        db = 'db'

    class ParseLayerProducerConfig:
        root = 'parse_layer_config'
        servers = 'servers'


class RedisMonitor(object):
    """
        Redis监控类基类
    """
    def __init__(self, host, port, db, **args):
        self.redis_conn = RedisManager.get_redis_conn(
            host, port, db, **args)
        self.queue_pop_func = {}

    def pop_item_from_queue(self, queue):
        """
            Pop item from result queue
        """
        queue_type = self.redis_conn.type(queue)
        pop_func = self.redis_conn.lpop \
            if queue_type == 'list' else self.redis.spop
        return pop_func(queue)

    def run(self):
        """
            run
        """
        raise NotImplementedError('You must implement this method.')


class ItemRedisMonitor(RedisMonitor):
    """
        Item-Redis监控模块
    """
    def __init__(self, host, port, db, parse_layer_producer, **args):
        super(ItemRedisMonitor, self).__init__(host, port, db, **args)
        self.parse_layer_producer = parse_layer_producer

    def run(self):
        """
            run
        """
        has_retry = 0
        retry_max = REDIS_MONITOR_CONFIG.get('retry_max', 3)
        sleep_interval = REDIS_MONITOR_CONFIG.get('sleep_interval', 0.001)
        wait_result_interval = REDIS_MONITOR_CONFIG.get(
            'wait_result_interval', 1)
        while True:
            try:
                is_free = True
                for result_queue_name in self.redis_conn.keys('*:items'):
                    item = self.pop_item_from_queue(result_queue_name)
                    if not item:
                        continue
                    is_free = False
                    self.parse_layer_producer.produce(item)
                if is_free:
                    time.sleep(wait_result_interval)
            except Exception:
                traceback.print_exc()
                has_retry += 1
            if has_retry > retry_max:
                break
            time.sleep(sleep_interval)


class ItemRedisMonitorManager(object):

    def __init__(self):
        self.monitors = []
        self.__init_redis_monitors()

    def __init_redis_monitors(self):
        """
            Init redis monitors
        """
        redis_instance_list = REDIS_MONITOR_CONFIG.get(
            ConfigField.RedisInstanceConfig.root,
            []
        )
        if not redis_instance_list:
            redis_instance_list = [
                {
                    ConfigField.RedisInstanceConfig.host: 'localhost',
                    ConfigField.RedisInstanceConfig.port: 6379,
                    ConfigField.RedisInstanceConfig.db: 0
                }
            ]
        for redis_instance in redis_instance_list:
            parse_layer_producer_config = redis_instance.get(
                ConfigField.ParseLayerProducerConfig.root, {})
            servers = parse_layer_producer_config.get(
                ConfigField.ParseLayerProducerConfig.servers,
                ['localhost:9092']
            )
            parse_layer_producer = ParseLayerProducer(
                bootstrap_servers=servers)
            monitor = ItemRedisMonitor(
                host=redis_instance.get(
                    ConfigField.RedisInstanceConfig.host, 'localhost'),
                port=redis_instance.get(
                    ConfigField.RedisInstanceConfig.port, 6379),
                db=redis_instance.get(ConfigField.RedisInstanceConfig.db, 0),
                parse_layer_producer=parse_layer_producer
            )
            self.monitors.append(monitor)

    def run(self):
        """
            run monitors
        """
        with ProcessPoolExecutor(
            max_workers=len(self.monitors)
        ) as executor:
            for monitor in self.monitors:
                executor.submit(monitor.run)
