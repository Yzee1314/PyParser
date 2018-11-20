#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mongo.py
# @Author : PengYingzhi
# @Date   : 11/7/2018, 5:33:15 PM


import pymongo


class MongoManager(object):

    @classmethod
    def get_mongo_client(cls, uri, db_name, col_name):
        """
            Get mongo client
        """
        client = pymongo.MongoClient(uri, connect=False)
        db = client.get_database(db_name)
        return db.get_collection(col_name)
