#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# redis.py
# @Author : PengYingzhi
# @Date   : 9/17/2018, 5:01:35 PM


import redis


class RedisManager(object):

    instances = {}

    @classmethod
    def get_instance_unikey(cls, host, port, db):
        """
            获取实例的唯一映射
        """
        key = host + str(port) + str(db)
        return key

    @classmethod
    def get_redis_conn(cls,
                       host='127.0.0.1',
                       port=6379,
                       db=0,
                       force_instance=False,
                       **kwargs):
        """
            get redis client
        """
        if force_instance:
            return redis.Redis(
                host, port, db, decode_responses=True)
        unikey = cls.get_instance_unikey(host, port, db)
        if unikey not in cls.instances:
            conn = redis.Redis(
                host, port, db, **kwargs)
            cls.instances[unikey] = conn
        return cls.instances[unikey]
