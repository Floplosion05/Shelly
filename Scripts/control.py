import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup
import sys

end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = ['Ip could not be reached', 'Device Type does not match']

url = 'http://{ip}/{type}/{channel}?{command}'

class Shelly:
	
	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shellys[self.__class__.__name__]
		self.check_device()

	def check_device(self):
		if (check_device_type(self.ip) != self.__class__.__name__):
			self.error(1)
		"""
		r = requests.get(self.device['url'].format(ip = self.ip, type = 'status', channel = '', command = '')[:-2])
		if (r.status_code != 200):
			print('IP check failed with returncode: ' + str(r.status_code))
			self.error(0)
		else:
			#print('IP check completed\n')
			if (self.device['type'] not in r.json()):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r.json():
						print('Wrong device type assigned: ' + self.__class__.__name__ + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				pass
				#print('Device type check completed')
		"""

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(ip = self.ip, type = self.device['type'].replace('s', ''), channel = channel, command = '')[:-1])
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(ip = self.ip, type = self.device['type'].replace('s', ''), channel = channel, command = '')[:-1])
				return r.json()
	
	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly25_Roller(Shelly):

	def go(self, command : str, value : int = None, channel : str = '0'):
		if (command in self.device['commands']['go'] and channel in self.device['channel']):
			if (value == None):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'go=' + command))
				print(r.text)
			elif (value != None):
				try:
					if (1 <= value <= 120):
						r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'go=' + command + '&duration=' + str(value)))
						print(r.text)
				except Exception as ex:
					print('Failed with output: ' + str(ex))

		elif (command in self.device['commands']['pos'] and channel in self.device['channel']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				try:
					if (r.json()['positioning'] == True):
						try:
							if (1 <= value <= 100):
								r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'go=' + command + '&roller_pos=' + str(value)))
								print(r.text)
						except Exception as ex:
							print('Failed with output: ' + str(ex))
					else:
						print('Device isnt calibrated, to calibrate use:\nx = Shelly25_roller\nx.calibrate("0")')
				except Exception as ex:
					print('Failed with output: ' + str(ex))
					print(r.text)

		else:
			print('Didnt recognise command: ' + command + ' on channel ' + channel)

	def calibrate(self, channel : str = '0'):
		if (channel in self.device['channel']):
			r = requests.get(self.device['url'].format(ip = self.ip, channel = channel + '/calibrate', command = ''))
			print(r.text)

class Shelly25_Relay(Shelly):

	def turn(self, command : str, channel : str = '0', time : int = None):
		if (command in self.device['commands']['turn'] and channel in self.device['channel']):
			if (time == None):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = ''))
				print(r.text)
			else:
				try:
					if (0 <= time <= 120):
						r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
						print(r.text)
				except Exception as ex:
					print('Failed with output: ' + str(ex))

