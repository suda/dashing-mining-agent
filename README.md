Dashing mining agent
====================

Agent reporting current cgminer status and GPU temperature to [Dashing mining dashboard](https://github.com/suda/dashing-mining-dashboard).

Requirements
============

* Linux (for now)
* Python 2.7 or newer
* memcached server
* ATI GPU with working drivers

Setup
=====

* Clone repository: `git clone https://github.com/suda/dashing-mining-agent.git`
* Enter directory: `cd dashing-mining-agent`
* Install requirements: `pip install -r requirements.txt`
* Create `local_settings.py` file based on `settings.py` file
* Edit crontab to send events every minute: `* * * * *  export DISPLAY=:0;/usr/bin/python /repo_path/dashing-mining-agent/agent.py`
