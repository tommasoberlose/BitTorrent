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
import Download as dnl

mutex = Lock()

class DaemonDownload(Thread):

	def __init__(self, host, t_host, sessionID, fileName, md5, partN, peer, listPartOwned, lenFile, lenPart):
		Thread.__init__(self)
		self.host = host
		self.t_host = t_host
		self.port = const.PORT
		self.sessionID = sessionID
		self.fileName = fileName
		self.peer = peer
		self.md5 = md5
		self.partN = partN
		self.listPartOwned = listPartOwned
		self.lenFile = lenFile
		self.lenPart = lenPart

	def run(self):

		global mutex
		
		sP = sfunc.create_socket_client(func.roll_the_dice(self.peer[0]), self.peer[1])
		if sP is None:
		    #tfunc.error('Error: could not open socket in download')
		    var = "" # giusto per fargli fare qualcosa
		else:
			try:
				if mutex.acquire(timeout = const.TIME_TO_UPDATE):
					dnl.update_own_memory(self.md5, self.partN, self.listPartOwned, "2")
					mutex.release()

					#tfunc.gtext("Start download della parte " + str(self.partN) + " da " + str(self.peer[0], "ascii"))

					pk = pack.request_download(self.md5, self.partN)
					sP.sendall(pk)
					ricevutoByte = sP.recv(const.LENGTH_HEADER)
					if str(ricevutoByte[0:4], "ascii") == pack.CODE_ANSWER_DOWNLOAD:
						nChunk = int(ricevutoByte[4:10])
						ricevutoByte = b''
						i = 0
						
						while i != nChunk:
							ricevutoLen = sP.recv(const.LENGTH_NCHUNK)
							while (len(ricevutoLen) < const.LENGTH_NCHUNK):
								ricevutoLen = ricevutoLen + sP.recv(const.LENGTH_NCHUNK - len(ricevutoLen))
							buff = sP.recv(int(ricevutoLen))
							while(len(buff) < int(ricevutoLen)):
								buff = buff + sP.recv(int(ricevutoLen) - len(buff))
							ricevutoByte = ricevutoByte + buff
							i = i + 1

						sP.close()

						# Modifico nel file la parte che ho appena scaricato, se il file non esiste lo creo (es b'00000')
						dnl.create_part(ricevutoByte, self.fileName, self.partN, self.lenFile, self.lenPart)

						if mutex.acquire(timeout = const.TIME_TO_UPDATE):
							# Aggiorno la mia memoria
							dnl.update_own_memory(self.md5, self.partN, self.listPartOwned, "1")
							mutex.release()

							pfunc.part_all(self.listPartOwned[self.md5][0])

							# Invio l'update al tracker
							send_update(self.t_host, self.sessionID, self.md5, self.partN, self.listPartOwned, self.peer)
						else:
							raise Exception("Error Download Code")
					else:
						raise Exception("Error Download Code")

				else:
					raise Exception("Error Download Code")

			except Exception as e:
				#tfunc.write_daemon_error(self.name, str(self.peer[0], "ascii"), "ERRORE DOWNLOAD: {0}".format(e))
				dnl.update_own_memory(self.md5, self.partN, self.listPartOwned, "0")


# >> PEER
def send_update(t_host, sessionID, md5, partN, listPartOwned, peer):
	s = sfunc.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1])
	if s is None:
	    tfunc.error('Error: could not open socket to update Tracker')
	else:
		pk = pack.request_update_tracker(sessionID, md5, partN)
		s.sendall(pk)
		ricevutoByte = s.recv(const.LENGTH_PACK)
		if str(ricevutoByte[0:4], "ascii") == pack.CODE_ANSWER_UPDATE_PART:
			tfunc.dnl_success("Download eseguito della parte " + str(partN) + " da " + str(peer[0], "ascii") + "\nAttualmente in possesso di " + str(int(ricevutoByte[4:])) + "/" + str(len(listPartOwned[md5][0])) + " parti del file.")
		s.close()
