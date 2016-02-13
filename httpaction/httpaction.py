#!/usr/bin/python3

import subprocess
from time import sleep
from flask import Flask
from flask import request

# The service will respond to requests on this port
tcpPort = 5000

# The service will respons to requests on this HTTP path
httpPath = '/'

# Sets if debug mode should be used
debug = True

# Path to the wakeonlan command
wakeonlanPath = '/usr/bin/'

# Path to the ping command
pingPath = '/bin/'

# Path to the ssh command
sshPath = '/usr/bin/'

httpaction = Flask(__name__)

@httpaction.route(httpPath)
def index():
    
    def poweron():
        if mac != None:
           if host != None:
               command = "{}wakeonlan -i {} {}".format(wakeonlanPath, host,  mac)
           else:
               command = "{}wakeonlan {}".format(wakeonlanPath, mac)
           for i in range(3):
               p = subprocess.Popen(
                   command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   shell=True)
               stdout, stderr = p.communicate()
               sleep(0.1)
           return stdout + stderr
        else:
            return "Action 'poweron' must have parameter 'mac'!"

    def poweroff():
        if user != None and host != None:
            command = "{}ssh -o StrictHostKeyChecking=no -T {}@{} 'shutdown -h now'".format(sshPath, user, host)
            p = subprocess.Popen(
                   command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   shell=True)
            stdout, stderr = p.communicate()
            return stdout + stderr
        elif user == None:
            return "Action 'poweroff' must have parameter 'user'!"
        elif host == None:
            return "Action 'poweroff' must have parameter 'host'!"
            
    def ping():
        if host != None:
            command = "ping -n 3 {}'".format(host)
            p = subprocess.Popen(
                   command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   shell=True)
            stdout, stderr = p.communicate()
            return stdout + stderr
        else:
            return "Action 'ping' must have parameter 'host'!"
            
    action = request.args.get('action')
    mac = request.args.get('mac')
    user = request.args.get('user')
    host = request.args.get('host')
    if action == 'poweron'.lower():
        return poweron()
    elif action == 'poweroff'.lower():
        return poweroff()
    elif action == 'ping'.lower():
        return ping()
    else:
        return "Unknown value '{}' for paramater 'action'. Choose from 'poweron, poweroff, ping'!".format(action)

if __name__ == '__main__':
    httpaction.run(debug=debug, host='0.0.0.0', port=tcpPort)
