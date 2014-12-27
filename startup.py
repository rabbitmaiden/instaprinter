#!/usr/bin/python

import subprocess
import re
import sys
import requests
import os
from termcolor import colored



os = subprocess.check_output(['uname'])
rpi = os == 'Linux'


if rpi:
    print "Hello from the Raspberry Pi"
else:
    print colored("Hello from a mac laptop", "green")
    print colored("Set this up for yourself", "red")
    sys.exit(1)
    

print colored("Do we have an IP address?", 'green')
ip = subprocess.check_output(['hostname', '-I']);
if not re.search(r'[\d]+\.[\d]+\.[\d]+\.[\d]+', ip):
    print colored("No ip address, please fix and restart", 'red')
    sys.exit(1)

print colored("We do! Now checking for internet connectivity", 'green')
r = requests.get('http://www.google.com/')
if r.status_code != 200:
    print colored("Could not connect to the internet, please fix and restart", 'red')
    sys.exit(1)

print colored("Okay we have internet, trying to update our codebase", 'green')

git = subprocess.call(["git", "pull", "origin", "master"])
if git != 0:
    print colored("Could not update codebase, please fix and restart", 'red')
    sys.exit(1)

print colored("Okay we updated the codebase!", 'green')
