import requests
from requests.auth import HTTPBasicAuth
import json

end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = []

url = 'http://{0}/relay/{1}?{2}'
shelly25_relay = {'url' : url, 'commands' : {'turn' : ['on', 'off', 'toggle'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'overtemperature', 'is_valid', 'source']}
shelly25_roller = {'url' : url, 'commands' : {'go' : ['open', 'stop', 'close'], 'pos' : ['to_pos']}, 'channel' : ['0', '1'], 'attributes' : ['state', 'power', 'is_valid', 'safety_switch', 'overtemperature', 'stop_reason', 'last_direction', 'current_pos', 'calibrating', 'positioning']}
shelly_dimmer = {'url' : url, 'commands' : {'turn' : ['on', 'off', 'toggle'], 'bright' : ['brightness'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'mode', 'brightness']}
shelly_plug = {'url' : url, 'commands' : {'turn' : ['on', 'off', 'toggle'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'overpower', 'source']}
shelly1 = {'url' : url, 'commands' : {'turn' : ['on', 'off', 'toggle'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'overpower', 'source']}

class Shelly25_roller:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = shelly25_roller

	def go(self, command : str, value : int = None, channel : str = '0'):
		if (command in self.device['commands']['go'] and channel in self.device['channel']):
			if (value == None):
				r = requests.get(self.device['url'].format(self.ip, channel, 'go=' + command))
				print(r.content.decode())
			elif (value != None):
				try:
					if (1 <= value <= 120):
						r = requests.get(self.device['url'].format(self.ip, channel, 'go=' + command + '&duration=' + str(value)))
						print(r.content.decode())
				except Exception as ex:
					print('Failed with output: ' + str(ex))

		elif (command in self.device['commands']['pos'] and channel in self.device['channel']):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				try:
					if (r.json()['positioning'] == True):
						try:
							if (1 <= value <= 100):
								r = requests.get(self.device['url'].format(self.ip, channel, 'go=' + command + '&roller_pos=' + str(value)))
								print(r.content.decode())
						except Exception as ex:
							print('Failed with output: ' + str(ex))
					else:
						print('Device isnt calibrated, to calibrate use:\nx = Shelly25_roller\nx.calibrate("0")')
				except Exception as ex:
					print('Failed with output: ' + str(ex))
					print(r.content.decode())

		else:
			print('Didnt recognise command: ' + command + ' on channel ' + channel)

	def calibrate(self, channel : str = '0'):
		if (channel in shelly25_relay['channel']):
			r = requests.get(self.device['url'].format(self.ip, channel + '/calibrate', ''))
			print(r.content.decode())

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly25_relay:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = shelly25_relay

	def turn(self, command : str, channel : str = '0', time : int = None):
		if (command in self.device['commands']['turn'] and channel in self.device['channel']):
			if (time == None):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				print(r.content.decode())
			else:
				try:
					if (0 <= time <= 120):
						r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command + '&timer=' + str(time)))
						print(r.content.decode())
				except Exception as ex:
					print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(self.ip, '0', ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()
	
	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly_dimmer:
	
	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = shelly_dimmer

	def turn(self, command : str, brightness : int = None, time : int = None, channel : str = '0'):
		if (command in self.device['commands']['turn'] and channel in self.device['channel']):
			if (brightness == None):
				if (time == None):
					r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command))
					print(r.content.decode())
				else:
					try:
						if (0 <= time <= 120):
							r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command + '&timer=' + str(time)))
							print(r.content.decode())
					except Exception as ex:
						print('Failed with output: ' + str(ex))
			else:
				if (time == None):
					try:
						if (0 <= brightness <= 100):
							r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command + '&brightness=' + str(brightness)))
							print(r.content.decode())
					except Exception as ex:
						print('Failed with output: ' + str(ex))
				else:
					try:
						if (0 <= time <= 120 and 0 <= brightness <= 120):
							r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command + '&brightness=' + str(brightness) + '&timer=' + str(time)))
							print(r.content.decode())
					except Exception as ex:
						print('Failed with output: ' + str(ex))
	
	def brightness(self, brightness : int, channel : str = '0'):
		try:
			if (0 <= brightness <= 100):
				r = requests.get(self.device['url'].format(self.ip, channel, 'brightness=' + str(brightness)))
				print(r.content.decode())
		except Exception as ex:
			print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		r = requests.get(self.device['url'].format(self.ip, '0', ''))
		print(r.json())
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly_plug:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = shelly_plug

	def turn(self, command : str, time : int = None, channel : str = '0'):
		if (time == None):
			if (command in self.device['commands']['turn']):
				r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command))
				print(r.content.decode())
		else:
			try:
				if (0 <= time <= 120):
					r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command + '&timer=' + str(time)))
					print(r.content.decode())
			except Exception as ex:
				print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly1:

	def __init__(self, ip):
		self.ip = ip
		self.errors = errors
		self.device = shelly1

	def turn(self, command : str, time : int = None, channel : str = '0'):
		if (time == None):
			if (command in self.device['commands']['turn']):
				r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command))
				print(r.content.decode())
		else:
			try:
				if (0 <= time <= 120):
					r = requests.get(self.device['url'].format(self.ip, channel, 'turn=' + command + '&timer=' + str(time)))
					print(r.content.decode())
			except Exception as ex:
				print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(self.ip, '0', ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(self.ip, channel, ''))
				return r.json()

if __name__ == '__main__':
	s = Shelly_dimmer('192.168.100.123')
	s.get_attr('ison')