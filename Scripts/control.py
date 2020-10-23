import requests
from requests.auth import HTTPBasicAuth
import re
import sys

end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = []

shelly25_relay_url = 'http://{0}/relay/{1}?{2}'
shelly25_roller_url = 'http://{0}/roller/{1}?{2}'
shelly25_relay_commands = {'turn' : ['on', 'off', 'toggle'], 'timer' : None}
shelly25_roller_commands = {'go' : ['open', 'stop', 'close'], 'roller_pos' : None}
shelly25_relay = {'url' : shelly25_relay_url, 'commands' : shelly25_relay_commands}
shelly25_roller = {'url' : shelly25_roller_url, 'commands' : shelly25_relay_commands}
devices = [shelly25_relay, shelly25_roller]

class Shelly25:

	def __init__(self, type, ip, command, errors, value = None):
		self.type = type
		self.ip = ip
		self.command = command
		if self.type == 'Roller':
			pass


		self.errors = errors

	def go(self, device):
		r = requests.get(device['url'].format(self.ip, self.channel, self.command))
		pass

	def pos(self, device):
		r = requests.get('')

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)