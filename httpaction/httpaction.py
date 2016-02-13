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
               command = "{}wakeonlan -i {} {}".format(ip, wakeonlanPath, mac)
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
            
    action = request.args.get('action')
    mac = request.args.get('mac')
    ip = request.args.get('ip')
    if action == 'poweron'.lower():
        return poweron()
    else:
        return "Unknown value '{}' for paramater 'action'. Choose from 'poweron, poweroff'!".format(action)

if __name__ == '__main__':
    httpaction.run(debug=debug, host='0.0.0.0', port=tcpPort)
