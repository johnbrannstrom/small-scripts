# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

SimpleDebug
***********

This module prints debug messages to screen.

"""


class SimpleDebug:
    """
    Helper class for debug printing.

    """

    DEBUG_LEVEL = 0
    """(*int*) Current debug level."""

    __LEVEL_COLOR = {
        1: "\033[0;30;41m", 2: "\033[0;30;42m", 3: "\033[0;30;43m",
        4: "\033[0;30;44m", 5: "\033[0;30;45m", 6: "\033[0;30;46m",
        7: "\033[0;30;41m", 8: "\033[0;30;41m", 9: "\033[0;30;42m",
        10: "\033[0;30;43m"}
    """(*dict*) Debug level color."""

    # noinspection PyShadowingBuiltins
    def debug_print(self, level, message, module=None, class_=None,
                    function=None):
        """
        Print debug message to screen.

        :param int level:    Lowest debug level message will be printed in.
        :param str message:  Message to print.
        :param str module:   Module this debug printout is used in.
        :param str class_:   Class this debug printout is used in.
        :param str function: Function this debug printout is used in.

        """
        if self.DEBUG_LEVEL >= level:
            start = SimpleDebug.__LEVEL_COLOR[level]
            end = "\033[0m"
            print()
            print("{}Debug level: {}{}".format(start, level, end))
            if module is not None:
                print("{}Module: {}{}".format(start, module, end))
            if class_ is not None:
                print("{}Class: {}{}".format(start, class_, end))
            if function is not None:
                print("{}Function: {}{}".format(start, function, end))
            print("{}{}{}".format(start, message, end))
            print()
