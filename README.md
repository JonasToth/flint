[![Build Status](https://travis-ci.org/JonasToth/flint.svg?branch=master)](https://travis-ci.org/JonasToth/flint)

# Toyproject to do some linting in our fortran code

This tool aims to do code transformations and create warnings.
It is python based to be very usable and not production ready.

**IT CAN NOT BE TRUSTED!**

## Features

### Static Analysis

- warn for missing `implicit none`

### Formatting

- format variable declarations to align `::`

## Other interesting tools

- [fortran-syntax](https://github.com/cphyc/fortran-syntax)
- [fprettify](https://github.com/pseewald/fprettify)


## Notes

The formatting capabilities are not very advanced, but complement `fprettify`.

Use `fprettify` for most of the formatting and use `flint` afterwards for
specific issues.
