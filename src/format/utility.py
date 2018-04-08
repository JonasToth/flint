#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions that are necessary for formatting.
"""


def overwrite_lines(overwritee: list, overwriter: list, start: int, end: int):
    # Overwrite for formatting.
    for new_line_idx, old_line_idx in enumerate(range(start, end)):
        overwritee[old_line_idx] = overwriter[new_line_idx]
