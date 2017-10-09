# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Debug
*****

This module handles debug logging.

"""


class Debug:
    """Helper class for debug logging. """

    ACTIVE_DEBUG_GROUPS = []
    """(*List*) Active debug groups."""

    __LEVEL_COLOR = {
        1: "\033[0;30;41m", 2: "\033[0;30;42m", 3: "\033[0;30;43m",
        4: "\033[0;30;44m", 5: "\033[0;30;45m", 6: "\033[0;30;46m",
        7: "\033[0;30;41m", 8: "\033[0;30;41m", 9: "\033[0;30;42m",
        10: "\033[0;30;43m"}
    """(*dict*) Debug level color."""

    DEBUG_DATA = {
        'test1': {
            'groups': ['test'],
            'message': "{0}"
        }
    }
    """(*dict*) Container for all debug messages."""

    # noinspection PyShadowingBuiltins
    @staticmethod
    def debug_status(id):
        """
        Get the current status for a specified debug id.

        :param any id: Target status debug id.
        :rtype:   bool
        :returns: Current status if the debug id.

        """
        id_groups = Debug.DEBUG_DATA[id]['groups']
        current_groups = [
            i for i in id_groups if i in Debug.ACTIVE_DEBUG_GROUPS]
        if len(current_groups) >= 1 or 'all' in Debug.ACTIVE_DEBUG_GROUPS:
            return True
        return False

    # noinspection PyShadowingBuiltins
    def debug_print(self, id, args=list()):
        """
        Print debug message.

        :param any id:           Id of the debug message.
        :param list args:        Arguments for the debug message.

        """
        if not isinstance(args, list):
            raise DebugArgumentTypeError(arg_name='args',
                                         arg_value=args,
                                         arg_type='list')
        if Debug.debug_status(id):
            color = 1
            if 'color' in self.DEBUG_DATA[id]:
                color = self.DEBUG_DATA[id]['color']
            start = self.__LEVEL_COLOR[color]
            end = "\033[0m"
            message = (self.DEBUG_DATA[id]['message']).format(*args)
            message = "{}{}{}".format(start, message, end)
            print()
            print(message)
            print()


class DebugError(Exception):
    """Error for debug handling."""


class DebugArgumentTypeError(DebugError):
    """Error for debug handling."""

    def __init__(self, arg_name, arg_value, arg_type):
        """
        Constructor function.

        :param str arg_name:  Target argument name.
        :param any arg_value: Target argument value.
        :param str arg_type:  Target argument wanted type.

        """
        message = ("Argument '{}' with value '{}' has invalid type '{}', type "
                   "must be '{}'!")
        self._message = message.format(arg_name,
                                       arg_value,
                                       str(type(arg_value)),
                                       arg_type)

    def __str__(self):
        """
        String representation function.
        """
        return self._message
