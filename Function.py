import string
import random
import socket
import shutil
import os
import sys
import hashlib
import time
import Constant as const
import Function as func
import Package as pack

import Libraries

# Random Functions
def random_string(length):
   return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length))

###### IP

def roll_the_dice(ip):
	return ip[16:55]
	#return random.choice([ip[0:15], ip[16:55]])

def get_ipv4(ip):
	return ip[0:15]

def get_ipv6(ip):
	return ip[16:55]
	
def progress():
	print("|||", end = "")


# TEST
"""
print("Random: " + random_string(const.LENGTH_SESSIONID))
print("Roll the dice: " + roll_the_dice("172:030:001:002|fc00:0000:0000:0000:0000:0000:0001:0002"))
"""