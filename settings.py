# List of boards/cgminer/GPU instances.
DASHBOARDS = {
	'default': {
		# Minerd listen address specified by --api-listen parameter
		'MINERD_ADDRESS': '127.0.0.1',
		# Minerd listen port specified by --api-port parameter
		'MINERD_PORT': 4028,
		# Which GPU temperature sensor to check
		'GPU_SENSOR_NUMBER': 0
	}
}

# URL for your Dashing instance (with trailing slash)
DASHING_URL = ''
# Auth token set in config.ru file of your Dashing
DASHING_AUTH_TOKEN = ''

# Memcached used for storing historical data
MEMCACHED = ['127.0.0.1:11211']
# Prefix for keys
MEMCACHED_PREFIX = ''

try:
    from local_settings import *
except ImportError:
    pass