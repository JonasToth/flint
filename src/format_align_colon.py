#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implement a formatter, that aligns the double colon on subsequent lines.

Example:

```fortran
integer(8) :: some_int
real(8) :: some_real
```
becomes
```fortran
integer(8) :: some_int
real(8)    :: some_real
```
"""

import logging

from abstract_formatter import AbstractFormatter
from file_io import CodeFile


class FormatAlignColon(AbstractFormatter):

    """
    ```fortran
    integer(8) :: some_int
    real(8) :: some_real

    integer(8)   :: another_int
    ! asdojasdlkj 
    real(8)  :: and_another_one
    ```
    becomes
    ```fortran
    integer(8)   :: some_int
    real(8)      :: some_real
 
    integer(8)   :: another_int
    ! asdojasdlkj 
    real(8)      :: and_another_one
    ```
    Formatting will ignore blank lines and lines that start with a comment.
    """

    def __init__(self, f_file: CodeFile):
        AbstractFormatter.__init__(self, f_file)

    @classmethod
    def help(self):
        return "Align the double colons of subsequent variable definitions."
    

    def format(self):
        pass
