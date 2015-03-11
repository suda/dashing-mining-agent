import requests
import json
import socket
import datetime
import time
import re
import sys
from subprocess import check_output
from os import path

history_file_path = path.join(path.dirname(path.abspath(__file__)), 'history.json')

settings = {}
history = {}

def update_number_widget(dashboard_name, widget, value):
	widget = dashboard_name + '_' + widget
	old_value = history.get(widget)
	payload = {
		'auth_token': settings.get('dashing-auth-token'),
		'current': value
	}

	if old_value is not None:		
		payload.update({'last': old_value})

	requests.post(settings.get('dashing-url') + 'widgets/' + widget, data=json.dumps(payload))	
	history.update({ widget: value})

def update_graph_widget(dashboard_name, widget, value):
	widget = dashboard_name + '_' + widget
	points = history.get(widget)
	payload = {
		'auth_token': settings.get('dashing-auth-token')		
	}

	if points is None:		
		points = []

	last_x = 1
	for point in points:
		last_x = max(last_x, point['x'])

	points.append({ 'x': last_x + 1, 'y': value})
	points = points[-10:]
	payload.update({'points': points})

	requests.post(settings.get('dashing-url') + 'widgets/' + widget, data=json.dumps(payload))
	history.update({ widget: points})

def update_text_widget(dashboard_name, widget, text):
	widget = dashboard_name + '_' + widget
	payload = {
		'auth_token': settings.get('dashing-auth-token'),
		'text': text
	}

	requests.post(settings.get('dashing-url') + 'widgets/' + widget, data=json.dumps(payload))

def update_temperature_widget(dashboard_name, widget, data):
	widget = dashboard_name + '_' + widget

	if data == -1:
		return

	points = []
	for point in data:
		points.append({
			'x': int(point[0]),
			'y': convert_temp(float(point[1]))
		})
	
	payload = {
		'auth_token': settings.get('dashing-auth-token'),
		'points': points
	}
	
	requests.post(settings.get('dashing-url') + 'widgets/' + widget, data=json.dumps(payload))	

def convert_temp(data):
        if settings.get('temperature-units') == 'Fahrenheit':
                data = round((data * 9/5) + 32, 2)
        return float(data)
        
def convert_hash(data):
        if settings.get('hash-units') == 'KH/s':
                data = data * 1000
        if settings.get('hash-units') == 'GH/s':
                data = data / 1000
        return data

def get_minerd_summary():
	minerd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	minerd_socket.connect((settings.get('minerd-address'), settings.get('minerd-port')))
	minerd_socket.sendall('{"command":"summary"}')
	received_data = minerd_socket.recv(4096)
	summary = json.loads(received_data[:-1])

	return summary

def get_minerd_pool_summary():
        minerd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        minerd_socket.connect((settings.get('minerd-address'), settings.get('minerd-port')))
        minerd_socket.sendall('{"command":"pools"}')
        received_data = minerd_socket.recv(4096)
        pool_summary = json.loads(received_data[:-1])

        return pool_summary

def check_cpuminer():
        minerd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        minerd_socket.connect((settings.get('minerd-address'), settings.get('minerd-port')))
        minerd_socket.sendall('{"get":"stats"}\n')

        if "error" in minerd_socket.recv(4096):
                cpuminer = True
        else:
                cpuminer = False

        return cpuminer

def get_cpuminer_summary():
        minerd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        minerd_socket.connect((settings.get('minerd-address'), settings.get('minerd-port')))

        minerd_socket.sendall('{"get":"stats"}\n')
        received_data = minerd_socket.recv(16384)

        summary = json.loads(received_data.replace("\'", '"'))

        return summary