class Shelly_Dimmer(Shelly):
				
	def turn(self, command : str, brightness : int = None, time : int = None, channel : str = '0'):
		if (command in self.device['commands']['turn'] and channel in self.device['channel']):
			if (brightness == None):
				if (time == None):
					r = requests.get(self.device['url'].format(ip = self.ip, type = 'light', channel = channel, command = 'turn=' + command))
					print(r.text)
				else:
					try:
						if (0 <= time <= 120):
							r = requests.get(self.device['url'].format(ip = self.ip, type = 'light', channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
							print(r.text)
					except Exception as ex:
						print('Failed with output: ' + str(ex))
			else:
				if (time == None):
					try:
						if (0 <= brightness <= 100):
							r = requests.get(self.device['url'].format(ip = self.ip, type = 'light', channel = channel, command = 'turn=' + command + '&brightness=' + str(brightness)))
							print(r.text)
					except Exception as ex:
						print('Failed with output: ' + str(ex))
				else:
					try:
						if (0 <= time <= 120 and 0 <= brightness <= 120):
							r = requests.get(self.device['url'].format(ip = self.ip, type = 'light', channel = channel, command = 'turn=' + command + '&brightness=' + str(brightness) + '&timer=' + str(time)))
							print(r.text)
					except Exception as ex:
						print('Failed with output: ' + str(ex))
	
	def brightness(self, brightness : int, channel : str = '0'):
		try:
			if (0 <= brightness <= 100):
				r = requests.get(self.device['url'].format(ip = self.ip, type = 'light', channel = channel, command = 'brightness=' + str(brightness)))
				print(r.text)
		except Exception as ex:
			print('Failed with output: ' + str(ex))

class Shelly_Plug(Shelly):

	def turn(self, command : str, time : int = None, channel : str = '0'):
		if (time == None):
			if (command in self.device['commands']['turn']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command))
				print(r.text)
		else:
			try:
				if (0 <= time <= 120):
					r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
					print(r.text)
			except Exception as ex:
				print('Failed with output: ' + str(ex))

class Shelly1(Shelly):

	def turn(self, command : str, time : int = None, channel : str = '0'):
		if (time == None):
			if (command in self.device['commands']['turn']):
				r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command))
				print(r.text)
		else:
			try:
				if (0 <= time <= 120):
					r = requests.get(self.device['url'].format(ip = self.ip, channel = channel, command = 'turn=' + command + '&timer=' + str(time)))
					print(r.text)
			except Exception as ex:
				print('Failed with output: ' + str(ex))

class Shelly_i3(Shelly):

	pass

class Shelly_RGBW2(Shelly):

	pass

