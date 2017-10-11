#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Flask server
************

This modules is a template flask web server.

"""

# Built in modules
import argparse

# Third party modules
from flask import Flask
from flask import render_template


class RequestHandler:
    """Flask web server."""

    def handle_request(self):
        """
        Handle a HTTP request.

        """
        return render_template('index.html')


class Main:
    """Contains the script"""

    @staticmethod
    def _parse_command_line_options():
        """
        Parse options from the command line.

        :rtype: Namespace

        """
        debug_help = 'Debugging printout level.'
        description = 'Start flask web server.'
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('--debug', type=int, default=0,
                            help=debug_help, required=False)
        args = parser.parse_args()
        return args

    def run(self):
        """
        Run the script.

        """
        args = self._parse_command_line_options()
        flask_debug = False
        if args.debug > 0:
            flask_debug = True
        web_server.run(debug=flask_debug,
                       host='0.0.0.0',
                       port=80,
                       processes=3)


web_server = Flask(__name__,
                   static_url_path="",
                   static_folder='html_static',
                   template_folder='html_templates')


@web_server.route('/')
def index():
    """
    Handle incoming HTTP requests.

    """
    request_handler = RequestHandler()
    return request_handler.handle_request()


if __name__ == '__main__':
    main = Main()
    main.run()
