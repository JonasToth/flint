#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implement a formatter that aligns trailing comments in subsequent
line. The line sequence end with an empty or non-comment line.

Example:

```fortran
integer(8) :: some_int ! asdlkja
real(8) :: some_real       ! alskdj
  ! continue the comment

! not in sequence
```
becomes
```fortran
integer(8) :: some_int     ! asdlkja
real(8) :: some_real       ! alskdj
                           ! continue the comment

! not in sequence
```
"""

import logging
import re
from common_matcher import match_line, match_blank_line, match_commented_line
from common_matcher import match_ignore_start, match_ignore_end
from file_io import CodeFile
from format.abstract_formatter import AbstractFormatter
from format.align import insert_whitespace, find_anchor
from format.utility import overwrite_lines

REGEX_TRAILING_COMMENT = re.compile(r'^(.*)([^\\]|\s+)!(.*)$')
REGEX_EXCLAMATION_IN_STRING = re.compile(r'^.*((".*!.*")|(\'.*!.*\')).*$')
REGEX_OMP_DIRECTIVE = re.compile(r'^!\$OMP(.*)$')


def _match_trailing_comment(line):
    """
    Match if a line contains a comment, but not only whitespace
    if front of the comment.
    """
    res = not match_commented_line(line) and \
          match_line(REGEX_TRAILING_COMMENT, line)
    return res


def _match_omp_directive(line):
    """
    Match if a comment is a OMP directive.
    Use this function to filter the alignments.
    """
    return match_line(REGEX_OMP_DIRECTIVE, line)


def _align_comments(lines: list):
    """
    Algorithm to align the trailing comments of ssubsequent lines is same
    as for `_align_colons`.
    Ignore OMP directives while aligning
    """
    if len(lines) == 0:
        return []

    comment_posi = find_anchor(
        lines,
        "!",
        skip_func=_match_omp_directive)
    (max_comment, max_line) = max((v, i) for i, v in enumerate(comment_posi))

    formatted_lines = []

    for i, line in enumerate(lines):
        if not _match_omp_directive(line):
            line = insert_whitespace(line, comment_posi[i], max_comment)
        formatted_lines.append(line)

    return formatted_lines


class FormatAlignTrailingComment(AbstractFormatter):
    """
    Example:

    ```fortran
    integer(8) :: some_int ! asdlkja
    real(8) :: some_real       ! alskdj
      ! continue the comment

    ! not in sequence
    ```
    becomes
    ```fortran
    integer(8) :: some_int     ! asdlkja
    real(8)    :: some_real    ! alskdj
                               ! continue the comment

    ! not in sequence
    ```

    Limitation:
    The formatting will fail if the line contains a string containing a '!'
    and a trailing comment. This might result in a mess but should be uncommon.
    """

    def __init__(self, f_file: CodeFile):
        super(FormatAlignTrailingComment, self).__init__(f_file)
        self._log = logging.getLogger(__file__ + "::align_trailing_comment")

    @classmethod
    def help(self):
        return "Align subsequent trailing comments. End with blank or non-comment line"

    def format(self):
        in_sequence = False
        in_ignore = False
        seq_start = -1
        seq_end = -1

        for (i, line) in enumerate(self._formatted_lines):
            if match_ignore_start(line):
                in_ignore = True

                in_sequence = False
                seq_start = -1
                seq_end = -1
                continue

            if in_ignore:
                if match_ignore_end(line):
                    in_ignore = False
                continue

            # Start a sequence if there is a trailing comment.
            if not in_sequence and _match_trailing_comment(line):
                self._log.debug("starting sequence at %d" % i)
                seq_start = i
                seq_end = i + 1
                in_sequence = True
                continue

            # Advance sequence for a following trailing comment.
            elif in_sequence and _match_trailing_comment(line):
                self._log.debug("advancing sequence to %d" % (i + 1))
                seq_end = i + 1
                continue

            # Maybe there is a continuation comment, align that, too.
            elif in_sequence and match_commented_line(line):
                self._log.debug("advancing sequence to %d" % (i + 1))
                seq_end = i + 1
                continue

            # End the sequence for every other line.
            elif in_sequence:
                self._log.debug("ending sequence at %d" % i)
                assert seq_start > 0
                assert seq_end > 0
                # Align all trailing comments
                new = _align_comments(self._formatted_lines[seq_start:seq_end])

                overwrite_lines(self._formatted_lines, new, seq_start, seq_end)

                # End sequence
                in_sequence = False
                seq_start = -1
                seq_end = -1
                continue

            # Ignore the rest of possible lines
            continue

        if in_ignore:
            self._log.warn("Missing end of ignore sequence!")

        return self.formatted_lines()
