#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Command line script.
********************

This is a template for writing a script that accepts command line arguments.

"""

# Built in modules
import argparse

# Third party modules
# TODO import modules here

# Local modules
# TODO import modules here


class Main:
    """Contains the script"""

    @staticmethod
    def _parse_command_line_options():
        """
        Parse options from the command line.

        :rtype: Namespace
        :returns: Command line arguments.

        """
        debug_help = 'Enter help text for parameter debug here.'  # TODO
        description = 'Short Description of what the script does.'  # TODO
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--debug', type=int, default="",
                            help=debug_help, required=False)
        args = parser.parse_args()
        return args

    # noinspection PySimplifyBooleanCheck
    def run(self):
        """
        Run the script.
        """
        args = self._parse_command_line_options()
        print(args.debug)  # TODO delete
        # TODO enter code here

if __name__ == '__main__':
    main = Main()
    main.run()
