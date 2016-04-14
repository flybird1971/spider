#!/usr/bin/env python
# coding:utf-8

import datetime
import logging
from config import debug_on


def info(infos, isPrint=False):

    if not debug_on:
        return None

    if isPrint:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print date + infos
    else:
        logging.info(infos)

__all__ = ['info']
