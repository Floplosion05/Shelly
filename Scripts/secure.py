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
end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = ['Failed to load Shelly.json, check the directory and path.' + end_str, 'Wrong password entered' + end_str]
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
		r = requests.get('http://' + self.ip + '/settings/login?enabled=1&unprotected=0&username=' + self.username + '&password=' + self.password)
		print('Enabling restricted login for ' + self.ip + ' with\nusername:\t' + self.username + '\npassword\t' + self.password + '\n')
		if r.content.decode() == '401 Unauthorized':
			print('Login already restricted')
			self.changeAuth()
			return
		content_json = r.json()
		if content_json['enabled'] and content_json['unprotected'] == False and content_json['username'] == self.username:
			print('Succesfull, saving the credentials')
			self.save()

	def disable(self):
		self.prev_username, self.prev_password_hash = self.load()
		self.prev_password = input('Please enter your last password:\n')
		if self.check_encrypted_password(self.prev_password, self.prev_password_hash):
			r = requests.get('http://' + self.ip + '/settings/login?enabled=0&unprotected=1&username=""', auth=(self.prev_username, self.prev_password))
			print('Disabled restricted login for ' + self.ip)
		else:
			self.error(1)

	def changeAuth(self):
		self.prev_username, self.prev_password_hash = self.load()
		self.prev_password = input('Please enter your last password:\n')
		if self.check_encrypted_password(self.prev_password, self.prev_password_hash):
			print('Changing authentification-credentials to:\nusername\t' + self.prev_username + '\npassword\t' + self.prev_password)
			r = requests.get('http://' + self.ip + '/settings/login?enabled=1&username=' + self.username + '&password=' + self.password, auth=(self.prev_username, self.prev_password))
			self.save()
		else:
			self.error(1)

	def load(self):
		if os.path.isfile('Shellys.json'):
			with open('Shellys.json', 'r') as f:
				self.data = json.load(f)
				for device in self.data['devices']:
					print('test')
					if self.ip == device['ip']:
						print('Device found')
						return device['username'], device['password']
		else:
			self.error(0)

	def save(self):
		self.hash = self.encrypt_password(self.password)
		print('Hash: ' + self.hash)
		if os.path.isfile('Shellys.json'):
			with open('Shellys.json', 'r') as f:
				self.data = json.load(f)
				for device in self.data['devices']:
					if self.ip == device['ip']:
						return True
				self.data['devices'].append({"ip":self.ip, "username":self.username, "password":self.hash})
				print(self.data)
		else:
			print('File doesnt exist, creating now')
			with open('Shellys.json', 'w') as f:
				json.dump({"devices":[{"ip":self.ip, "username":self.username, "password":self.hash}]}, f)

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