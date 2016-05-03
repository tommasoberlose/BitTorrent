import threading
import time
import sys
import socket
import Constant as const
import Function as func
import Package as pack
from threading import * 
import time
import TextFunc as tfunc
import SocketFunc as sfunc
import Upload as upl

"""

class Daemon(Thread):

	# Inizializza il thread, prende in ingresso l'istanza e un valore su cui ciclare
	# Tutti i metodi di una classe prendono l'istanza come prima variabile in ingresso
	# __init__ è un metodo predefinito per creare il costruttore
	def __init__(self, host, SN, sn_network, listPkt, listUsers, listFiles, role):
		# Costruttore
		Thread.__init__(self)
		self.host = host
		self.SN = SN
		if role:
			self.port = const.PORT_SN
		else:
			self.port = const.PORT
		self.sn_network = sn_network
		self.listPkt = listPkt
		self.listUsers = listUsers
		self.listFiles = listFiles
		#self.listResultQuery = []

	def run(self):
		# Creazione socket
		s = sfunc.create_socket_server(func.roll_the_dice(self.host), self.port)

		if s is None:
			func.write_daemon_text(self.name, self.host, 'Error: Daemon could not open socket in upload.')

		else:
			while 1:

				conn, addr = s.accept()
				ricevutoByte = conn.recv(const.LENGTH_PACK)
				#print("\n")
				#func.write_daemon_text(self.name, addr[0], str(ricevutoByte, "ascii"))


				if not ricevutoByte:
					func.write_daemon_error(self.name, addr[0], "Pacchetto errato")
				elif (str(ricevutoByte[0:4], "ascii") == const.CODE_CLOSE):
					break
				else:
					if str(ricevutoByte[0:4], "ascii") == const.CODE_SN: ### REQUEST SN
						if func.add_pktid(ricevutoByte[4:20], self.listPkt, self.port) is True:
							# FORWARD
							pk = pack.forward_sn(ricevutoByte)
							func.forward(pk, addr[0], self.sn_network)

							# RESPONSE
							if self.SN:
								# Aggiunta supernodi (collaterale)
								if str(ricevutoByte[75:80], "ascii") == (func.format_string(const.PORT_SN, 5, "0")):
									if not [str(ricevutoByte[20:75],"ascii"), str(ricevutoByte[75:80],"ascii")] in self.sn_network: 
										self.sn_network.append([str(ricevutoByte[20:75],"ascii"), str(ricevutoByte[75:80],"ascii")])
										func.write_daemon_success(self.name, addr[0], "SN Network - Added: " + str(ricevutoByte[20:75], "ascii"))
								pk = pack.answer_sn(ricevutoByte[4:20], self.host)
								sR = func.create_socket_client(func.roll_the_dice(ricevutoByte[20:75]), ricevutoByte[75:80])
								if sR != None:
									sR.sendall(pk)
									sR.close()
						#else:
						#	func.write_daemon_error(self.name, addr[0], "Pacchetto già ricevuto")

					elif str(ricevutoByte[0:4], "ascii") == const.CODE_ANSWER_SN: ### ANSWER SN
						if self.SN:
							if func.check_sn(ricevutoByte[4:20], self.listPkt) is True:
								# ADD SN TO NETWORK
								if not [str(ricevutoByte[20:75], "ascii"), str(ricevutoByte[75:80], "ascii")] in self.sn_network:
									self.sn_network.append([str(ricevutoByte[20:75],"ascii"), str(ricevutoByte[75:80],"ascii")])
									func.write_daemon_success(self.name, addr[0], "SN NETWORK - Added: " + str(ricevutoByte[20:75], "ascii"))
								else:
									func.write_daemon_error(self.name, addr[0], "SN NETWORK - Super nodo già presente")
							else:
								func.write_daemon_error(self.name, addr[0], "Tempo per la risposta terminato.")
						else:
							if func.check_sn(ricevutoByte[4:20], self.listPkt) is True:
								if not [str(ricevutoByte[20:75], "ascii"), str(ricevutoByte[75:80], "ascii")] in self.sn_network:
									self.sn_network.append([str(ricevutoByte[20:75], "ascii"), str(ricevutoByte[75:80],"ascii")])
									func.write_daemon_success(self.name, addr[0], "SN NETWORK - Added: " + str(ricevutoByte[20:75], "ascii"))
								else:
									func.write_daemon_error(self.name, addr[0], "SN NETWORK - Super nodo già presente")
							else:
								func.write_daemon_error(self.name, addr[0], "Tempo per la risposta terminato.")

					elif str(ricevutoByte[0:4], "ascii") == const.CODE_LOGIN: ### LOGIN
						if self.SN:
							pk = func.reconnect_user(ricevutoByte[4:59], self.listUsers)
							if pk == const.ERROR_PKT: 
								pk = pack.answer_login()
							conn.sendall(pk)
							user = [ricevutoByte[4:59], ricevutoByte[59:], pk[4:]]
							if not user in self.listUsers:
								self.listUsers.append(user)
								func.write_daemon_success(self.name, addr[0], "LOGIN OK")
							else: func.write_daemon_success(self.name, addr[0], "RECONNECT OK")
							#print(self.listUsers)

					elif str(ricevutoByte[0:4], "ascii") == const.CODE_ADDFILE:
						if self.SN:
							if func.isUserLogged(ricevutoByte[4:20], self.listUsers):
								if(func.check_file(self.listFiles, ricevutoByte)):
									self.listFiles.insert(0, [ricevutoByte[20:52], ricevutoByte[52:152], ricevutoByte[4:20]])
									func.write_daemon_success(self.name, addr[0], "ADD FILE: " + str(ricevutoByte[52:152], "ascii").strip())
								else:
									func.write_daemon_error(self.name, addr[0], "ADD FILE - File già inserito")
							else:
								func.write_daemon_error(self.name, addr[0], "ADD FILE - User not logged")

					elif str(ricevutoByte[0:4], "ascii") == const.CODE_REMOVEFILE:
						if self.SN:
							if func.isUserLogged(ricevutoByte[4:20], self.listUsers):
								findFile = False
								i = 0
								for file in self.listFiles:
									if (ricevutoByte[4:20] == file[2]) and (ricevutoByte[20:] == file[0]):
										findFile = True
										del self.listFiles[i]
										func.write_daemon_success(self.name, addr[0], "REMOVE FILE: " + str(ricevutoByte[20:], "ascii").strip())
										i -= 1
									i += 1
								if not findFile:
									func.write_daemon_error(self.name, addr[0], "REMOVE FILE - File not exists")
							else:
								func.write_daemon_error(self.name, addr[0], "REMOVE FILE - User not logged")

					elif str(ricevutoByte[0:4], "ascii") == const.CODE_LOGOUT: ### LOGOUT
						if self.SN:
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
							func.write_daemon_success(self.name, addr[0], "LOGOUT OK")


					elif str(ricevutoByte[0:4], "ascii") == const.CODE_QUERY: ### QUERY tra SN
						func.write_daemon_text(self.name, addr[0], "QUERY - " + func.reformat_string(str(ricevutoByte[82:],"ascii")))
						if func.add_pktid(ricevutoByte[4:20], self.listPkt, self.port) is True:
							# Inoltro
							pk = pack.forward_query(ricevutoByte)
							func.forward(pk, addr[0], self.sn_network)

							# Rispondi
							listFileFounded = []
							listFileFounded = func.search_file(bytes(func.reformat_string(str(ricevutoByte[82:],"ascii")),"ascii"), self.listFiles, self.listUsers) # Da controllare
							if len(listFileFounded) != 0:
								for x in listFileFounded:
									pk = pack.answer_query(ricevutoByte[4:20], x[2], x[3], str(x[0], "ascii"), str(x[1], "ascii"))
									sC = func.create_socket_client(func.roll_the_dice(str(ricevutoByte[20:75], "ascii")), ricevutoByte[75:80])
									if sC != None:
										sC.sendall(pk)
										sC.close()
						#else:
						#	func.write_daemon_error(self.name, addr[0], "Pacchetto già ricevuto")

					elif str(ricevutoByte[0:4], "ascii") == const.CODE_ANSWER_QUERY: ### RISPOSTA QUERY tra SN
						if func.check_query(ricevutoByte[4:20], self.listPkt, self.port):
							listResultQuery.append([ricevutoByte[80:112], ricevutoByte[112:], ricevutoByte[20:75], ricevutoByte[75:80]])
						else: 
							func.write_daemon_error(self.name, addr[0], "ANSWER QUERY - Ricerca conclusa")
					
					elif str(ricevutoByte[0:4], "ascii") == const.CODE_DOWNLOAD: ### DOWNLOAD
						func.write_daemon_text(self.name, addr[0], "UPLOAD")
						filef = func.find_file_by_md5(ricevutoByte[4:])
						if filef != const.ERROR_FILE:
							func.upload(filef, conn)

					elif(str(ricevutoByte[0:4], "ascii") == const.CODE_SEARCH): ### Richiesta di ricerca da un peer
						if self.SN:
							del listResultQuery[:]
							func.write_daemon_text(self.name, addr[0], "INIZIO RICERCA DI: " + str(ricevutoByte[20:], "ascii").strip())
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
					else:
						func.write_daemon_error(self.name, addr[0], "Ricevuto pacchetto sbagliato: " + str(ricevutoByte, "ascii"))
			s.close()
"""

class PeerDaemon(Thread):

	def __init__(self, host):
		Thread.__init__(self)
		self.host = host
		self.port = const.PORT

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
				elif (str(ricevutoByte[0:4], "ascii") == const.CODE_CLOSE):
					break
				else:
					if str(ricevutoByte[0:4], "ascii") == const.CODE_DOWNLOAD: #UPLOAD
						upl.upload(ricevutoByte[4:36], ricevutoByte[36:], conn)
					else:
						tfunc.write_daemon_error(self.name, addr[0], "Ricevuto pacchetto sbagliato: " + str(ricevutoByte, "ascii"))
			s.close()
		