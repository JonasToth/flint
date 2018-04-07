#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define functions that will read in fortran files and can output them again.
This will overwrite the original file if necessary.
"""

import os


class CodeFile(object):
    """
    Represent a fortran file, handle IO and give an interface for
    FIXITs.
    """

    def __init__(self, file_path):
        """
        Initialize the code file.

        :file_path: Path of the fortran file.
                    If the path is relative, the prefix of the execution directory
                    is added.
        """
        self._file_path = os.path.abspath(file_path)

    def path(self):
        """Return the absolute path of the `CodeFile`."""
        return self._file_path
