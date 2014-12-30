#!/usr/bin/python
import subprocess
import re
import sys
import requests
import os
from termcolor import colored
import pprint


#just in case
os.chdir('/home/pi/instaprinter')

uname = subprocess.check_output(['uname']).strip()
rpi = (uname == 'Linux')
if rpi:
    print (colored("Hello from the Raspberry Pi!!", "yellow"))
else:
    print (colored("Hello from a mac laptop", "yellow"))
    print (colored("Set this up for yourself", "red"))
    sys.exit(1)
    

sys.stdout.write(colored("Do we have an IP address? ", 'green'))
ip = subprocess.check_output(['hostname', '-I']);
if not re.search(r'[\d]+\.[\d]+\.[\d]+\.[\d]+', ip):
    print (colored("\nNo ip address, please fix and restart", 'red'))
    sys.exit(1)

sys.stdout.write(colored("Yes!\n", "cyan"))
sys.stdout.write(colored("Do we have internet connectivity? ", 'green'))

r = requests.get('http://www.google.com/')
if r.status_code != 200:
    print (colored("\nCould not connect to the internet", 'red'))
    sys.exit(1)

sys.stdout.write(colored("Yes!\n", "cyan"))
sys.stdout.write(colored("Updating codebase: ", 'green'))

git = subprocess.call(["git", "pull", "origin", "master"])
if git != 0:
    print (colored("\nCould not update codebase", 'red'))
    sys.exit(1)

sys.stdout.write(colored("Success!\n", 'cyan'))
sys.stdout.write(colored("Do we have a printer? ", "green"))

lpinfo = subprocess.check_output(['lpinfo', '--include-schemes', 'usb', '-v'])
if lpinfo == '':
    print (colored("\nCould not find the printer", 'red'))
    sys.exit(1)

sys.stdout.write(colored("Yes!\n", "cyan"))

tag = open('tag.txt').read().strip();

print (colored("The current tag is:", "green") + colored(" "+tag, "yellow"))

#answer = raw_input(colored("Start the printer? [y/n]: ", "magenta"))
#if answer == 'y' or answer == 'Y':
if True:
  subprocess.call(["./fetch.py"])
