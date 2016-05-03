import TextFunc as tfunc
import Constant as const
import sys

# FUNZIONI

def readArgs(argv):

	T = False
	host = ""

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

		# HELP
		elif argv[i] == "-h":
			writeHelp()
	
	# Return della lista della configurazione scelta
	return [T, host]


def writeHelp():
	func.warning("\nPOSSIBILI ARGOMENTI:")
	print("Tracker\t-t")
	print("Set Default Ip\t-ip group identifier")
	print("Change Port\t-p port")
	print("")
	sys.exit(-1)

# TEST
"""
[T, host] = readArgs(sys.argv)
print(T)
print(host)

"""