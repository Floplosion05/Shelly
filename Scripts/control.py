import requests
from requests.auth import HTTPBasicAuth

help_str = 'Please provide the information in the format:\nsecure.py [command] [value]'

shelly25_relay_url = 'http://{0}/relay/{1}?{2}'
shelly25_relay_commands = {'turn' : [{'cmd1' : 'on'}, {'cmd2' : 'off'}, {'cmd3' : 'toggle'}], 'timer' : None}
shelly25_relay_commands = {'turn' : ['on', 'off', 'toggle'], 'timer' : None}
shelly25_relay = {'url' : shelly25_relay_url, 'commands' : shelly25_relay_commands}

class Shelly:

    def __init__(self):
        pass

def check_input():
    if len(sys.argv) == 3 and sys.argv[1] in commands:
        for ip in ips:

if __name__ == '__main__':
	check_input()