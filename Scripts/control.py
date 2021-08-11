import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup
import sys
from check_device import check_device_type

end_str = '\n\nIf you are having trouble, please visit https://github.com/Floplosion05/Shelly'
errors = ['Ip could not be reached', 'Device Type does not match']

url = 'http://{ip}/{type}/{channel}?{command}'
   
Shellys = {
	'Shelly25_Relay' : {
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
	}
}

class Shelly25_Roller:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shellys['Shelly25_Roller']
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
			if (self.device['type'] not in r.json()):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r.json():
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

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

class Shelly25_Relay:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shellys['Shelly25_Relay']
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
			if (self.device['type'] not in r.json()):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r.json():
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

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

class Shelly_Dimmer:
	
	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shellys['Shelly_Dimmer']
		self.type = 'shelly_dimmer'
		self.check_device()

	def check_device(self):
		print(self.device['url'].format(ip = self.ip, type = '', channel = '', command = '')[:-2])
		r = requests.get(self.device['url'].format(ip = self.ip, type = 'status', channel = '', command = '')[:-2])
		if (r.status_code != 200):
			print('IP check failed with returncode: ' + str(r.status_code))
			self.error(0)
		else:
			print('IP check completed\n')
			if (self.device['type'] not in r.json()):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r.json():
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')
				

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

	def get_attr(self, attr : str, channel : str = '0'):
		if (channel in self.device['channel']):
			if (attr in self.device['attributes']):
				r = requests.get(self.device['url'].format(ip = self.ip, type = 'light', channel = channel, command = '')[:-1])
				return r.json()[attr]
			elif (attr == 'all'):
				r = requests.get(self.device['url'].format(ip = self.ip, type = 'light', channel = channel, command = '')[:-1])
				return r.json()

	def error(self, code):
		exit('Device:\t' + self.ip + '\n' + self.errors[code] + '\nErrorcode: ' + str(code) + end_str)

class Shelly_Plug:

	def __init__(self, ip : str):
		self.ip = ip
		self.errors = errors
		self.device = Shellys['Shelly_Plug']
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
			if (self.device['type'] not in r.json()):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r.json():
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

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

class Shelly1:

	def __init__(self, ip):
		self.ip = ip
		self.errors = errors
		self.device = Shellys['Shelly1']
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
			if (self.device['type'] not in r.json()):
				print('Device type check failed')
				for shelly_name, shelly in Shellys.items():
					if shelly['type'] in r.json():
						print('Wrong device type assigned: ' + self.type + ', device is of type: ' + shelly_name + '\n')
						break
				self.error(1)
			else:
				print('Device type check completed')

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
					'Shelly25_Roller' : Shelly25_Roller,
					'Shelly25_Relay' : Shelly25_Relay,
					'Shelly_Dimmer' : Shelly_Dimmer,
					'Shelly_Plug' : Shelly_Plug,
					'Shelly1' : Shelly1
}

def auto_assign(ip : str):
	r"""Auto assigns an IP to a shelly Object
	
	auto_assign(ip : str)

	:param ip: A String containing the IP of the Shelly
	"""
	r = requests.get('http://{0}/status'.format(ip))
	if (r.status_code != 200):
		print('IP check failed')
	else:
		#print('IP check completed\n')
		for shelly_name, shelly in Shellys.items():
			if shelly['type'] in r.json():
				print('Shelly is of type: ' + shelly_name + '\n')
				return Shelly_Classes[shelly_name](ip)

def device_discovery(ip_start : str, ip_end : str, timeout : int = 1, verbose = False, beautify : bool = False):
	ip_start_list = list(map(int,ip_start.split('.')))#[::-1]
	ip_end_list = list(map(int, ip_end.split('.')))#[::-1]
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
		]
	}
	for a in range(ip_start_list[0], ip_end_list[0] + 1):
		for b in range(ip_start_list[1], ip_end_list[1] + 1):
			for c in range(ip_start_list[2], ip_end_list[2] + 1):
				for d in range(ip_start_list[3], ip_end_list[3] + 1):
					temp_ip = str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)
					temp_device_type = check_device_type(temp_ip, timeout, verbose)
					if verbose:
						print(temp_ip + ' : ' + str(temp_device_type))
					try:
						shellys[temp_device_type].append(temp_ip)
					except KeyError as e:
						continue
					
	if beautify:
		print(json.dumps(shellys, sort_keys = True, indent=4))
	else:
		print(shellys)

if __name__ == '__main__':

	#for arg in sys.argv:

	device_discovery('192.168.100.0', '192.168.100.255',1,True,True)
	#a = auto_assign('FloziDimmer')
	#print(a.get_attr('brightness'))
	#a.brightness(67)
	#s = shelly_dimmer('192.168.100.123')
	#print(s.get_attr('all'))