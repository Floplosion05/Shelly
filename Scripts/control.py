import requests
from requests.auth import HTTPBasicAuth
import json

end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = []

shelly25_relay = {'url' : 'http://{0}/relay/{1}?{2}', 'commands' : {'turn' : ['on', 'off', 'toggle'], 'time' : ['timer']}, 'channel' : [0]}
shelly25_roller = {'url' : 'http://{0}/roller/{1}?{2}', 'commands' : {'go' : ['open', 'stop', 'close'], 'pos' : ['to_pos']}, 'channel' : [0, 1]}
shelly_dimmer = {'url' : 'http://{0}/light/{1}?{2}', 'commands' : {'turn' : ['on', 'off', 'toggle'], 'bright' : ['brightness'], 'time' : ['timer']}, 'channel' : [0]}

class Shelly25_roller:

	def __init__(self, ip):
		self.ip = ip
		self.errors = errors

	def go(self, command, value = None, channel = 0):
		if (command in shelly25_roller['commands']['go'] and channel in shelly25_roller['channel']):
			if (value == None):
				r = requests.get(shelly25_roller['url'].format(self.ip, str(channel), 'go=' + command))
				print(r.content.decode())
			elif (value != None):
				try:
					if (1 <= value <= 120):
						r = requests.get(shelly25_roller['url'].format(self.ip, str(channel), 'turn=' + command + '&duration=' + str(value)))
						print(r.content.decode())
				except Exception as ex:
					print('Failed with output: ' + str(ex))
					print(r.content.decode())

		elif (command in shelly25_roller['commands']['pos'] and channel in shelly25_relay['channel']):
				r = requests.get(shelly25_roller['url'].format(self.ip, str(channel), ''))
				try:
					if (r.json()['positioning'] == True):
						try:
							if (1 <= value <= 100):
								r = requests.get(shelly25_roller['url'].format(self.ip, str(channel), 'go=' + command + '&roller_pos=' + str(value)))
								print(r.content.decode())
						except Exception as ex:
							print('Failed with output: ' + str(ex))
							print(r.content.decode())
					else:
						print('Device isnt calibrated, to calibrate use:\nx = Shelly25_roller\nx.calibrate(0)')
				except Exception as ex:
					print('Failed with output: ' + str(ex))
					print(r.content.decode())

		else:
			print('Didnt recognise command: ' + command + ' on channel ' + str(channel))

	def calibrate(self, channel):
		if (channel in shelly25_relay['channel']):
			r = requests.get(shelly25_roller['url'].format(self.ip, '0/calibrate', ''))
			print(r.content.decode())

	def get_attr(self, attr):
		pass

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly25_relay:

	def __init__(self, ip):
		self.ip = ip
		self.errors = errors

	def turn(self, command, channel = 0, time = None):
		if (time == None):
			if (command in shelly25_relay['commands']['turn'] and channel in shelly25_relay['channel']):
				r = requests.get(shelly25_roller['url'].format(self.ip, channel, ''))
				print(r.content.decode())
		else:
			try:
				if (0 <= time <= 120):
					r = requests.get(shelly25_roller['url'].format(self.ip, str(channel), 'turn=' + command + '&timer=' + str(time)))
					print(r.content.decode())
			except Exception as ex:
				print('Failed with output: ' + str(ex))
				print(r.content.decode())

	def get_attr(self, attr):
		pass
	
	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly_dimmer:
	
	def __init__(self, ip):
		self.ip = ip
		self.errors = errors

	def turn(self, command, brightness = None, channel = 0):
		if (brightness == None):
			if (command in shelly_dimmer['commands'][command]):
				r = requests.get(shelly_dimmer['url'].format(self.ip, str(channel), 'turn=' + command))
		else:
			try:
				if (0 <= brightness <= 100):
					r = requests.get(shelly_dimmer['url'].format(self.ip, str(channel), 'turn=' + command + '&brightness=' + str(brightness)))
					print(r.content.decode())
			except Exception as ex:
				print('Failed with output: ' + str(ex))
				print(r.content.decode())
	
	def brightness(self, brightness, channel = 0):
		try:
			if (0 <= brightness <= 100):
				r = requests.get(shelly_dimmer['url'].format(self.ip, str(channel), 'brightness=' + str(brightness)))
				print(r.content.decode())
		except Exception as ex:
			print('Failed with output: ' + str(ex))
			print(r.content.decode())

	def get_attr(self, attr):
		pass

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class shelly_plug:

	def __init__(self, ip):
		self.ip = ip
		self.errors = errors

	def turn(self, command):
		pass

if __name__ == '__main__':
	s = Shelly_dimmer('192.168.100.123')
	s.turn('toggle', 10)