def get_temperature():
	if sys.platform == 'linux2':
                version = check_output(['uname', '-m'])[:3]

                if version == 'arm':
                        if path.isfile('/opt/vc/bin/vcgencmd'):
                                output = check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
                                output = "Sensor 0: Temperature - " + output.replace("temp=","").replace("'C\n"," C")
                        else:
                                output = ""
                else:
                        if path.isfile('/usr/bin/aticonfig'):
                                output = check_output(['/usr/bin/aticonfig', '--odgt'])
                        else:
                                output = ""

                matches = re.findall("Sensor ([0-9]+): Temperature - ([0-9]+\.[0-9]+)", output)
                
		if matches != []:			
			return matches
	elif sys.platform == 'win32':
		# On windows, cgminer _should_ be able to obtain temperature info
		minerd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		minerd_socket.connect((settings.get('minerd-address'), settings.get('minerd-port')))
		minerd_socket.sendall('{"command":"devs"}')
		received_data = minerd_socket.recv(4096)
		devs = json.loads(received_data[:-1])
		temps = []
		for dev in devs['DEVS']:
			temps.append((dev['GPU'], dev['Temperature']))
		return temps
	return -1

if __name__ == '__main__':
	try:
		settings_file = open(path.join(path.dirname(path.abspath(__file__)), 'settings.json'))
		settings = json.load(settings_file)
		settings_file.close()
	except IOError:
		raise Exception(u'Missing settings.json file')

	# Try to load local settings if they exist
	try:
		settings_file = open(path.join(path.dirname(path.abspath(__file__)), 'local_settings.json'))
		settings.update(json.load(settings_file))
		settings_file.close()
	except IOError:
		pass

	if settings.get('dashing-url') == '':
		raise Exception(u'Please specify dashing-url in settings file')

	if settings.get('dashing-auth-token') == '':
		raise Exception(u'Please specify dashing-auth-token in settings file')

	dashboard_name = settings.get('worker-name')

	# Initialize history object
	try:
		history_file = open(history_file_path)
		history = json.load(history_file)
		history_file.close()
	except IOError:
		pass

       if check_cpuminer():
                summary = get_cpuminer_summary()

                accepted = summary['pools'][0]['stats'][0]['accepted']
                rejected = summary['pools'][0]['stats'][0]['rejected']
                start_time = summary['pools'][0]['stats'][0]['start_time']

                elapsed = int(time.time()) - int(start_time)

                #WIP will need to loop for hash / errors
                #WIP will need to loop for pool
                #WIP Pool difficulty
                #WIP Pool
                hash = 0
                errors = 0
                pool = "Inactive"
                pool_difficulty = "N/A"
        else:
                summary = get_minerd_summary()
                hash = summary['SUMMARY'][0]['MHS 5s']
                accepted = summary['SUMMARY'][0]['Accepted']
                rejected = summary['SUMMARY'][0]['Rejected']
                errors = summary['SUMMARY'][0]['Hardware Errors']
                elapsed = summary['SUMMARY'][0]['Elapsed']

                pool_summary = get_minerd_pool_summary()

                for num in range(0, int(pool_summary['STATUS'][0]['Msg'].split()[0])-1):
                        if pool_summary['POOLS'][num]['Stratum Active']:
                                pool = pool_summary['POOLS'][num]['URL']
                                pool_difficulty = pool_summary['POOLS'][num]['Last Share Difficulty']

                        if pool == "":
                                pool = "Inactive"
                                pool_difficulty = "N/A"

        update_graph_widget(dashboard_name, 'hash', float(convert_hash(hash)))
        update_number_widget(dashboard_name, 'accepted', accepted)
        
        update_number_widget(dashboard_name, 'rejected', rejected)
        update_number_widget(dashboard_name, 'errors', errors)

        elapsed = str(datetime.timedelta(seconds=int(elapsed)))
        update_text_widget(dashboard_name, 'elapsed', elapsed)

        update_temperature_widget(dashboard_name, 'temperature', get_temperature())
        update_text_widget(dashboard_name, 'pool', pool)
        update_number_widget(dashboard_name, 'pool_difficulty', pool_difficulty)
        
	# Save history object
	with open(history_file_path, 'w+') as history_file:
		json.dump(history, history_file)
