import Constant as const
import Tracker as tracker
import Configuration as config
import Menu as m
import sys
import Login as logi

####### VARIABILI 

T = False
sessionID = ""

host = ""
t_host = ["", const.TPORT]

####### INIZIALIZZAZIONE
T, host, t_host = config.readArgs(sys.argv)

####### DEMONE TRACKER
if T:
	daemonThreadT = tracker.TrackerDaemon(host)
	daemonThreadT.setName("DAEMON T")
	daemonThreadT.setDaemon(True)
	daemonThreadT.start()

	logi.try_connection(host)

####### MENU
m.menu(host, T, t_host)