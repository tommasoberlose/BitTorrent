import socket
import Constant as const
import Function as func
import Package as pack
import TextFunc as tfunc
import SocketFunc as sfunc
import FileStruct as fs

class TrackerDaemon(Thread):

	# Inizializza il thread, prende in ingresso l'istanza e un valore su cui ciclare
	# Tutti i metodi di una classe prendono l'istanza come prima variabile in ingresso
	# __init__ è un metodo predefinito per creare il costruttore
	def __init__(self, host):
		# Costruttore
		Thread.__init__(self)
		self.host = host
		self.port = const.TPORT
		self.listFile = {}

	def run(self):
		# Creazione socket
		s = sfunc.create_socket_server(func.roll_the_dice(self.host), self.port)

		if s is None:
			tfunc.write_daemon_text(self.name, self.host, 'Error: Daemon could not open socket in upload.')

		else:
			while 1:

				conn, addr = s.accept()
				ricevutoByte = conn.recv(const.LENGTH_PACK)
				#print("\n")
				#tfunc.write_daemon_text(self.name, addr[0], str(ricevutoByte, "ascii"))


				if not ricevutoByte:
					tfunc.write_daemon_error(self.name, addr[0], "Pacchetto errato")
				elif (str(ricevutoByte[0:4], "ascii") == pack.CODE_CLOSE):
					break
				else:
					if str(ricevutoByte[0:4], "ascii") == pack.CODE_LOGIN: ### LOGIN
						pk = func.reconnect_user(ricevutoByte[4:59], self.listUsers) #da fare reconnect
						if pk == const.ERROR_PKT: 
							pk = pack.answer_login()
						conn.sendall(pk)
						user = [ricevutoByte[4:59], ricevutoByte[59:], pk[4:]]
						"""da fare controllo utente loggato
						if not user in self.listUsers:
							self.listUsers.append(user)
							tfunc.write_daemon_success(self.name, addr[0], "LOGIN OK")
						else: tfunc.write_daemon_success(self.name, addr[0], "RECONNECT OK")
						#print(self.listUsers)
						"""

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_ADDFILE:
						# Controllo presenza user
						if ricevutoByte[4:20] in listUsers.values():
							# Funzione che crea listPart tutta di 1
							totalPartFile = fs.create_total_part(ricevutoByte[20:30], ricevutoByte[30:36])
							fileToAdd = fs.FileStruct(ricevutoByte[36:136], ricevutoByte[20:30], ricevutoByte[30:36], [ricevutoByte[4:20], totalPartFile])
							self.listFile[ricevutoByte[-32:]] = fileToAdd 
							pk = pack.answer_add_file(totalPartFile)
							conn.send(pk)
						else:
							tfunc..write_daemon_error(self.name, addr[0], "ADD FILE - User not logged")


						"""
						if func.isUserLogged(ricevutoByte[4:20], self.listUsers):
							if(func.check_file(self.listFiles, ricevutoByte)):
								self.listFiles.insert(0, [ricevutoByte[20:52], ricevutoByte[52:152], ricevutoByte[4:20]])
								tfunc.write_daemon_success(self.name, addr[0], "ADD FILE: " + str(ricevutoByte[52:152], "ascii").strip())
							else:
								tfunc.write_daemon_error(self.name, addr[0], "ADD FILE - File già inserito")
						else:
							tfunc.write_daemon_error(self.name, addr[0], "ADD FILE - User not logged")
						"""

					elif(str(ricevutoByte[0:4], "ascii") == pack.CODE_LOOK): ### Richiesta di ricerca file da un peer
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

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_UPDATE_PART: ### Aggiornamento parti scaricate
					"""
					tfunc.write_daemon_text(self.name, addr[0], "UPLOAD")
					filef = func.find_file_by_md5(ricevutoByte[4:])
					if filef != const.ERROR_FILE:
						func.upload(filef, conn)
					"""

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_LOGOUT: ### LOGOUT
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
			
