#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Install
*******

This is a program installer module. It can be used to install a program on a
Linux system and prepare the Linux environment for this program to run
properly. This script also requires a Linux environment.

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
PROJECT = 'legcocar'
run_cmd_vars['PROJECT'] = PROJECT

# Install script location
run_cmd_vars['DIR'] = os.path.dirname(os.path.realpath(sys.argv[0]))

# Install script name
run_cmd_vars['SCRIPT'] = os.path.basename(__file__)


# noinspection PyShadowingNames,PyUnboundLocalVariable
def edit_line(file_name: str, regex: str, replace: str, mode: str = 'status',
              show_ok: bool = False):
    """
    Edit line in file matching a regular expression.

    :param file_name: Full path and name of file to write content to.
    :param regex:     Regular expression for matching line to edit.
    :param replace:   Replace line with this. Matching groups from regex are
                      matched with {1}...{10}
    :param mode:      Choices are: "status", "regular" and "quiet":
                      "status":  Print command and status.
                      "regular": Print command, stdout and stderr to screen
                                 (just as usual).
                      "verbose": Print status, command, stdout and stderr to
                                 screen.
                      "quiet":   Only print errors.
    :param show_ok:   If ok status should be shown.

    """
    error = ''
    # Insert values from run_cmd_vars in "regex" and "replace"
    # (if they exist)
    for key, val in run_cmd_vars.items():
        var = '{' + key + '}'
        if var in regex:
            regex = regex.replace(var, val)
        if var in replace:
            replace = replace.replace(var, val)

    # Set OK status message
    status_string = 'Replaced "{old}" with "{replace}" in file "{file_name}"'
    status_string = status_string.replace('{replace}', replace)
    status_string = status_string.replace('{file_name}', file_name)

    # Read file
    try:
        file = open(file_name, 'r', encoding='utf-8')
        line_list = file.readlines()
        line_list = [i.strip('\n') for i in line_list]
        file.close()
    except BaseException as e:
        status_string = 'Error editing file "{file_name}"'
        status_string = status_string.format(file_name=file_name)
        error = str(e)

    # Edit line in file
    if error == '':
        for i in range(len(line_list)):
            match = re.match(pattern=regex, string=line_list[i])

            # Replace line in memory
            if match is not None:
                # Insert matching groups in replace (if any)
                for n in range(1, 11):
                    group_string = '{' + str(n) + '}'
                    if group_string in replace:
                        replace = replace.replace(group_string, match.group(n))
                # Complete status string
                status_string = status_string.format(old=line_list[i])
                # Replace line in memory
                line_list[i] = replace
                break

        # Not finding a match is an error so we set error status
        if match is None:
            status_string = 'No match was found for "{regex}" in "{file_name}"'
            status_string = status_string.format(regex=regex,
                                                 file_name=file_name)
            error = None

    # Write file
    if error == '':
        try:
            tmp_file_name = file_name + '~'
            file = open(tmp_file_name, 'w', encoding='utf-8')
            file.writelines('\n'.join(line_list))
            file.close()
            os.rename(tmp_file_name, file_name)
        except BaseException as e:
            status_string = 'Error editing file "{file_name}"'
            status_string = status_string.format(file_name=file_name)
            error = str(e)

    # Print quiet mode
    if mode == 'quiet' and error != '':
        status = '[ \033[1;91mERROR\033[0m ] '
        status_string = status + status_string
        print(status_string, flush=True)
        if error is not None:
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
        if error != '' and error is not None:
            print(error, flush=True)
        elif mode == 'verbose':
            print(content, flush=True)


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
edit_line.__defaults__ = (None, None, None, mode, show_ok)

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

