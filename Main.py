import Function as func
import Constant as const
import Package as pack
import Daemon as daemon
import Configuration as config
import Menu as m
import os
import sys
import time
import hashlib

####### VARIABILI 

T = False
sessionID = ""

host = ""

####### INIZIALIZZAZIONE
[T, host] = config.readArgs(sys.argv)

if T:
	func.warning("\nP2P >> INIZIALIZZAZIONE COME TRACKER")
else:
	func.warning("\nP2P >> INIZIALIZZAZIONE COME PEER")



####### DEMONI
"""
if T:
	daemonThreadT = daemon.Daemon(host, True, sn_network, listPkt, listUsers, listFiles, True)
	daemonThreadT.setName("DAEMON T")
	daemonThreadT.start()

	daemonThreadP = daemon.Daemon(host, True, sn_network, listPkt, listUsers, listFiles, False)
	daemonThreadP.setName("DAEMON PEER")
	daemonThreadP.start()

else:
	daemonThreadP = daemon.Daemon(host, False, sn_network, listPkt, listUsers, listFiles, False)
	daemonThreadP.setName("DAEMON PEER")
	daemonThreadP.start()	
"""

m.menu()