import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup

end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = ['Ip could not be reached', 'Device Type does not match']

url = 'http://{ip}/{type}/{channel}?{command}'
Shelly25_Relay_Dict = {'url' : url, 'type' : 'relays', 'commands' : {'turn' : ['on', 'off', 'toggle'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'overtemperature', 'is_valid', 'source']}
Shelly25_Roller_Dict = {'url' : url, 'type' : 'rollers', 'commands' : {'go' : ['open', 'stop', 'close'], 'pos' : ['to_pos']}, 'channel' : ['0', '1'], 'attributes' : ['state', 'power', 'is_valid', 'safety_switch', 'overtemperature', 'stop_reason', 'last_direction', 'current_pos', 'calibrating', 'positioning']}
Shelly_Dimmer_Dict = {'url' : url, 'type' : 'lights', 'commands' : {'turn' : ['on', 'off', 'toggle'], 'bright' : ['brightness'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'mode', 'brightness']}
Shelly_Plug_Dict = {'url' : url, 'type' : 'relays', 'commands' : {'turn' : ['on', 'off', 'toggle'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'overpower', 'source']}
Shelly1_Dict = {'url' : url, 'type' : 'relays', 'commands' : {'turn' : ['on', 'off', 'toggle'], 'time' : ['timer']}, 'channel' : ['0'], 'attributes' : ['ison', 'has_timer', 'timer_started', 'timer_duration', 'timer_remaining', 'overpower', 'source']}
Shellys = {'shelly25_relay' : Shelly25_Relay_Dict, 'shelly25_roller' : Shelly25_Roller_Dict, 'shelly_dimmer' : Shelly_Dimmer_Dict, 'shelly_plug' : Shelly_Plug_Dict, 'shelly1' : Shelly1_Dict}

class shelly25_roller:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shelly25_Roller_Dict
		self.type = 'shelly25_roller'
		self.check_device()
		self.device['url'] = self.device['url'].format(ip = '{ip}', type = 'roller', channel = '{channel}', command = '{command}')

	def check_device(self):
		r = requests.get(self.device['url'].format(ip = self.ip, type = 'status', channel = '', command = '')[:-2])
		if (r.status_code != 200):
			print('IP check failed with returncode: ' + str(r.status_code))
			self.error(0)
		else:
			print('IP check completed\n')
			r_json = json.loads(r.content.decode())
			if (self.device['type'] not in r_json):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r_json:
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

	def go(self, command : str, value : int = None, channel : str = '0'):
		if (command in self.device['commands']['go'] and channel in self.device['channel']):
			if (value == None):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'go=' + command))
				print(r.content.decode())
			elif (value != None):
				try:
					if (1 <= value <= 120):
						r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'go=' + command + '&duration=' + str(value)))
						print(r.content.decode())
				except Exception as ex:
					print('Failed with output: ' + str(ex))

		elif (command in self.device['commands']['pos'] and channel in self.device['channel']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				try:
					if (r.json()['positioning'] == True):
						try:
							if (1 <= value <= 100):
								r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'go=' + command + '&roller_pos=' + str(value)))
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
		if (channel in self.device['channel']):
			r = requests.get(self.device['url'].format(ip = self.ip, channel = channel + '/calibrate', command = ''))
			print(r.content.decode())

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class shelly25_relay:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shelly25_Relay_Dict
		self.type = 'shelly25_relay'
		self.check_device()
		self.device['url'] = self.device['url'].format(ip = '{ip}', type = 'relay', channel = '{channel}', command = '{command}')

	def check_device(self):
		r = requests.get(self.device['url'].format(ip = self.ip, type = 'status', channel = '', command = '')[:-2])
		if (r.status_code != 200):
			print('IP check failed with returncode: ' + str(r.status_code))
			self.error(0)
		else:
			print('IP check completed\n')
			r_json = json.loads(r.content.decode())
			if (self.device['type'] not in r_json):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r_json:
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

	def turn(self, command : str, channel : str = '0', time : int = None):
		if (command in self.device['commands']['turn'] and channel in self.device['channel']):
			if (time == None):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				print(r.content.decode())
			else:
				try:
					if (0 <= time <= 120):
						r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
						print(r.content.decode())
				except Exception as ex:
					print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = '0', command = ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				return r.json()
	
	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class shelly_dimmer:
	
	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shelly_Dimmer_Dict
		self.type = 'shelly_dimmer'
		print(self.device['url'])
		self.check_device()
		self.device['url'] = self.device['url'].format(ip = '{ip}', type = 'light', channel = '{channel}', command = '{command}')

	def check_device(self):
		print(self.device['url'])
		print(self.device['url'].format(ip = self.ip, type = '', channel = '', command = '')[:-2])
		r = requests.get(self.device['url'].format(ip = self.ip, type = 'status', channel = '', command = '')[:-2])
		if (r.status_code != 200):
			print('IP check failed with returncode: ' + str(r.status_code))
			self.error(0)
		else:
			print('IP check completed\n')
			r_json = json.loads(r.content.decode())
			if (self.device['type'] not in r_json):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r_json:
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')
				

	def turn(self, command : str, brightness : int = None, time : int = None, channel : str = '0'):
		if (command in self.device['commands']['turn'] and channel in self.device['channel']):
			if (brightness == None):
				if (time == None):
					r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command))
					print(r.content.decode())
				else:
					try:
						if (0 <= time <= 120):
							r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
							print(r.content.decode())
					except Exception as ex:
						print('Failed with output: ' + str(ex))
			else:
				if (time == None):
					try:
						if (0 <= brightness <= 100):
							r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&brightness=' + str(brightness)))
							print(r.content.decode())
					except Exception as ex:
						print('Failed with output: ' + str(ex))
				else:
					try:
						if (0 <= time <= 120 and 0 <= brightness <= 120):
							r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&brightness=' + str(brightness) + '&timer=' + str(time)))
							print(r.content.decode())
					except Exception as ex:
						print('Failed with output: ' + str(ex))
	
	def brightness(self, brightness : int, channel : str = '0'):
		try:
			if (0 <= brightness <= 100):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'brightness=' + str(brightness)))
				print(r.content.decode())
		except Exception as ex:
			print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = '')[:-1])
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = '')[:-1])
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class shelly_plug:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shelly_Plug_Dict
		self.type = 'shelly_plug'
		self.check_device()
		self.device['url'] = self.device['url'].format(ip = '{ip}', type = 'relay', channel = '{channel}', command = '{command}')

	def check_device(self):
		r = requests.get(self.device['url'].format(ip = self.ip, type = 'status', channel = '', command = '')[:-2])
		if (r.status_code != 200):
			print('IP check failed with returncode: ' + str(r.status_code))
			self.error(0)
		else:
			print('IP check completed\n')
			r_json = json.loads(r.content.decode())
			if (self.device['type'] not in r_json):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r_json:
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

	def turn(self, command : str, time : int = None, channel : str = '0'):
		if (time == None):
			if (command in self.device['commands']['turn']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command))
				print(r.content.decode())
		else:
			try:
				if (0 <= time <= 120):
					r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
					print(r.content.decode())
			except Exception as ex:
				print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class shelly1:

	def __init__(self, ip):
		self.ip = ip
		self.errors = errors
		self.device = Shelly1_Dict
		self.type = 'shelly1'
		self.check_device()
		self.device['url'] = self.device['url'].format(ip = '{ip}', type = 'relay', channel = '{channel}', command = '{command}')

	def check_device(self):
		r = requests.get(self.device['url'].format(ip = self.ip, type = 'status', channel = '', command = '')[:-2])
		if (r.status_code != 200):
			print('IP check failed with returncode: ' + str(r.status_code))
			self.error(0)
		else:
			print('IP check completed\n')
			r_json = json.loads(r.content.decode())
			if (self.device['type'] not in r_json):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r_json:
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

	def turn(self, command : str, time : int = None, channel : str = '0'):
		if (time == None):
			if (command in self.device['commands']['turn']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command))
				print(r.content.decode())
		else:
			try:
				if (0 <= time <= 120):
					r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
					print(r.content.decode())
			except Exception as ex:
				print('Failed with output: ' + str(ex))

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = '0', command = ''))
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

Shelly_Classes = {
					'shelly25_roller' : shelly25_roller,
					'shelly25_relay' : shelly25_relay,
					'shelly_dimmer' : shelly_dimmer,
					'shelly_plug' : shelly_plug,
					'shelly1' : shelly1
}

def auto_assign(ip : str):
	r"""Auto assigns an IP to a shelly Object
	
	auto_assign(ip : str)

	:param ip: A String containing the IP of the Shelly

	:param shelly: A variable to hold the rteurned class
	"""
	r = requests.get('http://{0}/status'.format(ip))
	if (r.status_code != 200):
		print('IP check failed')
	else:
		#print('IP check completed\n')
		r_json = json.loads(r.content.decode())
		for shelly_name, shelly in Shellys.items():
			if shelly['type'] in r_json:
				print('Shelly is of type: ' + shelly_name + '\n')
				return Shelly_Classes[shelly_name](ip)

a = auto_assign('FloziDimmer')
print(a.get_attr('all'))

if __name__ == '__main__':
	s = shelly_dimmer('192.168.100.123')
	print(type(s))
	print(s.get_attr('all'))