#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implement functions that are usable to emit warnings.
"""

import sys
import file_io


def error(ffile: file_io.CodeFile, line: int, message: str):
    """Emit a warning for this file at a line.

    :ffile: file_io.CodeFile: Fortran File to emit the warning
    :line: int: line number of the warned construct
    :message: str: human readable warning message
    """
    _check_location(ffile, line)
    print(_create_message(ffile, line, "error", message), file=sys.stderr)


def warning(ffile: file_io.CodeFile, line: int, message: str):
    """Emit a warning for this file at a line.

    :ffile: file_io.CodeFile: Fortran File to emit the warning
    :line: int: line number of the warned construct
    :message: str: human readable warning message
    """
    _check_location(ffile, line)
    print(_create_message(ffile, line, "warning", message), file=sys.stderr)


def note(ffile: file_io.CodeFile, line: int, message: str):
    """Emit a warning for this file at a line.

    :ffile: file_io.CodeFile: Fortran File to emit the warning
    :line: int: line number of the warned construct
    :message: str: human readable warning message
    """
    _check_location(ffile, line)
    print(_create_message(ffile, line, "note", message), file=sys.stderr)


def _create_message(ffile: file_io.CodeFile, line: int, category: str,
                    message: str):
    return "{}: {}: {}: {}".format(ffile.path(), line, category, message)


def _check_location(ffile: file_io.CodeFile, line: int):
    assert line > 0, "Trying to emit a diagnostic for a negative line number"
    assert line < len(ffile.original_lines()), "To big line number"
