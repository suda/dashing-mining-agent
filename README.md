Dashing mining agent
====================

Agent reporting current cgminer status and GPU/CPU temperature to [Dashing mining dashboard](https://github.com/suda/dashing-mining-dashboard).

Requirements
============

* Linux or Windows
* Python 2.7 or newer
* cgminer with enabled API

Temperature Module - Supported Devices
============

* ATI GPU with working drivers
* Raspberry PI

Setup on Windows
================

Setup this agent on every worker you want to monitor.

* Start cgminer with API enabled by adding `--api-listen --api-allow=127.0.0.1` to your batch file
* Install [Python and pip](http://www.aaronstannard.com/post/2012/08/17/How-to-Setup-a-Proper-Python-Environment-on-Windows.aspx)
* Download [latest repository](https://github.com/suda/dashing-mining-agent/archive/master.zip) and unpack it's contents
* Open Command Line and enter repository's directory
* Install requirements: `pip.exe install -r requirements.txt`
* Create `local_settings.json` file based on `settings.json` file:
  * Set `dashing-url` to your Heroku app url
  * Set `dashing-auth-token` to token you've set when setting up dashing-mining-dashboard
  * Set `worker-name` array with your worker name
* Test if agent works: `python.exe agent.py`
* Create batch file `agent.bat` containing full path to python and `agent.py` file (i.e. `C:\Python27\python.exe C:\Users\miner\Desktop\dashing-mining-agent\agent.py`)
* Start this batch file every minute: `schtasks /create /tn dashing-mining-agent /sc MINUTE /tr C:\Users\miner\Desktop\dashing-mining-agent\agent.bat`

Setup on Linux
==============

Setup this agent on every worker you want to monitor.

* Start cgminer with API enabled by adding `--api-listen --api-allow=127.0.0.1` to its command line
* Install pre-requisites: `sudo apt-get install python-dev git python-pip`
* Enter directory: `cd /opt`
* Clone repository: `sudo git clone https://github.com/suda/dashing-mining-agent.git`
* Enter directory: `cd dashing-mining-agent`
* Install requirements: `sudo pip install -r requirements.txt`
* Create `local_settings.json` file based on `settings.json` file: (`sudo cp settings.json local_settings.json`)
  * Set `dashing-url` to your Heroku app url
  * Set `dashing-auth-token` to token you've set when setting up dashing-mining-dashboard
  * Set `worker-name` array with your worker name
* Test if agent works: `sudo python agent.py` (if there's an error about X server not being active, execute: `export DISPLAY=:0`, sometimes it's also needed to run this with `sudo`)
* Edit crontab (`sudo crontab -e`) to send events every minute:
* `* * * * *  export DISPLAY=:0;/usr/bin/python /opt/dashing-mining-agent/agent.py`
* If you want the dashboard to update every 30 seconds, add the line below, in addition to the line above:
* `* * * * *  sleep 30; export DISPLAY=:0;/usr/bin/python /opt/dashing-mining-agent/agent.py`

Support
=======

If you have any problems with setting up this agent, [create new issue](https://github.com/suda/dashing-mining-agent/issues/new) and I'll try to help.

Settings file
=============

`settings.json` / `local_settings.json` fields:

* `worker-name` - Name of dashbord in DMD
* `dashing-url` - URL for your Dashing instance (with trailing slash and http:// prefix)
* `dashing-auth-token` - Auth token set in config.ru file of your Dashing
* `minerd-address` - Minerd listen address specified by --api-listen parameter
* `minerd-port` - Minerd listen port specified by --api-port parameter
* `temperature-units` - Displays temperature in either Celsius (default) or Fahrenheit

Donations
========

Any donations are welcome and should result in more features in less time :)

BTC address: `1AAkZXsn9c2EWWbo7yzDEgMz1b3wMBN52Q`

LTC address: `LehFD6SvT3PfE4gBbrQwhXdrmFWwdrFxrU`

Author
======

Wojtek Siudzinski - [@suda](https://twitter.com/suda)

License
=======

Distributed under the [MIT license](https://github.com/suda/dashing-mining-agent/blob/master/LICENSE)
