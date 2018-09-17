#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# redis_monitor.py
# @Author : PengYingzhi
# @Date   : 9/10/2018, 4:58:07 PM

import time
import traceback

from pyparser.utils.redis import RedisManager
from settings import REDIS_MONITOR_CONFIG


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
        if queue not in self.queue_pop_func:
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
    def __init__(self, host, port, db, **args):
        super(ItemRedisMonitor, self).__init__(host, port, db, **args)

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
                if is_free:
                    time.sleep(wait_result_interval)
            except Exception:
                traceback.print_exc()
                has_retry += 1
            if has_retry > retry_max:
                break
            time.sleep(sleep_interval)
