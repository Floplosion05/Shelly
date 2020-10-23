import requests
from requests.auth import HTTPBasicAuth
import json

end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = []

#shelly25_relay = {'url' : 'http://{0}/relay/{1}?{2}', 'commands' : {'turn' : ['on', 'off', 'toggle'], 'timer' : None}}
shelly25_roller = {'url' : 'http://{0}/roller/{1}?{2}', 'commands' : {'move' : ['open', 'stop', 'close'], 'pos' : ['to_pos']}}

class Shelly25_roller:

	def __init__(self, ip):
		self.type = type
		self.ip = ip
		self.errors = errors

	def go(self, command, value = None, channel = 0):
		if (command in shelly25_roller['commands']['move']):
			if (value == None):
				r = requests.get(shelly25_roller['url'].format(self.ip, channel, 'go=' + command))
				print(r.content.decode())
			elif (value != None):
				try:
					if (1 <= value <= 120):
						r = requests.get(shelly25_roller['url'].format(self.ip, channel, 'turn=' + command + '&duration=' + str(value)))
						print(r.content.decode())
				except Exception as ex:
					print('Failed with output: ' + str(ex))
					print(r.content.decode())

		elif (command in shelly25_roller['commands']['pos']):
				r = requests.get(shelly25_roller['url'].format(self.ip, channel, ''))
				try:
					if (r.json()['positioning'] == True):
						try:
							if (1 <= value <= 100):
								r = requests.get(shelly25_roller['url'].format(self.ip, channel, 'go=' + command + '&roller_pos=' + str(value)))
								print(r.content.decode())
						except Exception as ex:
							print('Failed with output: ' + str(ex))
							print(r.content.decode())
					else:
						print('Device isnt calibrated, to calibrate use:\nx = Shelly25_roller\nx.calibrate()')
				except Exception as ex:
					print('Failed with output: ' + str(ex))
					print(r.content.decode())

		else:
			print('Didnt recognise command: ' + command)

	def calibrate(self):
		r = requests.get(shelly25_roller['url'].format(self.ip, '0/calibrate', ''))
		print(r.content.decode())

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

if __name__ == '__main__':
	s = Shelly25_roller('192.168.xxx.xxx')
	s.go('to_pos', 100)