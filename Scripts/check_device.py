import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup

Shellys = {
	'type' : {
		'lights' : [
			'Shelly_Dimmer'
		],
		'relays' : {
			'Shelly Switch' : [
				'Shelly1',
				'Shelly25-Relay'
			],
			'Shelly Plug' : [] #Shelly Plug
		},
		'rollers' : [
			'Shelly25_Roller'
		]
	}
}

def check_device_type(ip : str, timeout : int = 5, verbose : bool = False) -> str:

	ip = ip.replace('http://','').replace('/status', '').replace('/','')
	try:
		r1 = requests.get('http://' + ip + '/status', timeout = timeout)
		r2 = requests.get('http://' + ip, timeout = timeout)
	except requests.exceptions.RequestException as e:
		if verbose:
			print('Failed with error: ' + str(e))
		return False

	if r1.status_code != 200:
		if verbose:
			print('IP not found, errorcode: ' + str(r1.status_code))
		return False
	else:
		for type in Shellys['type']:
			if type in r1.json() and type != 'relays':
				return Shellys['type'][type][0]
			elif type in r1.json():
				soup = BeautifulSoup(r2.content, 'html.parser')
				if soup.find('head').title.get_text() in Shellys['type'][type] and soup.find('head').title.get_text() != 'Shelly Switch':
					return list(Shellys['type'][type])[list(Shellys['type'][type]).index(soup.find('head').title.get_text())]
				elif soup.find('head').title.get_text() in Shellys['type'][type]:
					return Shellys['type'][type][soup.find('head').title.get_text()][len(r1.json()['relays']) - 1]

if __name__ == '__main__':
	print(check_device_type('FloZiRoll'))