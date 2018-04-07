#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define the abstract interface of all checks.
"""

import abc
from file_io import CodeFile


class AbstractCheck(object):
    """
    This abstract class defines the interface all static analysis checks
    must implement.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, f_file: CodeFile):
        self._f_file = f_file

    @abc.abstractmethod
    def help(self):
        pass

    @abc.abstractmethod
    def check(self):
        pass

    @abc.abstractmethod
    def report(self):
        pass
