#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# __init__.py
# @Author : PengYingzhi
# @Date   : 9/18/2018, 11:11:54 AM

import time
import traceback

from kafka import KafkaConsumer


class BaseConsumer(KafkaConsumer):

    def __init__(self, *args, **kwargs):
        self.topics = kwargs.pop(
            'topics', None)
        KafkaConsumer.__init__(
            self, *args, **kwargs)
        self.sleep_interval = kwargs.pop(
            'sleep_interval', 0.01)
        self.max_retry = kwargs.pop(
            'max_retry', 3)
        self.subscribe(topics=self.topics)

    def consume(self, item):
        """
            consume
        """
        raise NotImplementedError(
            'You must implement `consume` method')

    def run(self):
        """
            run
        """
        has_retry = 0
        while True:
            try:
                for item in self:
                    self.consume(item)
            except Exception:
                traceback.print_exc()
                has_retry += 1
            time.sleep(self.sleep_interval)
            if has_retry > self.max_retry:
                break
