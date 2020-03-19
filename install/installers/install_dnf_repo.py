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
PROJECT = 'dnf'
run_cmd_vars['PROJECT'] = PROJECT

# Install script location
run_cmd_vars['DIR'] = os.path.dirname(os.path.realpath(sys.argv[0]))

# Install script name
run_cmd_vars['SCRIPT'] = os.path.basename(__file__)


# noinspection PyShadowingNames
def write_file(file_name: str, content: str, mode: str = 'status',
               show_ok: bool = False, file_mode: str = 'w'):
    """
    Write content to file.

    :param file_name: Full path and name of file to write content to.
    :param content:   Content to write to file.
    :param mode:      Choices are: "status", "regular" and "quiet":
                      "status":  Print command and status.
                      "regular": Print command, stdout and stderr to screen
                                 (just as usual).
                      "verbose": Print status, command, stdout and stderr to
                                 screen.
                      "quiet":   Only print errors.
    :param show_ok:   If ok status should be shown.
    :param file_mode: Setting this to "w" till overwrite the file.
                      Setting this to "a" till append to the file.

    """
    # Insert values from run_cmd_vars in "file_name" and "content"
    # (if they exist)
    for key, val in run_cmd_vars.items():
        var = '{' + key + '}'
        if var in file_name:
            file_name = file_name.replace(var, val)
        if var in content:
            content = content.replace(var, val)

    # Write to file
    error = ''
    status_string = 'Wrote content to "{file_name}"'
    if file_mode == 'a':
        status_string = 'Appended content to "{file_name}"'
    status_string = status_string.format(file_name=file_name)
    try:
        file = open(file_name, file_mode)
        file.write(content)
        file.close()
    except BaseException as e:
        status_string = 'Error writing content to "{file_name}"'
        if file_mode == 'a':
            status_string = 'Error appending content to "{file_name}"'
        status_string = status_string.format(file_name=file_name)
        error = str(e)

    # Print quiet mode
    if mode == 'quiet' and error != '':
        status = '[ \033[1;91mERROR\033[0m ] '
        status_string = status + status_string
        print(status_string, flush=True)
        print(error, flush=True)

    # Print regular mode
    elif mode == 'regular' and (error != '' or show_ok):
        print(status_string, flush=True)

    # Print verbose and status mode
    elif (mode == 'verbose' or mode == 'status') and (error != '' or show_ok):
        status = '[ \033[1;32m OK  \033[0m ] '
        if error != '':
            status = '[ \033[1;91mERROR\033[0m ] '
        status_string = status + status_string
        print(status_string, flush=True)
        if error != '':
            print(error, flush=True)
        elif mode == 'verbose':
            print(content, flush=True)


# noinspection PyShadowingNames,PyTypeChecker,PyUnboundLocalVariable
def run_cmd(command: str, mode: str = 'status', show_ok: bool = False):
    """
    Run a command and print status.

    :param command: Command to run.
    :param mode:    Choices are: "status", "regular" and "quiet":
                    "status":  Print command and status.
                    "regular": Print command, stdout and stderr to screen (just
                               as usual).
                    "verbose": Print status, command, stdout and stderr to
                               screen.
                    "quiet":   Only print errors.
    :param show_ok: If ok status should be shown.

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
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.returncode == 0:
            status = '\033[1;32m OK  \033[0m'
            stderr = ''
        else:
            status = '\033[1;91mERROR\033[0m'
            stderr = '\n' + result.stderr.decode('utf-8')

        # Print status
        if stderr != '' or show_ok:
            status_string = "[ {status} ] {command}{stderr}"
            status_string = status_string.format(status=status,
                                                 command=command,
                                                 stderr=stderr)
            print(status_string, flush=True)

    # Handle quiet mode
    else:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # Print status if we had an error
        if result.returncode > 0:
            status = '\033[1;91mERROR\033[0m'
            stderr = '\n' + result.stderr.decode('utf-8')
            status_string = "[ {status} ] {command}{stderr}"
            status_string = status_string.format(status=status,
                                                 command=command,
                                                 stderr=stderr)
            print(status_string, flush=True)


# Parse command line arguments
# noinspection PyShadowingNames
def parse_command_line_options():
    """
    Parse options from the command line.
    
    :rtype: Namespace

    """
    skip_help = (
        'Supplying this flag will skip as many time consuming steps as possibl'
        'e to speed up the installation process. This is used for development '
        'purposes only.')
    show_ok_help = 'Supplying this flag will also actions with show ok status.'
    verbose_help = 'Supplying this flag will enable all possible output.'
    remote_help = 'Install program on remote user@host.'
    description = 'Installer script for the {PROJECT}.'.format(PROJECT=PROJECT)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', '--skip', default=False, action='store_true',
                        help=skip_help, required=False)
    parser.add_argument('-o', '--show-ok', default=False, action='store_true',
                        help=show_ok_help, required=False)
    parser.add_argument('-v', '--verbose', default=False, action='store_true',
                        help=verbose_help, required=False)
    parser.add_argument('-r', '--remote', type=str, default="",
                        help=remote_help, required=False)
    args = parser.parse_args()
    return args


args = parse_command_line_options()
skip = args.skip
show_ok = args.show_ok
remote = args.remote
verbose = args.verbose

# Set default values according to command line options
mode = 'status'
if verbose:
    mode = 'verbose'
run_cmd.__defaults__ = (None, mode, show_ok)
write_file.__defaults__ = (None, None, mode, show_ok, 'w')

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
    if skip:
        opts += ' -s'
    if show_ok:
        opts += ' -o'
    if verbose:
        opts += ' -v'
    command = command.replace('{opts}', opts)
    run_cmd(command, mode='regular')
    sys.exit(0)

# Add program specific content below this line

# List of packages to install with dnf
DNF_PACKAGE_LIST = ['httpd', 'python3-pip', 'createrepo', 'yum-utils']

# List of packages to install with pip3
PIP3_PACKAGE_LIST = []

# Install packages with dnf
if not skip:
    run_cmd('dnf makecache')
    for package in DNF_PACKAGE_LIST:
        run_cmd('dnf -y install {package}'.format(package=package))

# Install packages with pip3
if not skip:
    for package in PIP3_PACKAGE_LIST:
        run_cmd('pip3 install {package}'.format(package=package))

# Create a Directory to Store the Repositories
run_cmd('mkdir --parents /var/www/repos/centos/8/x86_64/os')
run_cmd('chmod -R 755 /var/www/repos')

# Copy from official repository
if not skip:
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ --repo=BaseOS --download-metadata')
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ --repo=AppStream --download-metadata')
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ --repo=extras --download-metadata')

# Add copy task to daily jobs
content = """# create new
#!/bin/bash

VER='8'
ARCH='x86_64'
REPOS=(BaseOS AppStream extras)

for REPO in ${REPOS[@]}
do
    reposync -p /var/www/repos/centos/${VER}/${ARCH}/os/ --repo=${REPO} --download-metadata --newest-only
done
"""
write_file('/etc/cron.daily/update-repo', content)
run_cmd('chmod 755 /etc/cron.daily/update-repo')

# Restart apache for changes to take effect
run_cmd('systemctl restart httpd')
