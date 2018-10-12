#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# logger.py
# @Author : PengYingzhi
# @Date   : 10/9/2018, 2:24:38 PM

import logging


def get_stream_logger(name):
    """
    Return a stream a logger

    Params:
        * name:           (string) - log's name
        * level:          (int)    - log's level

    Returns:
        * logger:         (Logger) - Logger instance
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formater = logging.Formatter(
        '[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    handler.setFormatter(formater)
    logger.addHandler(handler)
    return logger


class LoggerManager(object):

    loggers = {}

    @classmethod
    def get_logger(cls, name):
        """
            Return a logger instance
        """
        if name not in cls.loggers:
            cls.loggers[name] = get_stream_logger(name)
        return cls.loggers[name]

    @classmethod
    def add_logger(cls, name, logger):
        """
            Add a logger to loggers
        """
        cls.loggers[name] = logger


class FormatFactory(object):
    """
        A Factory of getting logger's format.
    """
    class Options:
        normal = 'normal'
        just_message = 'just_message'

    @classmethod
    def get_format(cls, format='normal'):
        """
            Get format according to `FormatFactory.Options`
        """
        if format == cls.Options.just_message:
            return '%(message)s'
        else:
            return '[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s'


class FileLoggerFactory(object):
    """
        A Factory of creating the `FileHandler` logger
    """

    @classmethod
    def get_rotating_file_logger(cls,
                                 name,
                                 filename,
                                 max_bytes=1024*20,
                                 backup_count=50,
                                 format=FormatFactory.Options.normal):
        logger = logging.getLogger(name)
        handler = logging.handlers.RotatingFileHandler(
            filename, maxBytes=max_bytes, backupCount=backup_count)
        formater = logging.Formatter(format)
        handler.setFormatter(formater)
        logger.addHandler(handler)
        return logger
