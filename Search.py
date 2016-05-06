import TextFunc as tfunc
import Constant as const
import Package as pack
import SocketFunc as sfunc
import Download as dnl
import string
import Function as func
import FileStruct as fs

# MACROFUNZIONE DI SISTEMA
# >> PEER
def search(sessionID, host, t_host, listPartOwned):

	tfunc.warning("\n>>> SEARCH")
	query = input("\nInserisci il nome del file da cercare: ")
	while(len(query) > const.LENGTH_QUERY):
		tfunc.error("Siamo spiacenti ma accettiamo massimo 20 caratteri.")
		query = input("\nInserisci il nome del file da cercare: ")

	# Fase 1
	ricevutoByte = b''
	pk = pack.request_look(sessionID, query)
	s = sfunc.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1]);
	if s is None:
		tfunc.error("Tracker non attivo.")
	else:
		s.sendall(pk)

		ricevutoByte = s.recv(4 * const.LENGTH_PACK)

		if str(ricevutoByte[0:4], "ascii") == pack.CODE_ANSWER_LOOK:
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
				
				if selectId != "0" :
					for i in range (0, id):
						if listFile[i][0] == int(selectId):
							selectFile = listFile[i]
							break

					# FASE 2 

					print ("\n>>> DOWNLOAD")
					dnl.download(host, t_host, selectFile, sessionID, listPartOwned)

			else:
				tfunc.error("Non sono presenti file con questa query nel nome: " + query)
		s.close()

# Da in uscita la lista degli md5 
# >> TRACKER
def search_in_list_file(listFile, sessionID, query, name, addr):
	listFounded = fs.find_file_from_string(listFile, sessionID, query)
	if len(listFounded) == 0:
		tfunc.write_daemon_error(name, addr[0], "SEARCH FILE - Nessun file con " + str(query, "ascii").strip() + " nel nome.")
	pk = pack.answer_look(listFounded)
	return pk


# >> TRACKER
def find_hitpeer(listFile, listUsers, sessionID, md5, name, addr):
	listFounded = fs.find_hitpeer_from_md5(listFile, listUsers, sessionID, md5)
	if len(listFounded) == 0:
		tfunc.write_daemon_error(name, addr[0], "REQUEST FILEPART - Nessun file con md5: " + str(md5, "ascii"))
	pk = pack.answer_hitpeer(listFounded)
	return pk
