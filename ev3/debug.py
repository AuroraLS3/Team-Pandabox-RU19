#!/usr/bin/env python3

'''
Debug logging utility.

Example usage:

    from debug import debug

    debug("Message to print to VSCode console")
'''

import os
import sys

ON = True
OFF = False


def _reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def _set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def _set_font():
    os.system('setfont Lat15-Terminus24x12')


def prepare_console():
    _reset_console()
    _set_font()
    _set_cursor(OFF)


def debug(*args, **kwargs):
    '''
    Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

