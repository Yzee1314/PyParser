#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# celeryconfig.py
# @Author: PengYingzhi
# @Date  : 9/27/2018, 9:33:38 AM


from kombu import (
    Exchange,
    Queue
)


CELERY_CONFIG = {
    'broker_url': 'amqp://localhost',

    # default
    'task_default_queue': 'default',
    'task_default_exchange': 'default',
    'task_default_routing_key': 'default',

    'imports': (
        'cores.celery_workers.save',
        'cores.celery_workers.parser'
    ),

    # queues
    'task_queues': {
        Queue(
            'default',
            Exchange('default', type=''),
            routing_key='default'
        ),
        Queue(
            'save',
            Exchange('save', type='topic'),
            routing_key='save.#'
        ),
        Queue(
            'parser',
            Exchange('parser', type='topic'),
            routing_key='parser.#'
        ),
    },

    # routes
    'task_routes': {
        'cores.celery_workers.save.save_to_local_file': {
            'queue': 'save',
            'routing_key': 'save.local_file'
        },
        'cores.celery_workers.parser.parse': {
            'queue': 'parser',
            'routing_key': 'parser.parser'
        }
    }
}
