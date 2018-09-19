#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_redis_monitor.py
# @Author : PengYingzhi
# @Date   : 9/19/2018, 10:59:32 AM


from pyparser.cores.redis_monitor import ItemRedisMonitorManager


def main():
    """
        main
    """
    ir_monitor_manager = ItemRedisMonitorManager()
    ir_monitor_manager.run()


if __name__ == '__main__':
    main()