# List of packages to install with apt
APT_PACKAGE_LIST = [
    'python3=3.7.3-1', 'openssl=1.1.1c-1', 'build-essential=12.6',
    'tk-dev=8.6.9+1', 'libncurses5-dev=6.1+20181013-2+deb10u2',
    'libncursesw5-dev=6.1+20181013-2+deb10u2', 'libreadline-dev=7.0-5',
    'libgdbm-dev=1.18.1-4', 'libsqlite3-dev=3.27.2-3',
    'libssl-dev=1.1.1d-0+deb10u2', 'libbz2-dev=1.0.6-9.2~deb10u1',
    'libexpat1-dev=2.2.6-2+deb10u1', 'liblzma-dev=5.2.4-1',
    'zlib1g-dev=1:1.2.11.dfsg-1', 'libffi-dev=3.2.1-9', 'uuid-dev=2.33.1-0.1',
    'python3-pip=18.1-5+rpt1', 'apache2=2.4.38-3+deb10u3',
    'libapache2-mod-wsgi-py3=4.6.5-1', 'rabbitmq-server=3.7.8-4',
    'supervisor=3.3.5-1']

# List of packages to install with pip3
PIP3_PACKAGE_LIST = [
    'bricknil==0.9.3', 'flask==1.1.1', 'pika==1.1.0', 'bricknil-bleak==0.3.1',
    'coloredlogs==10.0', 'verboselogs==1.7']

# Create supervisor log dir
run_cmd('mkdir -p /var/log/supervisor')

# Set bash_aliases for root
run_cmd('''sed -i "/alias ls='ls -lah --color=auto'/d" /root/.bashrc''',
        mode='quiet')
run_cmd('''echo "alias ls='ls -lah --color=auto'" >> /root/.bashrc''')

# Install packages with apt
if not skip:
    run_cmd('apt-get update')
    for package in APT_PACKAGE_LIST:
        run_cmd('apt-get -y install {package}'.format(package=package))

# Install packages with pip3
if not skip:
    for package in PIP3_PACKAGE_LIST:
        run_cmd('pip3 install {package}'.format(package=package))

# Create project user
if not skip:
    run_cmd('useradd -m {PROJECT}')

# Create directories, move files, and set permissions
run_cmd('rm -Rf /srv/flask_wsgi', mode='quiet')
run_cmd('rm -Rf /srv/{PROJECT}', mode='quiet')
run_cmd('mkdir /srv/flask_wsgi')
run_cmd('mkdir /srv/{PROJECT}')
run_cmd('mkdir -p /var/log/{PROJECT}')
run_cmd('chown -R {PROJECT}:{PROJECT} /var/log/{PROJECT}')
run_cmd('chmod 755 /var/log/{PROJECT}')
run_cmd('cp {DIR}/other/legcocar_template.conf /srv/{PROJECT}/')
run_cmd('cp -R {DIR}/html_static /srv/{PROJECT}/')
run_cmd('cp -R {DIR}/html_templates /srv/{PROJECT}/')
run_cmd('cp {DIR}/src/flaskserver.py /srv/{PROJECT}/')
run_cmd('cp {DIR}/src/wsgi.py /srv/flask_wsgi/')
run_cmd('cp {DIR}/other/000-default.conf /etc/apache2/sites-available/')
run_cmd('chown -R {PROJECT}:{PROJECT} /srv/flask_wsgi')
run_cmd('chmod 755 /srv/flask_wsgi')
run_cmd('chown -R {PROJECT}:{PROJECT} /srv/{PROJECT}')
run_cmd('chmod 755 /srv/{PROJECT}')

# Restart apache2 for settings to take affect
run_cmd('service apache2 restart')

# Create rabbitMQ .erlang.cookie
if not skip:
    run_cmd_vars['ERLANG_COOKIE'] = 'HEIQLGKPYPKGHVQFRPRF'
    run_cmd('echo -n {ERLANG_COOKIE} > /var/lib/rabbitmq/.erlang.cookie')
    run_cmd('chown rabbitmq.rabbitmq /var/lib/rabbitmq/.erlang.cookie')
    run_cmd('chmod 400 /var/lib/rabbitmq/.erlang.cookie')

# /etc/rabbitmq/enabled_plugins
if not skip:
    run_cmd(
        '''echo '[rabbitmq_management].' > /etc/rabbitmq/enabled_plugins''')
    run_cmd('chown rabbitmq.rabbitmq /etc/rabbitmq/enabled_plugins')

# Create RabbitMQ project user
if not skip:
    run_cmd('rabbitmqctl add_user {PROJECT} {PROJECT}')
    run_cmd('rabbitmqctl set_user_tags {PROJECT} administrator')

# Restart RabbitMQ server
if not skip:
    run_cmd('service rabbitmq-server restart')
