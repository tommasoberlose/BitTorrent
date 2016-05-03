import TextFunction as tfunc
import Constant as const
import Package as pack
import SocketFunc as sfunc
import Download as dnl

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

# FUNZIONI

def search_file(query, listFiles, listUsers): 
	listResultQuery = []
	for f in listFiles:
		if query in f[1]:
			for i in listUsers:
				if i[2] == f[2]:
					listResultQuery.append([f[0], bytes(tfunc.format_string(str(f[1],"ascii"), const.LENGTH_FILENAME, " "),"ascii"), i[0], i[1]])
					break
	return listResultQuery


def add_pktid(pktid, list_pkt, port):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if (pktid == lista[0]):# and (port == lista[2]):
			return False
	pkTime = time.time() * 1000
	add_list = [pktid, pkTime, port]
	list_pkt.append(add_list)
	return True

def clear_pktid(list_pkt):
	x = 0
	for i in list_pkt:
		pkTime = i[1]
		nowtime = time.time() * 1000
		diff = nowtime - pkTime
		if diff >= const.MAX_TIME:
			del list_pkt[x]
			x -= 1
		x += 1
	return list_pkt

def check_query(pktid, list_pkt, port):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if (pktid == lista[0]):# and (port == lista[2]):
			return True
	return False

def remove_pktid(pktid, list_pkt):
	i = 0
	for lista in list_pkt:
		if pktid == lista[0]:
			del list_pkt[i]
			i -= 1
		i += 1


