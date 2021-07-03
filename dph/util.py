#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import reduce
import operator


__all__ = [ 'product' ]


def product(*args):
    return reduce(operator.mul, args)
