'''Published from @Floplosion05 under the MIT-License'''

import requests
from requests.auth import HTTPBasicAuth
import sys
import time
import json

ips = ['floziroll','joziroll'] #add ips or mdns name of devices
help_str = 'Please provide the information in the format:\nsecure.py [mode] [username] [password]\n\nmode\temable/disable the login page\n\nusername\tthe username you wantto use\n\npassword\tthe password you want to use'
username = ''
password = ''
prev_username = 'test' #insert your previously used username
prev_password = 'test' #insert your previously used passowrd

def check_input():
	if (len(sys.argv) == 2 and sys.argv[1] == 'disable'):
		disable()
	elif (len(sys.argv) == 4 and sys.argv[1] == 'enable'):
		username = str(sys.argv[2])
		password = str(sys.argv[3])
		enable(username, password)
	elif (len(sys.argv) == 4 and sys.argv[1] == 'changeAuth'):
		changeAuth()
	else:
		print(help_str)
		quit()

def disable():
	for ip in ips:
		r = requests.get('http://' + ip + '/settings/login?enabled=0&unprotected=1&username=""', auth=(prev_username, prev_password))
		print('Disabled restricted login for ' + ip)
		print('Got output: ' + r.content.decode())

def enable(username, password):
	for ip in ips:
		r = requests.get('http://' + ip + '/settings/login?enabled=1&username=' + username + '&password=' + password)
		print('Enabled restricted login for ' + ip + ' with\nusername:\t' + username + '\npassword\t' + password)
		print('Got output: ' + r.content.decode())
		time.sleep(0.05)

def changeAuth():
	for ip in ips:
		r = requests.get('http://' + ip + '/settings/login?enabled=1&username=' + username + '&password=' + password, auth=(prev_username, prev_password))
		print('Got output: ' + r.content.decode())

if __name__ == '__main__':
	check_input()
