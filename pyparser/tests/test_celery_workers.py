#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_celery_workers.py
# @Author : PengYingzhi
# @Date   : 11/3/2018, 11:19:52 AM

import os
import sys
sys.path.insert(0, os.getcwd())

from datetime import datetime
import random as rd
import uuid

import click


@click.group()
def main():
    pass


@main.command()
def test_save_worker():
    """
        test_save_worker
    """
    pass


@main.command()
def test_parse_worker():
    """
        test_parse_worker
    """
    from faker import Factory
    from cores.celery_workers.parser import parse

    faker = Factory.create()
    content = ' '.join([faker.name() for _ in range(50)])
    parse.apply_async(
        kwargs={
            'app_id': 'test_01',
            'task_id': datetime.now().strftime('%Y-%m-%d'),
            'unikey': 'test_01',
            'url': 'https://www.google.com/',
            'content': content,
            'meta': {
                'from': 'from test_celery_workers'
            }
        }
    )


@main.command()
def test_validate_worker():
    """
        test_validate_worker
    """
    pass


if __name__ == '__main__':
    main()