Shellys = {
	'Shelly25_Relay' : {
		'class' : Shelly25_Relay,
        'url' : url,
        'type' : 'relays',
        'commands' : {
            'turn' : [
                'on',
                'off',
                'toggle'
            ],
            'time' : [
                'timer'
            ]
        },
        'channel' : [
            '0'
        ],
        'attributes' : [
            'ison',
            'has_timer',
            'timer_started',
            'timer_duration',
            'timer_remaining',
            'overtemperature',
            'is_valid',
            'source'
        ]
    },
	'Shelly25_Roller' : {
		'class' : Shelly25_Roller,
		'url' : url,
		'type' : 'rollers',
		'commands' : {
			'go' : [
				'open',
				'stop',
				'close'
			],
			'pos' : [
				'to_pos'
			]
		},
		'channel' : [
			'0',
			'1'
		],
		'attributes' : [
			'state',
			'power',
			'is_valid',
			'safety_switch',
			'overtemperature',
			'stop_reason',
			'last_direction',
			'current_pos',
			'calibrating',
			'positioning'
		]
	},
	'Shelly_Dimmer' : {
		'class' : Shelly_Dimmer,
		'url' : url,
		'type' : 'lights',
		'commands' : {
			'turn' : [
				'on',
				'off',
				'toggle'
			],
			'bright' : [
				'brightness'
			],
			'time' : [
				'timer'
			]
		},
		'channel' : [
			'0'
		],
		'attributes' : [
			'ison',
			'has_timer',
			'timer_started',
			'timer_duration',
			'timer_remaining',
			'mode',
			'brightness'
		]
	},
	'Shelly_Plug' : {
		'class' : Shelly_Plug,
		'url' : url,
		'type' : 'relays',
		'commands' : {
			'turn' : [
				'on',
				'off',
				'toggle'
			],
			'time' : [
				'timer'
			]
		},
		'channel' : [
			'0'
		],
		'attributes' : [
			'ison',
			'has_timer',
			'timer_started',
			'timer_duration',
			'timer_remaining',
			'overpower',
			'source'
		]
	},
	'Shelly1' : {
		'class' : Shelly1,
		'url' : url,
		'type' : 'relays',
		'commands' : {
			'turn' : [
				'on',
				'off',
				'toggle'
			],
			'time' : [
				'timer'
			]
		},
		'channel' : [
			'0'
		],
		'attributes' : [
			'ison',
			'has_timer',
			'timer_started',
			'timer_duration',
			'timer_remaining',
			'overpower',
			'source'
		]
	},
	'Shelly_i3' : {
		'class' : Shelly_i3,
		'url' : url,
		'type' : 'inputs',
		'channel' : [
			'0',
			'1',
			'2'
		],
		'attributes' : [
			'input',
			'event',
			'event_cnt'
		]
	},
	'Shelly_RGBW2' : {
		'class' : Shelly_RGBW2,
		'url' : url,
		'type' : 'lights',
		'commands' : {
			'turn' : [
				'on',
				'off',
				'toggle'
			],
			'effect' : [
				'0',
				'1',
				'2',
				'3',
				'4'
			],
			'red' : [],
			'green' : [],
			'blue' : []
		},
		'channel' : [
			'0'
		],
		'attributes' : [
			'ison',
			'source',
			'has_timer',
			'timer_started',
			'timer_duration',
			'timer_remaining',
			'mode',
			'red',
			'green',
			'blue',
			'white',
			'gain',
			'effect',
			'power',
			'overpower'
		]
	},
	'type' : {
		'lights' : [
			'Shelly_Dimmer'
		],
		'relays' : {
			'Shelly Switch' : [
				'Shelly1',
				'Shelly25_Relay'
			],
			'Shelly Plug' : [
				'Shelly_Plug'
			]
		},
		'rollers' : [
			'Shelly25_Roller'
		],
		'inputs' : [
			'Shelly_i3'
		]
	},
	'type2' : {
		'SHSW-25' : {
			'relays' : [
				'Shelly25_Relay'
			],
			'rollers' : [
				'Shelly25_Roller'
			]
		},
		'SHDM-1' : [
			'Shelly_Dimmer'
		],
		'SHDM-2' : [
			'Shelly_Dimmer'
		],
		'SHPLG-S' : [
			'Shelly_Plug'
		],
		'SHIX3-1' : [
			'Shelly_i3'
		],
		'SHRGBW2' : [
			'Shelly_RGBW2'
		]
	},
	'classes' : {
		'Shelly25_Roller' : Shelly25_Roller,
		'Shelly25_Relay' : Shelly25_Relay,
		'Shelly_Dimmer' : Shelly_Dimmer,
		'Shelly_Plug' : Shelly_Plug,
		'Shelly1' : Shelly1
	}
}

def check_device_type(ip : str, timeout : int = 3, verbose : bool = False, instantiate : bool = False):
	r"""
	Returns the device type or an instance of it of a given ip. Returns False when no device type could be associated or the ip is unreachable

	check_device(ip : str, timeout : int, verbose : bool, instantiate : bool)

	:param ip: A string containing the ip to be scanned

	:param timeout: An integer defining the maximum time before a http request times out without a response (Defaults to 3)

	:param verbose: A boolean to activate verbose output (Defaults to False)

	:param instantiate: A boolean to activate the return of instances

	"""

	ip = ip.replace('http://', '').replace('/status', '').replace('/', '')
	try:
		r1 = requests.get('http://' + ip + '/shelly', timeout = timeout)
		r2 = requests.get('http://' + ip + '/status', timeout = timeout)
		try:
			r1.json()
			r2.json()
		except Exception as ex:
			if verbose:
				print('Failed to convert Html content to JSON\n' + str(ex) + ' : ' + ip)
			return False
	except Exception as ex:
		if verbose:
			print('Failed to establish a connection\n' + str(ex) + ' : ' + ip)
		return False
	
	if r1.status_code != 200 or r2.status_code != 200:
		if verbose:
			print('Failed to establish a connection\nStatuscode: ' + str(r1.status_code) + ' : ' + ip)
			print('Failed to establish a connection\nStatuscode: ' + str(r2.status_code) + ' : ' + ip)
		return False
	else:
		for type in Shellys['type2']:
			if r1.json()['type'] == type:
				if type != 'SHSW-25':
					if instantiate:
						return Shellys[Shellys['type2'][type][0]]['class'](ip)
					else:
						return Shellys['type2'][type][0]
				else:
					for mode in Shellys['type2'][type]:
						if mode in r2.json():
							if instantiate:
								return Shellys[Shellys['type2'][type][mode][0]]['class'](ip)
							else:
								return Shellys['type2'][type][mode][0]
							break
				break

