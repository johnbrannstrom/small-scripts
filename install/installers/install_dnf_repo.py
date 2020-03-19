#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Install Dnf repository
**********************

This script will configure a CentOS 8 server as a Dnf repository mirror.

"""

# Built in modules
import subprocess
import argparse
import os
import sys


# Adding variables and values in this dictionary will enable them to be
# substituted into run_cmd commands
run_cmd_vars = dict()

# Name of project
PROJECT = 'yum'
run_cmd_vars['PROJECT'] = PROJECT

# Install script location
run_cmd_vars['DIR'] = os.path.dirname(os.path.realpath(sys.argv[0]))

# Install script name
run_cmd_vars['SCRIPT'] = os.path.basename(__file__)


# noinspection PyShadowingNames,PyTypeChecker,PyUnboundLocalVariable
def run_cmd(command: str, mode: str = 'status'):
    """
    Run a command and print status.

    :param command: Command to run.
    :param mode:    Choices are: "status", "regular" and "quiet":
                    "status":  Print command and status.
                    "regular": Print command, stdout and stderr to screen (just
                               as usual).
                    "verbose": Print status, command, stdout and stderr to
                               screen.
                    "quiet":   Don't print anything.

    """
    # Insert values from run_cmd_vars if they exist
    for key, val in run_cmd_vars.items():
        var = '{' + key + '}'
        if var in command:
            command = command.replace(var, val)

    # Handle regular and verbose mode
    if mode.lower() == 'regular' or mode.lower() == 'verbose':
        print(command, flush=True)
        error = False
        with subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              bufsize=1,
                              shell=True,
                              universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='', flush=True)
            for line in p.stderr:
                error = True
                print(line, end='', flush=True)
        # Print status for verbose mode
        if mode.lower() == 'verbose':
            if error:
                status = '\033[1;91mERROR\033[0m'
            else:
                status = '\033[1;32m OK  \033[0m'

            # Print status
            status_string = "[ {status} ] {command}"
            status_string = status_string.format(status=status,
                                                 command=command)
            print(status_string, flush=True)

    # Handle status mode
    elif mode == 'status':
        result = subprocess.run(command, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            status = '\033[1;32m OK  \033[0m'
            stderr = ''
        else:
            status = '\033[1;91mERROR\033[0m'
            stderr = '\n' + result.stderr.decode('utf-8')

        # Print status
        status_string = "[ {status} ] {command}{stderr}"
        status_string = status_string.format(status=status,
                                             command=command,
                                             stderr=stderr)
        print(status_string, flush=True)

    # Handle quiet mode
    else:
        subprocess.run(command, shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Parse command line arguments
# noinspection PyShadowingNames
def parse_command_line_options():
    """
    Parse options from the command line.
    
    :rtype: Namespace

    """
    quick_help = (
        'Supplying this flag will skip as many time consuming steps as possibl'
        'e to speed up the installation process. This is used for development '
        'purposes only.')
    verbose_help = 'Supplying this flag will enable extra verbose output.'
    remote_help = 'Install program on remote user@host.'
    description = 'Installer script for the {PROJECT}.'.format(PROJECT=PROJECT)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-q', '--quick',  default=False, action='store_true',
                        help=quick_help, required=False)
    parser.add_argument('-v', '--verbose', default=False, action='store_true',
                        help=verbose_help, required=False)
    parser.add_argument('-r', '--remote', type=str, default="",
                        help=remote_help, required=False)
    args = parser.parse_args()
    return args


args = parse_command_line_options()
quick = args.quick
remote = args.remote
verbose = args.verbose

if verbose:
    run_cmd.__defaults__ = (None, 'verbose')

# Copy program and installer script to remote location and run it there instead
if remote != "":
    run_cmd_vars['REMOTE'] = remote
    run_cmd("ssh {REMOTE} 'mkdir -p /tmp/{PROJECT}'", mode='quiet')
    run_cmd("echo 'put -r {DIR}/*' > /tmp/sftp_batchfile", mode='quiet')
    run_cmd("sftp -b /tmp/sftp_batchfile {REMOTE}:/tmp/{PROJECT}",
            mode='regular')
    run_cmd("rm /tmp/sftp_batchfile", mode='quiet')

    # Run install script on remote side
    opts = ''
    command = "ssh {REMOTE} '/tmp/{PROJECT}/{SCRIPT}{opts}'"
    if quick:
        opts += ' -q'
    if verbose:
        opts += ' -v'
    command = command.replace('{opts}', opts)
    run_cmd(command, mode='regular')
    sys.exit(0)

# Add program specific content below this line

# List of packages to install with yum
YUM_PACKAGE_LIST = ['httpd', 'python3-pip', 'createrepo', 'yum-utils']

# List of packages to install with pip3
PIP3_PACKAGE_LIST = []

# Install packages with dnf
if not quick:
    run_cmd('dnf makecache')
    for package in YUM_PACKAGE_LIST:
        run_cmd('dnf -y install {package}'.format(package=package))

# Install packages with pip3
if not quick:
    for package in PIP3_PACKAGE_LIST:
        run_cmd('pip3 install {package}'.format(package=package))

# Create a Directory to Store the Repositories
run_cmd('mkdir --parents /var/www/repos/centos/8/x86_64/os')
run_cmd('chmod -R 755 /var/www/repos')

# Copy from official repository
if not quick:
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ --repo=BaseOS --download-metadata')
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ --repo=AppStream --download-metadata')
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ --repo=extras --download-metadata')
