# GuestBook

guestbook is a simple server written in python witch interfaces with a google sheet as datastorage.


# setup

0. create a virtual environment (`python -m venv venv`) (don't forget to activate it)
1. install deps (`pip install -r requirements.txt`)
2. copy the config from `example.config.py` to `config.py`
3. setup the google sheet ID
4. create a service account on Google API Console
5. add the service account's email to your google sheet
6. paste the service account's json into the config.py 