def device_discovery(ip_start : str, ip_end : str, timeout : int = 3, verbose : bool = False, beautify : bool = False, instantiate : bool = False, outputFile : bool = False):
	r"""Discovers devices in a given ip range, returning a Dict of IP's 
	
	device_discovery(ip_start : str, ip_end : str, timeout : int, verbose : bool, beautify : bool)

	:param ip_start: A String containing the starting IP

	:param ip_end: A String containing the ending IP, must be higher than ip_start!

	:param timeout: An integer defining the maximum time before a http request times out without a response (Defaults to 3)

	:param verbose: A boolean to activate verbose output (Defaults to False)

	:param beautify: A boolean to beautify the output of this function in the shell (Defaults to False)

	:param outputFile: A boolean to activate the outputFile (Shellys.json) located in the same directory

	"""
	ip_start_list = list(map(int,ip_start.split('.')))
	ip_end_list = list(map(int, ip_end.split('.')))
	shellys = {
		'Shelly25_Relay' : [
		],
		'Shelly25_Roller' : [
		],
		'Shelly_Dimmer' : [
		],
		'Shelly_Plug' : [
		],
		'Shelly1' : [
		],
		'Shelly_i3' : [
		],
		'Shelly_RGBW2' : [
		]
	}
	shellys_instances = {
		'Shelly25_Relay' : [
		],
		'Shelly25_Roller' : [
		],
		'Shelly_Dimmer' : [
		],
		'Shelly_Plug' : [
		],
		'Shelly1' : [
		],
		'Shelly_i3' : [
		],
		'Shelly_RGBW2' : [
		]
	}
	for a in range(ip_start_list[0], ip_end_list[0] + 1):
		for b in range(ip_start_list[1], ip_end_list[1] + 1):
			for c in range(ip_start_list[2], ip_end_list[2] + 1):
				for d in range(ip_start_list[3], ip_end_list[3] + 1):
					temp_ip = str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)
					temp_device_type = check_device_type(temp_ip, timeout, verbose, instantiate)

					if temp_device_type:
						if instantiate:
							shellys[temp_device_type.__class__.__name__].append(temp_ip)
							shellys_instances[temp_device_type.__class__.__name__].append(temp_device_type)
							if verbose:
								print(temp_ip + ' : ' + str(temp_device_type.__class__.__name__))
						else:
							try:
								shellys[temp_device_type].append(temp_ip)
							except KeyError as e:
								print('lol')
								continue
							if verbose:
								print(temp_ip + ' : ' + str(temp_device_type))
					else:
						continue

	if outputFile:
		with open('Shellys.json', 'w+') as outfile:
			json.dump(shellys, outfile)
	else:
		if beautify:
			print(json.dumps(shellys, sort_keys = True, indent=4))
		else:
			print(shellys)
		
	if instantiate:
		return shellys_instances
	
#Shelly RGB support
#secure.py zusammenführen

if __name__ == '__main__':

	#for arg in sys.argv:
	shelly_instances = device_discovery('192.168.100.0', '192.168.100.255', 3, False, True, True)
	for shelly_type, shelly_instance_list in shelly_instances.items():
		for shelly_instance in shelly_instance_list:
			print(shelly_instance.get_attr('all'))
	#a = check_device_type('FloziDimmer', 3, True, True)
	#print(a.get_attr('brightness'))
	#s = Shelly_Dimmer('192.168.100.123')
	#print(s.get_attr('all'))