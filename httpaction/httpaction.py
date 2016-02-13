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

httpaction = Flask(__name__)

@httpaction.route(httpPath)
def index():
    
    def poweron():
        if mac != None:
           if ip != None:
               command = "{}wakeonlan -i {} {}".format(wakeonlanPath, ip,  mac)
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

    def poweron():
        if user != None and ip != None:
            command = "ssh -t {}@{} 'sudo shutdown -h now'".format(user, ip)
            p = subprocess.Popen(
                   command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                   shell=True)
            stdout, stderr = p.communicate()
            return stdout + stderr
        elif user == None:
            return "Action 'poweroff' must have parameter 'user'!"
        elif ip == None:
            return "Action 'poweroff' must have parameter 'ip'!"
            
    action = request.args.get('action')
    mac = request.args.get('mac')
    user = request.args.get('user')
    ip = request.args.get('ip')
    if action == 'poweron'.lower():
        return poweron()
    elif action == 'poweroff'.lower():
        return poweroff()
    else:
        return "Unknown value '{}' for paramater 'action'. Choose from 'poweron, poweroff'!".format(action)

if __name__ == '__main__':
    httpaction.run(debug=debug, host='0.0.0.0', port=tcpPort)
