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
t_host = ["", const.TPORT]

####### INIZIALIZZAZIONE
[T, host] = config.readArgs(sys.argv)

if T:
	tfunc.warning("\nP2P >> INIZIALIZZAZIONE COME TRACKER")
else:
	tfunc.warning("\nP2P >> INIZIALIZZAZIONE COME PEER")



####### DEMONI
if T:
	daemonThreadT = daemon.PeerDaemon(host)
	daemonThreadT.setName("DAEMON T")
	daemonThreadT.start()


m.menu(host, T, t_host)