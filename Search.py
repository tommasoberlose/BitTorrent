import TextFunc as tfunc
import Constant as const
import Package as pack
import SocketFunc as sfunc
import Download as dnl
import string

# MACROFUNZIONE DI SISTEMA

def search(sessionID, ip55, ipTracker55):

	tfunc.warning("\n>>> SEARCH")
	query = input("\nInserisci il nome del file da cercare: ")
	while(len(query) > const.LENGTH_QUERY):
		tfunc.error("Siamo spiacenti ma accettiamo massimo 20 caratteri.")
		query = input("\nInserisci il nome del file da cercare: ")

	# Fase 1
	ricevutoByte = b''
	pk = pack.request_search(sessionID, query)
	s = sfunc.create_socket_client(func.roll_the_dice(ipTracker55), const.TPORT);
	if s is None:
		tfunc.error("Tracker non attivo.")
	else:
		s.sendall(pk)

		ricevutoByte = s.recv(4 * const.LENGTH_PACK)

		if str(ricevutoByte[0:4],"ascii") == pack.CODE_ANSWER_LOOK:
			nIdmd5 = int(ricevutoByte[4:7])
			if(nIdmd5 != 0):
				tfunc.success("Ricerca completata.")
				pointer = 7
				id = 0
				listFile = []
				for j in range(0, nIdmd5):
					md5 = ricevutoByte[pointer:pointer + 32]
					nomeFile = ricevutoByte[pointer + 32:pointer + 132]
					lenFile = ricevutoByte[pointer + 132:pointer + 142]
					lenPart = ricevutoByte[pointer + 142:pointer + 148]
					id = id + 1
					fixList = [id, md5, nomeFile, lenFile, lenPart]
					listFile.append(fixList)

					pointer = pointer + 148
						
				print("\nScegli file da quelli disponibili (0 per uscire): \n")
				print("FILE    \t\tID\tDimensione del file\n")
				for row in listFile:
					nomeFile = tfunc.reverse_format_string((str(row[2], "ascii").strip() + ":"), const.LENGTH_FORMAT, " ")
					print(nomeFile + str(row[0]) + "\t" + str(int(row[3])))
				
				selectId = input("\nInserire il numero di file che vuoi scaricare (0 per uscire): ")
				
				if(selectId != "0"):
					for i in range (0, id):
						if listFile[i][0] == int(selectId):
							selectFile = listFile[i]
							break

					# FASE 2 dnl.download(selectFile)

			else:
				func.error("Non sono presenti file con questa query nel nome: " + query)
		s.close()

# Da in uscita la lista degli md5 
def search_in_list_file(listFile, query):
	# Da fare
	return []