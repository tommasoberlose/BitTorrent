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

class DaemonDownload(Thread):

	def __init__(self, host, t_host, sessionID, fileName, md5, partN, peer, listPartOwned):
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

	def run(self):
		
		sP = func.create_socket_client(func.roll_the_dice(self.peer[0]), self.peer[1])
		if sP is None:
		    print ('Error: could not open socket in download')
		else:
			listPartOwned[self.md5][partN - 1] = '2'

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

				# Creo il file .part
				dnl.create_part(ricevutoByte, self.fileName, self.md5, self.partN)

				# Aggiorno la mia memoria
				dnl.update_own_memory(self.md5, self.partN, self.listPartOwned)

				# Invio l'update al tracker
				send_update(self.t_host, self.sessionID, self.md5, self.partN)


# >> PEER
def send_update(t_host, sessionID, md5, partN):
	s = func.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1])
	if s is None:
	    print ('Error: could not open socket to update Tracker')
	else:
		pk = pack.request_update_tracker(sessionID, md5, partN)
		s.sendall(pk)
		ricevutoByte = sP.recv(const.LENGTH_LONG_HEADER)
		if str(ricevutoByte[0:4], "ascii") == const.CODE_ANSWER_UPDATE_PART:
			tfunc.success("Download parte completato.\nAttualemente in possesso di " + str(int(ricevutoByte[4:])) + " parti del file.")
		s.close()
