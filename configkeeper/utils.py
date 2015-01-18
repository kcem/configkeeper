#!/usr/bin/env python

import inspect


def caller_module(caller_level=-2):
    # 0 - current stack
    # 1 - config_keeper stack
    # 2 - caller stack
    #
    # -1 - __main__ level
    # -2 - first package

    try:
        frm = inspect.stack()[caller_level]
        mod = inspect.getmodule(frm[0])
        return mod.__name__ if mod.__name__ != '__main__' else None

    except (IndexError, AttributeError):
        # AttributeError is raised when called from python command line
        # IndexError should not happend
        return None
