'''Published by @Floplosion05 under the MIT-License'''

import requests
from requests.auth import HTTPBasicAuth
import sys
import json
from passlib.context import CryptContext
import _io
import os.path
import re

ips = ['192.168.100.74'] #add ips or mdns names of devices
help_str = 'Please provide the information in the format:\nsecure.py [mode] [username] [password]\n\nmode\t\tenable/disable the login page\n\nusername\tthe username you want to use\n\npassword\tthe password you want to use'
end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
pwd_str = 'The username and password must be between 1 and 50 caracters'
errors = ['Failed to load Shelly.json, check the directory and path.', 'Wrong password entered.', 'Right hash found but wrong password provided.', 'Found Shelly.json, but didnt find entry for this device', 'Found Shelly.json, but its empty', 'Fatal error']
commands = ['disable', 'enable']

class Shelly:

	def __init__(self, ip, mode, username, password, errors):
		self.ip = ip
		self.mode = mode
		self.password = password
		self.username = username
		self.errors = errors
		self.pwd_context = CryptContext(
			schemes=["pbkdf2_sha256"],
			default="pbkdf2_sha256",
			pbkdf2_sha256__default_rounds=30000
			)
		if not eval('self.' + self.mode)():
			self.error(5)


	def enable(self):
		r = requests.get('http://' + self.ip + '/settings/login?enabled=1&unprotected=0&username=' + self.username + '&password=' + self.password)
		print('Enabling restricted login for ' + self.ip + ' with\nusername:\t' + self.username + '\npassword\t' + self.password + '\n')
		if r.content.decode() == '401 Unauthorized':
			print('Login already restricted\n')
			if self.changeAuth():
				return True
			else:
				return False
		else:
			try:
				content_json = r.json()
			except Exception:
				print('Failed with output: ' + r.content.decode())
			else:
				if content_json['enabled'] and content_json['unprotected'] == False and content_json['username'] == self.username:
					print('Succesfully enabled restricted-login, saving the credentials')
					if self.save():
						return True
					else:
						return False

	def disable(self):
		self.prev_username, self.prev_password_hash = self.load()
		if self.check_encrypted_password(self.password, self.prev_password_hash):
			r = requests.get('http://' + self.ip + '/settings/login?enabled=0&unprotected=1&username=""', auth=(self.username, self.password))
			print('Disabling restricted login for ' + self.ip)
			try:
				content_json = r.json()
			except Exception:
				print('Failed with output: ' + r.content.decode())
			else:
				if content_json['enabled'] == False and content_json['unprotected'] == True:
					print('Succesfully disabled the restricted-login')
				else:
					print('Failed with output: ' + r.content.decode())
		else:
			self.error(1)

	def changeAuth(self):
		self.prev_username, self.prev_password_hash = self.load()
		self.prev_password = input('Please enter your last password:\n')
		if self.check_encrypted_password(self.prev_password, self.prev_password_hash):
			print('Changing authentification-credentials to:\nusername\t' + self.username + '\npassword\t' + self.password)
			r = requests.get('http://' + self.ip + '/settings/login?enabled=1&username=' + self.username + '&password=' + self.password, auth=(self.prev_username, self.prev_password))
			try:
				content_json = r.json()
			except Exception:
				print('Failed with output: ' + r.content.decode())
			else:
				if content_json['enabled'] == True and content_json['unprotected'] == False:
					print('Succesfull, saving the credentials')
					if self.save():
						return True
					else:
						return False
				else:
					print('Failed with output: ' + r.content.decode())
					self.error(2)

		else:
			self.error(1)

	def load(self):
		if os.path.isfile('Shellys.json'):#Check if File exists
			with open('Shellys.json', 'r') as f:
				data = json.load(f)
				for device in data['devices']:#get device credentials
					if self.ip == device['ip']:
						return device['username'], device['password']
				self.error(3)
		else:
			self.error(0)

	def save(self):
		hashed = self.encrypt_password(self.password)#create hash for password
		print('Hash: ' + hashed + '\n')
		if os.path.isfile('Shellys.json'):
			with open('Shellys.json', 'r') as f:
				data = json.load(f)
				for device in data['devices']:
					if self.ip == device['ip']:
						print('Device already exists in Credentials-File, overwriting')
						device['username'] = self.username
						device['password'] = hashed
						with open('Shellys.json', 'w') as f:
							json.dump(data, f)
						return True

				else:
					print('Device doesnt exist in Credentials-File, appending')
					data['devices'].append({"ip":self.ip, "username":self.username, "password":hashed})
					print(data)
					with open('Shellys.json', 'w') as f:
						json.dump(data, f)
					return True
		else:
			print('File doesnt exist, creating now')
			with open('Shellys.json', 'w') as f:
				json.dump({"devices":[{"ip":self.ip, "username":self.username, "password":hashed}]}, f)
			return True

	def encrypt_password(self, password):
		return self.pwd_context.hash(password)

	def check_encrypted_password(self, password, hashed):
		return self.pwd_context.verify(password, hashed)

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

def check_input():
	if len(sys.argv) == 4 and sys.argv[1] in commands:
		if 1 <= len(sys.argv[2]) <= 50 and 1 <= len(sys.argv[3]) <= 50:
			for ip in ips:
				ips[ips.index(ip)] = Shelly(ip, sys.argv[1], sys.argv[2], sys.argv[3], errors)
		else:
			print(pwd_str)
			quit()
	else:
		print(help_str)
		quit()

if __name__ == '__main__':
	check_input()