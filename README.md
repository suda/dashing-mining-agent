Dashing mining agent
====================

Agent reporting current cgminer status and GPU temperature to [Dashing mining dashboard](https://github.com/suda/dashing-mining-dashboard).

Requirements
============

* Linux (for now)
* Python 2.7 or newer
* memcached server
* ATI GPU with working drivers
* cgminer with enabled API

Setup
=====

* Clone repository: `git clone https://github.com/suda/dashing-mining-agent.git`
* Enter directory: `cd dashing-mining-agent`
* Install requirements: `pip install -r requirements.txt`
* Create `local_settings.py` file based on `settings.py` file
* Start cgminer with API enabled by adding `--api-listen --api-allow=127.0.0.1` flags
* Edit crontab to send events every minute: `* * * * *  export DISPLAY=:0;/usr/bin/python /repo_path/dashing-mining-agent/agent.py`

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
