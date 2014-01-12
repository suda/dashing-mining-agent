Dashing mining agent
====================

Agent reporting current cgminer status and GPU temperature to [Dashing mining dashboard](https://github.com/suda/dashing-mining-dashboard).

Requirements
============

* Linux (for now)
* Python 2.7 or newer
* ATI GPU with working drivers
* cgminer with enabled API

Setup
=====

Setup this agent on every worker you want to monitor.

* Start cgminer with API enabled by adding `--api-listen --api-allow=127.0.0.1` to its command line
* Clone repository: `git clone https://github.com/suda/dashing-mining-agent.git`
* Enter directory: `cd dashing-mining-agent`
* Install requirements: `pip install -r requirements.txt`
* Create `local_settings.json` file based on `settings.json` file:
  * Set `dashing-url` to your Heroku app url
  * Set `dashing-auth-token` to token you've set when setting up dashing-mining-dashboard
  * Set `worker-name` array with your worker name
* Test if agent works: `python agent.py` (if there's an error about X server not being active, execute: `export DISPLAY=:0`)
* Edit crontab to send events every minute: `* * * * *  export DISPLAY=:0;/usr/bin/python /repo_path/dashing-mining-agent/agent.py`

If you have any problems with setting up this agent, [create new issue](https://github.com/suda/dashing-mining-agent/issues/new) and I'll try to help.

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
