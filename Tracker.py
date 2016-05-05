import socket
import Constant as const
import Function as func
import Package as pack
import TextFunc as tfunc
import SocketFunc as sfunc
import FileStruct as fs
from threading import *
import Logout as logo
import Login as logi
import Search as search

class TrackerDaemon(Thread):

	# Inizializza il thread, prende in ingresso l'istanza e un valore su cui ciclare
	# Tutti i metodi di una classe prendono l'istanza come prima variabile in ingresso
	# __init__ è un metodo predefinito per creare il costruttore
	def __init__(self, host):
		# Costruttore
		Thread.__init__(self)
		self.host = host
		self.port = const.TPORT
		self.listUsers = {}
		self.listFile = {}

	def run(self):
		# Creazione socket
		s = sfunc.create_socket_server(func.roll_the_dice(self.host), self.port)

		if s is None:
			tfunc.write_daemon_text(self.name, self.host, 'Error: Daemon could not open socket in upload.')

		else:
			while 1: #auuauaau

				conn, addr = s.accept()
				ricevutoByte = conn.recv(const.LENGTH_PACK)
				#print("\n")
				#tfunc.write_daemon_text(self.name, addr[0], str(ricevutoByte, "ascii"))


				if not ricevutoByte:
					tfunc.write_daemon_error(self.name, addr[0], "Pacchetto errato")
				elif (str(ricevutoByte[0:4], "ascii") == pack.CODE_CLOSE):
					break
				elif (str(ricevutoByte[0:4], "ascii") == pack.CODE_CONF):
					tfunc.write_daemon_error(self.name, addr[0], "Avvio demone Tracker")
				else:
					if str(ricevutoByte[0:4], "ascii") == pack.CODE_LOGIN: ### LOGIN
						pk = logi.reconnect_user(ricevutoByte[4:59], ricevutoByte[59:], self.listUsers)
						self.listUsers[pk[4:]] = [ricevutoByte[4:59], ricevutoByte[59:]]
						conn.sendall(pk)

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_ADDFILE:
						# Controllo presenza user
						if ricevutoByte[4:20] in self.listUsers:
							# Funzione che crea listPart tutta di 1
							fileToAdd = fs.FileStruct(ricevutoByte[36:136], ricevutoByte[20:30], ricevutoByte[30:36], ricevutoByte[4:20])
							fileToAdd.add_owner_total()
							self.listFile[ricevutoByte[-32:]] = fileToAdd 
							tfunc.write_daemon_success(self.name, addr[0], "ADD FILE " + str(ricevutoByte[36:136], "ascii").strip())
							pk = pack.answer_add_file(fileToAdd.nPart)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "ADD FILE - User not logged")

					elif(str(ricevutoByte[0:4], "ascii") == pack.CODE_LOOK): ### Richiesta di ricerca file da un peer
						# Controllo logon user
						if ricevutoByte[4:20] in self.listUsers:
							listMd5 = search.search_in_list_file(self.listFile, ricevutoByte[20:])
							if len(listMd5) == 0:
								tfunc.write_daemon_error(self.name, addr[0], "SEARCH FILE - Non è stato trovato nessun file con " + str(ricevutoByte[20:], "ascii") + " nel nome.")
							pk = pack.answer_look(listMd5, self.listFile)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "SEARCH FILE - User not logged")
						"""
						del listResultQuery[:]
						tfunc.write_daemon_text(self.name, addr[0], "INIZIO RICERCA DI: " + str(ricevutoByte[20:], "ascii").strip())
						pk = pack.query(self.host, ricevutoByte[20:])
						func.add_pktid(pk[4:20], self.listPkt, self.port)

						for x in self.sn_network:
							sNet = func.create_socket_client(func.roll_the_dice(x[0]), x[1])
							if sNet != None:
								sNet.sendall(pk)
								sNet.close()

						listaRisultatiDellaQuery = []
						listaRisultatiDellaQuery = func.search_file(bytes(str(ricevutoByte[20:],"ascii").strip(),"ascii"), self.listFiles, self.listUsers)
						for x in listaRisultatiDellaQuery:
							listResultQuery.append(x)


						#func.send_afin(conn, self.listResultQuery)

						daemonAfin = threading.Thread(target=sendAfin, args=(conn, ))
						daemonAfin.start()

						#t = Timer(int(const.MAX_TIME / 1000), func.send_afin, (conn, self.listResultQuery))
						"""

					elif(str(ricevutoByte[0:4], "ascii") == pack.CODE_FIND_PART): ### Richiesta conoscenza possesso parti del file cercato nella rete 
						print("Blabla")

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_UPDATE_PART: ### Aggiornamento parti scaricate
						# Controllo presenza user
						if ricevutoByte[4:20] in self.listUsers:
							nPart = update_memory(ricevutoByte[4:20], ricevutoByte[20:52], ricevutoByte[52:], self.listFile)
							pk = pack.answer_update_tracker(nPart)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "ADD FILE - User not logged")

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_LOGOUT: ### LOGOUT
						if ricevutoByte[4:] in self.listUsers:
							nPart = logo.try_logout(ricevutoByte[4:])
							if nPart != 0:
								conn.sendall(pack.reject_logout(fs.get_part_from_string(fs.get_part_by_sessionID(ricevutoByte[4:])) - nPart))
							else:
								conn.sendall(pack.answer_logout(nPart))
						else:
							tfunc.write_daemon_error(self.name, addr[0], "User not logged")
						"""
						i = 0
						for user in self.listUsers:
							if ricevutoByte[4:] == user[2]:
								del user

						nDelete = 0
						for file in self.listFiles:
							if ricevutoByte[4:] == file[2]:
								del self.listFiles[i]
								nDelete += 1
								i -= 1
							i += 1
						pk = pack.answer_logout(nDelete)
						conn.sendall(pk)
						tfunc.write_daemon_success(self.name, addr[0], "LOGOUT OK")
						"""

					else:
						tfunc.write_daemon_error(self.name, addr[0], "Ricevuto pacchetto sbagliato: " + str(ricevutoByte, "ascii"))
			s.close()
			
