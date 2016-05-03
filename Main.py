import Function as func
import Constant as const
import Daemon as daemon
import Configuration as config
import TextFunc as tfunc
import Menu as m
import sys

####### VARIABILI 

T = False
sessionID = ""

host = ""

####### INIZIALIZZAZIONE
[T, host] = config.readArgs(sys.argv)

if T:
	tfunc.warning("\nP2P >> INIZIALIZZAZIONE COME TRACKER")
else:
	tfunc.warning("\nP2P >> INIZIALIZZAZIONE COME PEER")



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