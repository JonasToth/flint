#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define functions that will read in fortran files and can output them again.
This will overwrite the original file if necessary.
"""

import logging as log
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
        If the path is relative, the prefix of the execution
        directory is added.
        """
        self._log = log.getLogger(__file__)

        self._log.debug("Set _file_path to %s" % os.path.abspath(file_path))
        self._file_path = os.path.abspath(file_path)

        # List of strings the file consists of. Read in lazyly.
        # Both the original version and the case insenstive version.
        self._original_file_content = None
        self._insensitive_file_content = None

    def path(self):
        """Return the absolute path of the `CodeFile`."""
        return self._file_path

    def original_lines(self):
        """
        Return the original content as list of lines.
        :note: Use `insensitive_lines` for analysis.
        :note: The lines do include the \\n character.
        """
        if self._original_file_content is None:
            self.__read_file()
        return self._original_file_content

    def insensitive_lines(self):
        """
        Return a list of lines that are not case sensitive and better to
        work with while analyzing.
        The lines do include the \\n character.
        """
        if self._insensitive_file_content is None:
            self.__read_file()
        return self._insensitive_file_content

    def update_lines(self, lines):
        """Remove all current lines and overwrite them with `lines`."""
        self.__assign_lines(lines)

    def write(self):
        """
        Write the content of `_original_file_content` into the original file.
        """
        with open(self._file_path, 'w') as fortran_file:
            fortran_file.writelines(self._original_file_content)

    def __read_file(self):
        """Read the file content into memory."""
        assert self._original_file_content is None, "Already read file"
        assert self._insensitive_file_content is None, "Already read file"
        self._log.debug("Reading the content of the file %s" % self._file_path)

        with open(self._file_path) as fortran_file:
            self.__assign_lines(fortran_file)

    def __assign_lines(self, iteratable):
        """Assign every line in `iterabtable` to the content."""
        self._original_file_content = []
        self._insensitive_file_content = []

        for line in iteratable:
            self._log.debug("assigning: %s" % line)
            self._original_file_content.append(line)
            self._insensitive_file_content.append(line.lower())
