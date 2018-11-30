#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# setup.py
# @Author : PengYingzhi
# @Date   : 11/29/2018, 5:43:26 PM

from setuptools import setup, find_packages


DESCRIPTION = 'A high-level data extraction, cleaning ' \
              'and validation framework to handle the ' \
              'data from web spiders.'

setup(
    name='pyparser',
    version='v0,1',
    author='Yzee',
    description=DESCRIPTION,
    maintainer='Yzee',
    maintainer_email='yzee_work@163.com',
    license='GPL',
    url='https://github.com/Beatles1314/PyParser',
    packages=find_packages('pyparser', exclude=('tests', 'tests.*')),
    include_package_data=True,  # read other files from MANIFEST.in
    python_requires='==3,6',
    install_requires=[
        'amqp>=2.3.2',
        'argh>=0.26.2',
        'billiard>=3.5.0.4',
        'celery>=4.2.1',
        'Click>=7.0',
        'kombu>=4.2.1',
        'pathtools>=0.1.2',
        'pkg-resources==0.0.0',
        'pymongo>=3.7.2',
        'pytz>=2018.7',
        'PyYAML>=3.13',
        'redis>=3.0.1',
        'simplejson>=3.16.0',
        'vine>=1.1.4',
        'watchdog>=0.9.0'
    ]
)
