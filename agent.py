import requests
import json
import memcache
import socket
import json
import datetime
import re
from subprocess import check_output

try:
	import settings
except ImportError:
	raise Exception(u'Missing settings.py file')

mc = memcache.Client(settings.MEMCACHED)

def update_number_widget(widget, value):
	widget = settings.DASHBOARD_NAME + '_' + widget
	old_value = mc.get(settings.MEMCACHED_PREFIX + widget)
	payload = {
		'auth_token': settings.DASHING_AUTH_TOKEN,
		'current': value
	}

	if old_value is not None:		
		payload.update({'last': old_value})

	requests.post(settings.DASHING_URL + 'widgets/' + widget, data=json.dumps(payload))
	mc.set(settings.MEMCACHED_PREFIX + widget, value, 0)

def update_graph_widget(widget, value):
	widget = settings.DASHBOARD_NAME + '_' + widget
	points = mc.get(settings.MEMCACHED_PREFIX + widget)
	payload = {
		'auth_token': settings.DASHING_AUTH_TOKEN		
	}

	if points is None:		
		points = []

	last_x = 1
	for point in points:
		last_x = max(last_x, point['x'])

	points.append({ 'x': last_x + 1, 'y': value})
	points = points[-10:]
	payload.update({'points': points})

	requests.post(settings.DASHING_URL + 'widgets/' + widget, data=json.dumps(payload))
	mc.set(settings.MEMCACHED_PREFIX + widget, points, 0)

def update_text_widget(widget, text):
	widget = settings.DASHBOARD_NAME + '_' + widget
	payload = {
		'auth_token': settings.DASHING_AUTH_TOKEN,
		'text': text
	}

	requests.post(settings.DASHING_URL + 'widgets/' + widget, data=json.dumps(payload))

def get_minerd_summary():
	minerd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	minerd_socket.connect((settings.MINERD_ADDRESS, settings.MINERD_PORT))
	minerd_socket.sendall('{"command":"summary"}')
	received_data = minerd_socket.recv(4096)
	summary = json.loads(received_data[:-1])

	return summary

def get_gpu_temperature():
	output = check_output(['/usr/bin/aticonfig', '--odgt'])
	matches = re.search("([0-9]+\.[0-9]+)", output)

	return float(matches.group(1))

if __name__ == '__main__':
	summary = get_minerd_summary()
	update_graph_widget('khs', float(summary['SUMMARY'][0]['MHS 5s']) * 1000)
	update_number_widget('accepted', summary['SUMMARY'][0]['Accepted'])
	update_number_widget('rejected', summary['SUMMARY'][0]['Rejected'])
	update_number_widget('errors', summary['SUMMARY'][0]['Hardware Errors'])	
	elapsed = str(datetime.timedelta(seconds=int(summary['SUMMARY'][0]['Elapsed'])))
	update_text_widget('elapsed', elapsed)
	update_graph_widget('temperature', get_gpu_temperature())	

