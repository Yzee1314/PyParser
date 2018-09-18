#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# parse.py
# @Author : PengYingzhi
# @Date   : 9/18/2018, 11:12:16 AM

"""
    Parse Layer
"""

from multiprocessing import Pool

from kafka import (
    KafkaProducer
)
import simplejson as json

from . import BaseConsumer


def value_serializer(obj):
    """
        value_serializer
    """
    return json.dumps(obj).encode('utf-8')


class ConfigField:

    class PersistConfig:
        root = 'persist_config'
        is_persist = 'is_persist'
        persist_type = 'persist_type'

    class ResultInfo:
        root = 'result_info'
        uniqkey = 'uniqkey'
        content = 'content'

    class ParseConfig:
        root = 'parse_config'
        parse_template = 'parse_template'


class Topics:

    persist_content_topic = 'persist_content_topic'
    parse_topic = 'parse_topic'


class ParseLayer(object):

    def __init__(self, input_processor, ):
        pass

    def input(self, item):
        """
            Parse layer input
        """
        pass


class ParseLayerProducer(KafkaProducer):

    def __init__(self, **config):
        super(ParseLayerProducer, self).__init__(
            value_serializer=value_serializer,
            **config
        )

    def produce(self, item):
        """
            Params:
            * item:    (dict) - result
        """
        obj = json.loads(item)
        persist_config = obj.get(ConfigField.PersistConfig.root, {})
        if persist_config.pop(ConfigField.PersistConfig.is_persist, False):
            self.send(Topics.persist_content_topic, obj)
        self.send(Topics.parse_topic, obj)


class PersistContentConsumer(BaseConsumer):
    """
        Save the web content
    """
    def __init__(self, **config):
        super(PersistContentConsumer, self).__init__(**config)

    def consume(self, item):
        """
            consume
        """
        pass


class ParseConsumer(BaseConsumer):
    """
        Recevie the content and load the parse script to extract data
    """
    def __init__(self, **config):
        super(ParseConsumer, self).__init__(**config)

    def consume(self, item):
        """
            consume
        """
        pass
