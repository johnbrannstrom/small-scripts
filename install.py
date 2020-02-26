#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: John Brännström <john.brannstrom@gmail.com>

Install
*******

This is a program installer module. It can be used to install a program on a
Linux system and prepare the Linux environment for this program to run
properly.

"""

# Built in modules
import subprocess

PROJECT = 'legcocar'
"""(*str*) Name of project"""

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
    'supervisor=3.3.5-1', 'coloredlogs==10.0', 'verboselogs==1.7']
""""(*list*) List of packages to install with apt"""


PIP3_PACKAGE_LIST = [
    'bricknil==0.9.3', 'flask==1.1.1', 'pika==1.1.0', 'bricknil-bleak==0.3.1']
"""(*list*) List of packages to install with pip3"""


# Current location compared to script location
command = 'dirname "$(readlink -f "$0")"'
DIR = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     shell=True)


def run_cmd(command: str, quiet: bool = False):
    """
    Run a command and print status.

    :param command: Command to run.
    :param quiet: Setting this to false will print command and status.

    """
    # Insert PROJECT in command if it exists
    if '{PROJECT}' in command:
        command = command.format(PROJECT=PROJECT)

    # Insert DIR in command if it exists
    if '{DIR}' in command:
        command = command.format(DIR=DIR)

    # Run command
    stdout, stderr = subprocess.run(command, shell=True)

    # Print command and status
    status_string = " [ {status} ] {command}\n{stderr}"
    if stderr == '':
        status = '1;32m OK  \033[0m'
    else:
        status = '[1;91mERROR\033[0m'
    if not quiet:
        print(status_string.format(status=status,
                                   command=command,
                                   stderr=stderr))


# Add program specific content below this line


# Create supervisor log dir
run_cmd('mkdir -p /var/log/supervisor')

# Set bash_aliases for root
run_cmd('''sed -i "/alias ls='ls -lah --color=auto'/d" /root/.bashrc''',
        quiet=True)
run_cmd('''echo "alias ls='ls -lah --color=auto'" >> /root/.bashrc''')

# Install packages with apt
run_cmd('apt-get update')
for package in APT_PACKAGE_LIST:
    run_cmd('apt-get -y install {package}'.format(package=package))

# Install packages with pip3
for package in PIP3_PACKAGE_LIST:
    run_cmd('apt-get -y install {package}'.format(package=package))

# Create project user
run_cmd('useradd -m {PROJECT}')

# Create directories, move files, and set permissions
run_cmd('rm -Rf /srv/flask_wsgi', quiet=True)
run_cmd('rm -Rf /srv/{PROJECT}', quiet=True)
run_cmd('mkdir /srv/flask_wsgi')
run_cmd('mkdir /srv/{PROJECT}')
run_cmd('mkdir -p /var/log/{PROJECT}')
run_cmd('chown -R {PROJECT}:{PROJECT} /var/log/{PROJECT}')
run_cmd('chmod 755 /var/log/{PROJECT}')
run_cmd('mv {DIR}/other/legcocar_template.conf /srv/{PROJECT}/')
run_cmd('mv {DIR}/html_static /srv/{PROJECT}/')
run_cmd('mv {DIR}/html_templates /srv/{PROJECT}/')
run_cmd('mv {DIR}/src/flaskserver.py /srv/{PROJECT}/')
run_cmd('mv {DIR}/src/wsgi.py /srv/flask_wsgi/')
run_cmd('mv {DIR}/other/000-default.conf /etc/apache2/sites-available/')
run_cmd('chown -R {PROJECT}:{PROJECT} /srv/flask_wsgi')
run_cmd('chmod 755 /srv/flask_wsgi')
run_cmd('chown -R {PROJECT}:{PROJECT} /srv/{PROJECT}')
run_cmd('chmod 755 /srv/{PROJECT}')

# Restart apache2 for settings to take affect
run_cmd('service apache2 restart')

# Create rabbitMQ .erlang.cookie
erlang_cookie="HEIQLGKPYPKGHVQFRPRF"
command = 'echo -n {erlang_cookie} > /var/lib/rabbitmq/.erlang.cookie'
run_cmd(command.format(erlang_cookie=erlang_cookie))
run_cmd('chown rabbitmq.rabbitmq /var/lib/rabbitmq/.erlang.cookie')
run_cmd('chmod 400 /var/lib/rabbitmq/.erlang.cookie')

# /etc/rabbitmq/enabled_plugins
run_cmd('''echo '[rabbitmq_management].' > /etc/rabbitmq/enabled_plugins''')
run_cmd('chown rabbitmq.rabbitmq /etc/rabbitmq/enabled_plugins')

# Create RabbitMQ project user
run_cmd('rabbitmqctl add_user {PROJECT} {PROJECT}')
run_cmd('rabbitmqctl set_user_tags {PROJECT} administrator')
# TODO uncomment
# Restart RabbitMQ server
#run_cmd('service rabbitmq-server restart')
