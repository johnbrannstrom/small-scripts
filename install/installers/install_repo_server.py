#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Install repository server
*************************

This script will configure a CentOS 8 server as a:
* Dnf repository mirror/server.
* pip repository server.

"""

# Built in modules
import subprocess
import argparse
import os
import sys
import re

# Adding variables and values in this dictionary will enable them to be
# substituted into run_cmd commands
run_cmd_vars = dict()

# Name of project
PROJECT = 'dnf_repo'
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
    :rtype:   str
    :returns: Target command stdout

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
        stdout = ''
        with subprocess.Popen(command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              bufsize=1,
                              shell=True,
                              universal_newlines=True) as p:
            for line in p.stdout:
                stdout += line
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

        # Return stdout
        return stdout

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

        # Return stdout
        return result.stdout.decode('utf-8')

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

        # Return stdout
        return result.stdout.decode('utf-8')


# Parse command line arguments
# noinspection PyShadowingNames
def parse_command_line_options():
    """
    Parse options from the command line.

    :rtype: Namespace

    """
    force_first_help = (
        'Supplying this will run the script as if it was the first time.')
    skip_help = (
        'Supplying this flag will skip as many time consuming steps as '
        'possible to speed up the installation process. This is used for '
        'development purposes only.')
    show_ok_help = 'Supplying this flag will show actions with ok status.'
    verbose_help = 'Supplying this flag will enable all possible output.'
    remote_help = 'Install program on remote user@host.'
    description = 'Installer script for the {PROJECT}.'.format(PROJECT=PROJECT)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-f', '--force-first', default=False,
                        action='store_true', help=force_first_help,
                        required=False)
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
force_first = args.force_first

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
    run_cmd("echo 'put -r {DIR}/*' > /tmp/{PROJECT}_sftp_batchfile", mode='quiet')
    run_cmd("sftp -b /tmp/{PROJECT}_sftp_batchfile {REMOTE}:/tmp/{PROJECT}",
            mode='regular')
    run_cmd("rm /tmp/{PROJECT}_sftp_batchfile", mode='quiet')

    # Run install script on remote side
    opts = ''
    command = "ssh {REMOTE} '/tmp/{PROJECT}/{SCRIPT}{opts}'"
    if skip:
        opts += ' -s'
    if show_ok:
        opts += ' -o'
    if verbose:
        opts += ' -v'
    if force_first:
        opts += ' -f'
    command = command.replace('{opts}', opts)
    run_cmd(command, mode='regular')
    sys.exit(0)

# Set if we are running the script for the first time
command = "if [ -f '/var/tmp/{PROJECT}_once' ]; then echo 'true'; fi"
first = run_cmd(command, mode='quiet') == 'true'
if not first:
    run_cmd('touch /var/tmp/{PROJECT}_once', mode='quiet')
if force_first:
    first = True

# Add program specific content below this line

# List of packages to install with dnf
DNF_PACKAGE_LIST = ['httpd', 'python3-pip', 'createrepo', 'yum-utils', 'nano',
                    'mod_ssl', 'createrepo']

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
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ '
            '--repo=BaseOS --download-metadata')
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ '
            '--repo=AppStream --download-metadata')
    run_cmd('reposync -p /var/www/repos/centos/8/x86_64/os/ '
            '--repo=extras --download-metadata')

# Add copy task to daily jobs
content = """#!/bin/bash

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

# Create custom limited repo
run_cmd('rm -Rf /var/www/repos/centos/8/x86_64/os/limited')
run_cmd('mkdir -p /var/www/repos/centos/8/x86_64/os/limited/Packages')
run_cmd('touch /var/www/repos/centos/8/x86_64/os/limited/mirrorlist')
# Add packages to repo
run_cmd('ln /var/www/repos/centos/8/x86_64/os/BaseOS/Packages/nano-2.9.8-1.el8.x86_64.rpm '
        '/var/www/repos/centos/8/x86_64/os/limited/Packages')
# Run create repository command
run_cmd('createrepo /var/www/repos/centos/8/x86_64/os/limited')

# Create custom limited pip3 repo
run_cmd('mkdir -p /var/www/repos/pip3')
content = """<VirtualHost *:80>
    ServerName pgcentos1.local

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
</VirtualHost>

<VirtualHost *:443>
    ServerName pypi.pgcentos1.local
    DocumentRoot /var/www/repos/pip3

    SSLEngine On
    SSLCertificateFile /etc/pki/tls/certs/dnf.crt
    SSLCertificateKeyFile /etc/pki/tls/private/dnf.key

    <Directory /var/www/repos/pip3/>
        AllowOverride None
        Options +Indexes
        IndexOptions SuppressColumnSorting
        IndexIgnore ..
        Order deny,allow
        Allow from all

        AuthType Basic
        AuthName "My Server"
        AuthBasicProvider file
        AuthUserFile /etc/httpd/passwords_pypi
        Require valid-user
    </Directory>

    LogLevel warn
    ErrorLog /var/log/httpd/pypi3-error.log
    CustomLog /var/log/httpd/pypi3-access.log combined
</VirtualHost>
"""
write_file('/etc/httpd/conf.d/pypi3.conf', content)


# Configure Apache httpd to provide repository for other Client Hosts
content = """Alias /repos /var/www/repos
<directory /var/www/repos>
    Options +Indexes
    Require all granted
</directory>"""
write_file('/etc/httpd/conf.d/repos.conf', content)
edit_line(file_name='/etc/httpd/conf.d/ssl.conf',
          regex='SSLCertificateFile +.*',
          replace='SSLCertificateFile /etc/pki/tls/certs/dnf.crt')
edit_line(file_name='/etc/httpd/conf.d/ssl.conf',
          regex='SSLCertificateKeyFile +.*',
          replace='SSLCertificateKeyFile /etc/pki/tls/private/dnf.key')
run_cmd('systemctl enable httpd')

# Disable password authentication
edit_line(file_name='/etc/ssh/sshd_config',
          regex='PasswordAuthentication +[a-zA-Z0-1]+.*',
          replace='PasswordAuthentication no')
run_cmd('systemctl restart sshd')

# Allow HTTPS service in firewall
run_cmd('firewall-cmd --add-service=https --permanent')
run_cmd('firewall-cmd --reload')

# Create key and certificate and then copy both to client
if first:
    run_cmd('openssl genrsa -out /etc/pki/tls/private/dnf.key 2048')
    run_cmd('openssl req -days 3650 -x509 -new -nodes '
            '-key /etc/pki/tls/private/dnf.key -sha256 '
            '-out /etc/pki/tls/certs/dnf.crt '
            '-subj "/C=SE/ST=Östergötland/L=Norrköping/CN=pgcentos1.local"')
    run_cmd('update-ca-trust extract')
    run_cmd('scp /etc/pki/tls/private/dnf.key root@pgcentos2:/var/lib/dnf/client.key')
    run_cmd('scp /etc/pki/tls/certs/dnf.crt root@pgcentos2:/var/lib/dnf/client.crt')

# Activate apache changes
run_cmd('systemctl reload httpd')
run_cmd('systemctl restart httpd')

# Manual commands
if first:
    print('Run these commands manually:')
    print('htpasswd -c /etc/httpd/passwords_pypi pypi')
