'''Published from @Floplosion05 under the MIT-License'''

import requests
from requests.auth import HTTPBasicAuth
import sys
import time
import json
from passlib.context import CryptContext
import _io
import os.path

ips = ['floziroll'] #add ips or mdns name of devices
help_str = 'Please provide the information in the format:\nsecure.py [mode] [username] [password]\n\nmode\t\tenable/disable the login page\n\nusername\tthe username you want to use\n\npassword\tthe password you want to use'
errors = ['Failed to load Shelly.json, check the directory and path.\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly', '']
commands = ['disable', 'enable']

class Shelly:

	def __init__(self, ip, mode, password, username, errors):
		self.ip = ip
		self.mode = mode
		self.password = password
		self.username = password
		self.errors = errors
		self.pwd_context = CryptContext(
			schemes=["pbkdf2_sha256"],
			default="pbkdf2_sha256",
			pbkdf2_sha256__default_rounds=30000
			)
		eval('self.' + self.mode)()


	def enable(self):
		r = requests.get('http://' + self.ip + '/settings/login?enabled=1&username=' + self.username + '&password=' + self.password)
		print('Enabled restricted login for ' + self.ip + ' with\nusername:\t' + self.username + '\npassword\t' + self.password + '\n')
		if r.content.decode() == '401 Unauthorized':
			self.changeAuth()
		content_json = r.json()
		if content_json['enabled'] and content_json['enabled'] == 'true':
			print(content_json['enabled'])
			pass

	def disable(self):
		self.prev_username, self.prev_password = self.load()
		r = requests.get('http://' + self.ip + '/settings/login?enabled=0&unprotected=1&username=""', auth=(self.prev_username, self.prev_password))
		print('Disabled restricted login for ' + self.ip)
		print('Got output: ' + r.content.decode())

	def changeAuth(self):
		r = requests.get('http://' + self.ip + '/settings/login?enabled=1&username=' + self.username + '&password=' + self.password, auth=(self.prev_username, self.prev_password))
		print('Got output: ' + r.content.decode())

	def load(self):
		if os.path.isfile('Shellys.json'):
			with open('Shellys.json', 'r') as f:
				self.data = json.loads(f.read().strip())
				return json.dumps(self.data), json.dumps(self.data)
		else:
			self.error(0)

	def save(self):
		if os.path.isfile('Shellys.json'):
			with open('Shellys.json', 'a') as f:
				devices = json.loads(f.read().strip())
				print(devices)
		else:
			with open('Shellys.json', 'w') as f:
				f.write({'devices':[{'ip':self.ip, 'username':self.username, 'password':self.password}]})

	def encrypt_password(self, password):
		return self.pwd_context.encrypt(password)

	def check_encrypted_password(self, password, hashed):
		return self.pwd_context.verify(password, hashed)

	def error(self, code):
		exit(self.errors[code])

def check_input():
	if len(sys.argv) > 1 and sys.argv[1] in commands:
		if len(sys.argv) == 2:
			for ip in ips:
				ips[ips.index(ip)] = Shelly(ip, sys.argv[1], '', '', errors)
		elif len(sys.argv) == 4:
			for ip in ips:
				ips[ips.index(ip)] = Shelly(ip, sys.argv[1], sys.argv[2], sys.argv[3], errors)
		else:
			print(help_str)
			quit()
	else:
		print(help_str)
		quit()

if __name__ == '__main__':
	check_input()