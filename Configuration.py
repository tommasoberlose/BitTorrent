import TextFunc as tfunc
import Constant as const
import sys

# FUNZIONI

def readArgs(argv):

	T = False
	host = ""
	t_host = ["", const.TPORT]

	for i in range(len(argv)):

		# TRACKER
		if argv[i] == "-t":
			T = True

		# IP
		elif argv[i] == "-ip":
			try:
				nGroup = argv[i + 1]
				nElement = argv[i + 2]
			
				host = ("172.030." + tfunc.format_string(nGroup, const.LENGTH_SECTION_IPV4, "0") + 
							"." + tfunc.format_string(nElement, const.LENGTH_SECTION_IPV4, "0") + 
							"|fc00:0000:0000:0000:0000:0000:" + tfunc.format_string(nGroup, const.LENGTH_SECTION_IPV6, "0") + 
							":" + tfunc.format_string(nElement, const.LENGTH_SECTION_IPV6, "0"))
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		# PORT
		elif argv[i] == "-p":
			try:
				const.PORT = argv[i + 1]
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		# IP TRACKER
		elif argv[i] == "-ipt":
			try:
				nGroupT = argv[i + 1]
				nElementT = argv[i + 2]
			
				t_host = [("172.030." + tfunc.format_string(nGroupT, const.LENGTH_SECTION_IPV4, "0") + 
							"." + tfunc.format_string(nElementT, const.LENGTH_SECTION_IPV4, "0") + 
							"|fc00:0000:0000:0000:0000:0000:" + tfunc.format_string(nGroupT, const.LENGTH_SECTION_IPV6, "0") + 
							":" + tfunc.format_string(nElementT, const.LENGTH_SECTION_IPV6, "0")), const.TPORT]
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		# TIME TO UPDATE
		elif argv[i] == "-ttu":
			try:
				const.TIME_TO_UPDATE = int(argv[i + 1])
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		# TIME TO UPDATE
		elif argv[i] == "-mr":
			try:
				const.MAX_RESULT = int(argv[i + 1])
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()
		

		# HELP
		elif argv[i] == "-h":
			writeHelp()
	

	if host == "":
		nGroup = input("Inserire il numero del gruppo: ")
		nElement = input("Inserire il numero dell'elemento del gruppo: ")
		host = ("172.030." + func.format_string(nGroup, const.LENGTH_SECTION_IPV4, "0") + 
						"." + func.format_string(nElement, const.LENGTH_SECTION_IPV4, "0") + 
						"|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, const.LENGTH_SECTION_IPV6, "0") + 
						":" + func.format_string(nElement, const.LENGTH_SECTION_IPV6, "0"))
	tfunc.gtext("IP: " + host)
	if t_host[0] != 0:
		tfunc.gtext("IP TRACKER: " + t_host[0])

	if T:
		tfunc.warning("\nP2P >> INIZIALIZZAZIONE COME TRACKER")
	else:
		tfunc.warning("\nP2P >> INIZIALIZZAZIONE COME PEER")

	# Return della lista della configurazione scelta
	return T, host, t_host


def writeHelp():
	tfunc.warning("\nPOSSIBILI ARGOMENTI:")
	print("Tracker\t-t")
	print("Set Default Ip\t-ip group identifier")
	print("Set Default Tracker Ip\t-ipt group identifier")
	print("Change Port\t-p port")
	print("Change Time To Update\t-ttu seconds")
	print("Change Max Results/ttu\t-ms #result")
	print("")
	sys.exit(-1)
