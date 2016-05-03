import TextFunc as tfunc

def readArguments(argv):

	for i in range(len(argv)):

		if argv[i] == "-t":
			T = True

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

		elif argv[i] == "-p":
			try:
				const.PORT = argv[i + 1]
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		elif argv[i] == "-pSN":
			try:
				const.PORT_SN = argv[i + 1]
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		elif argv[i] == "-t":
			try:
				const.MAX_TIME = int(argv[i + 1]) * 1000
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		elif argv[i] == "-ttl":
			try:
				const.TTL = argv[i + 1]
			except:
				tfunc.error("Errore inserimento dati")
				writeHelp()

		elif argv[i] == "-h":
			writeHelp()
		return [T]


def writeHelp():
	func.warning("\nPOSSIBILI ARGOMENTI:")
	print("Super Nodo\t-sn")
	print("Set Default Ip\t-ip group identifier")
	print("Change Port\t-p port")
	print("Change Port SN\t-pSN port")
	print("Change time\t-t time")
	print("Change ttl\t-ttl ttl")
	print("")
	sys.exit(-1)