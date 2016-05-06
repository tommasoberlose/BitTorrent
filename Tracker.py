import Constant as const
import Function as func
import Package as pack
import TextFunc as tfunc
import SocketFunc as sfunc
import FileStruct as fs
from threading import *
import Logout as logo
import Login as logi
import Search as src
import Add as add

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
			while 1: 

				conn, addr = s.accept()
				ricevutoByte = conn.recv(const.LENGTH_PACK)
				#print("\n")
				#tfunc.write_daemon_text(self.name, addr[0], str(ricevutoByte, "ascii"))


				if not ricevutoByte:
					tfunc.write_daemon_error(self.name, addr[0], "Pacchetto errato")
				elif (str(ricevutoByte[0:4], "ascii") == pack.CODE_CLOSE):
					break
				elif (str(ricevutoByte[0:4], "ascii") == pack.CODE_CONFIRM):
					tfunc.write_daemon_success(self.name, addr[0], "Avvio demone Tracker")
				else:
					if str(ricevutoByte[0:4], "ascii") == pack.CODE_LOGIN: ### LOGIN OK
						pk = logi.reconnect_user(ricevutoByte[4:59], ricevutoByte[59:], self.listUsers, self.name, addr)
						conn.sendall(pk)

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_ADDFILE: ### ADD FILE OK
						# Controllo presenza user
						if ricevutoByte[4:20] in self.listUsers:
							pk = add.add_file_to_list(ricevutoByte[36:136], ricevutoByte[20:30], ricevutoByte[30:36], ricevutoByte[4:20], ricevutoByte[-32:], self.listFile, self.name, addr)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "ADD FILE - User not logged")

					elif(str(ricevutoByte[0:4], "ascii") == pack.CODE_LOOK): ### LOOK
						# Controllo presenza user
						if ricevutoByte[4:20] in self.listUsers:
							pk = src.search_in_list_file(self.listFile, ricevutoByte[4:20], ricevutoByte[20:], self.name, addr)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "SEARCH FILE - User not logged")

					elif(str(ricevutoByte[0:4], "ascii") == pack.CODE_FIND_PART): ### SEARCH PART 
						# Controllo presenza user
						if ricevutoByte[4:20] in self.listUsers:
							pk = src.find_hitpeer(self.listFile, self.listUsers, ricevutoByte[4:20], ricevutoByte[20:], self.name, addr)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "REQUEST FILEPART - User not logged")

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_UPDATE_PART: ### UPDATE MEMORY OK
						# Controllo presenza user
						if ricevutoByte[4:20] in self.listUsers:
							pk = update_memory(ricevutoByte[4:20], ricevutoByte[20:52], ricevutoByte[52:], self.listFile)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "ADD FILE - User not logged")

					elif str(ricevutoByte[0:4], "ascii") == pack.CODE_LOGOUT: ### LOGOUT OK
						if ricevutoByte[4:20] in self.listUsers:
							pk = logo.try_logout(ricevutoByte[4:], self.listFile, self.listUsers)
							conn.sendall(pk)
						else:
							tfunc.write_daemon_error(self.name, addr[0], "User not logged")

					else:
						tfunc.write_daemon_error(self.name, addr[0], "Ricevuto pacchetto sbagliato: " + str(ricevutoByte, "ascii"))
			s.close()
			
