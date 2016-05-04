import Constant as const
import Daemon as daemon
import Configuration as config
import Menu as m
import sys

####### VARIABILI 

T = False
sessionID = ""

host = ""
t_host = ["", const.TPORT]

####### INIZIALIZZAZIONE
[T, host] = config.readArgs(sys.argv)

####### DEMONE TRACKER
if T:
	daemonThreadT = daemon.TrackerDaemon(host)
	daemonThreadT.setName("DAEMON T")
	daemonThreadT.start()

####### MENU
m.menu(host, T, t_host)