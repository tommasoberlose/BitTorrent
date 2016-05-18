import threading
import sys
import socket
import Constant as const
import Function as func
import Package as pack
from threading import * 
import TextFunc as tfunc
import SocketFunc as sfunc
import Upload as upl
import PartFunc as pfunc

class PeerDaemon(Thread):

	def __init__(self, host, listPartOwned):
		Thread.__init__(self)
		self.host = host
		self.port = const.PORT
		self.listPartOwned = listPartOwned

	def run(self):
		# Creazione socket
		s = sfunc.create_socket_server(func.roll_the_dice(self.host), self.port)
		if s is None:
			tfunc.write_daemon_text(self.name, self.host, 'Error: Daemon could not open socket in upload.')
		else:
			while 1:
				try:
					conn, addr = s.accept()
					
					ricevutoByte = conn.recv(const.LENGTH_PACK)

					if not ricevutoByte:
						tfunc.write_daemon_error(self.name, addr[0], "Pacchetto errato")
					elif (str(ricevutoByte[0:4], "ascii") == pack.CODE_CLOSE):
						break
					else:
						if str(ricevutoByte[0:4], "ascii") == pack.CODE_DOWNLOAD: #UPLOAD
							if pfunc.check_presence(int(ricevutoByte[36:]), ricevutoByte[4:36], self.listPartOwned):
								upl.upload(ricevutoByte[4:36], ricevutoByte[36:], conn, self.listPartOwned, self.name, addr)
							else:
								tfunc.write_daemon_error(self.name, addr[0], "Errore, la parte " + str(int(ricevutoByte[36:])) + " non è presente.")
						else:
							tfunc.write_daemon_error(self.name, addr[0], "Ricevuto pacchetto sbagliato: " + str(ricevutoByte, "ascii"))
				except Exception as ex:
					print(ex)
					continue
			s.close()
		