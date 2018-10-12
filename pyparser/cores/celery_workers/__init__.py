#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# __init__.py
# @Author : PengYingzhi
# @Date   : 9/27/2018, 9:33:04 AM


from celery import Celery

from .celeryconfig import CELERY_CONFIG


app = Celery()
app.conf.update(CELERY_CONFIG)
