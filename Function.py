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

# Random Functions
def random_pktid(length):
   return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length))

def random_sessionID(length):
   return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length))

###### IP

def roll_the_dice(ip):
	return ip[16:55]
	#return random.choice([ip[0:15], ip[16:55]])

def get_ipv4(ip):
	return ip[0:15]

def get_ipv6(ip):
	return ip[16:55]


###### SEARCH FILE

def search_file(query, listFiles, listUsers): 
	listResultQuery = []
	for f in listFiles:
		if query in f[1]:
			for i in listUsers:
				if i[2] == f[2]:
					listResultQuery.append([f[0], bytes(func.format_string(str(f[1],"ascii"), const.LENGTH_FILENAME, " "),"ascii"), i[0], i[1]])
					break
	return listResultQuery


def add_pktid(pktid, list_pkt, port):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if (pktid == lista[0]):# and (port == lista[2]):
			return False
	pkTime = time.time() * 1000
	add_list = [pktid, pkTime, port]
	list_pkt.append(add_list)
	return True

def clear_pktid(list_pkt):
	x = 0
	for i in list_pkt:
		pkTime = i[1]
		nowtime = time.time() * 1000
		diff = nowtime - pkTime
		if diff >= const.MAX_TIME:
			del list_pkt[x]
			x -= 1
		x += 1
	return list_pkt

def check_query(pktid, list_pkt, port):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if (pktid == lista[0]):# and (port == lista[2]):
			return True
	return False

def check_sn(pktid, list_pkt):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if pktid == lista[0]:
			return True
	return False

def remove_pktid(pktid, list_pkt):
	i = 0
	for lista in list_pkt:
		if pktid == lista[0]:
			del list_pkt[i]
			i -= 1
		i += 1

