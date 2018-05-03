#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define the abstract interface of all checks.
"""

import abc
from file_io import FortranCode


class AbstractCheck(object):
    """
    This abstract class defines the interface all static analysis checks
    must implement.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, f_file: FortranCode):
        self._f_file = f_file

    @classmethod
    def help(self):
        pass

    @abc.abstractmethod
    def check(self):
        pass

    @abc.abstractmethod
    def report(self):
        pass
