#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define the abstract interface of formatters.
"""

import abc
from file_io import CodeFile


class AbstractFormatter(object):
    """
    Abstract class as interface for all formatters.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, f_file: CodeFile):
        self._f_file = f_file
        self._formatted_lines = []

    @classmethod
    def help(self):
        pass

    @abc.abstractmethod
    def format(self):
        pass

    def formatted_lines(self):
        return self._formatted_lines
        
