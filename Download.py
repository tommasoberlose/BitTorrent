import PartFunc as pfunc
import DaemonDownload as daemonDnl
import Function as func
import Search as src
import FileStruct as fs
import Package as pack
import SocketFunc as sfunc
import threading
from threading import *
import TextFunc as tfunc
import Constant as const
import os
import time

###### DOWNLOAD FILE

class DaemonMasterOfDownloads(Thread):

	def __init__(self, host, t_host, selectFile, sessionID, listPartOwned):
		Thread.__init__(self)
		self.host = host
		self.t_host = t_host
		self.selectFile = selectFile
		self.sessionID = sessionID
		self.listPartOwned = listPartOwned

	def run(self):
		while start_download(self.host, self.t_host, self.selectFile, self.sessionID, self.listPartOwned):
			time.sleep(const.TIME_TO_UPDATE)


# Funzione di download
# >> PEER
def start_download(host, t_host, selectFile, sessionID, listPartOwned):	

	md5 = selectFile[1]
	fileName = selectFile[2]
	lenFile = selectFile[3]
	lenPart = selectFile[4]
	ricevutoByte = request_memory_of_hitpeer(t_host, sessionID, md5)

	if str(ricevutoByte[0:4], "ascii") == pack.CODE_ANSWER_FIND_PART:
		nHitPeer = int(ricevutoByte[4:7])
		if nHitPeer != 0:
			listPart = fs.find_part_from_hitpeer(host, int(ricevutoByte[4:7]), ricevutoByte[7:], listPartOwned, md5, lenFile, lenPart)

			for part in listPart:
				daemonThreadD = daemonDnl.DaemonDownload(host, t_host, sessionID, fileName, md5, part[0], part[1], listPartOwned, lenFile, lenPart)
				daemonThreadD.setName("DAEMON DOWNLOAD PART " + str(part[0]) + " di " + str(fileName, "ascii"))
				daemonThreadD.setDaemon(True)
				daemonThreadD.start()

			# Controllo se ho finito di scaricare il file
			if check_ended_download(fileName, md5, listPartOwned):
				save_and_open_file(fileName)
				return False
		else:
			tfunc.error("Non ci sono hitpeer disponibili da cui scaricare il file.")

	return True


# >> PEER
def request_memory_of_hitpeer(t_host, sessionID, md5):
	s = sfunc.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1]);
	if s is None:
		tfunc.error("Tracker non attivo.")
		return bytes(const.ERROR_PKT, "ascii")
	else:
		pk = pack.request_hitpeer(sessionID, md5)
		s.sendall(pk)

		return s.recv(4 * const.LENGTH_PACK)

# >> PEER
def update_own_memory(md5, partN, listPartOwned, value):
	listToUpdate = list(listPartOwned[md5][0])
	listToUpdate[partN] = value
	listPartOwned[md5][0] = "".join(listToUpdate)
	#pfunc.part_compl(listPartOwned[md5][0])


# >> PEER
def save_and_open_file(fileN):

	fileName = str(fileN, "ascii").strip()	
	
	try:
		retcode = os.system("open " + const.FILE_COND + fileName)
	except:
		try:
			os.system("start " + const.FILE_COND + fileName)
		except:
			print("Apertura non riuscita")
	
	

# >> PEER
def create_part(ricevutoByte, fileN, partN, lenFile, lenPart):  
	notExists = False
	startPos = int(lenPart) * (partN)
	fileName = str(fileN, "ascii").strip()
	if os.path.exists(const.FILE_COND + fileName):
		fileDnl = open((const.FILE_COND + fileName), 'r+b')
	else:
		notExists = True
		fileDnl = open((const.FILE_COND + fileName),'w+b')
		fileDnl.write(b'\x00' * startPos)

	fileDnl.seek(startPos, 0)
	fileDnl.write(ricevutoByte)
	if notExists:
		fileDnl.write(b'\x00' * (int(lenFile) - int(startPos) - int(lenPart)))
	fileDnl.close()

# >> PEER
def check_ended_download(fileName, md5, listPartOwned):
	if len(listPartOwned[md5][0]) == fs.count_one_in_part(listPartOwned[md5][0]):
		tfunc.success("Download del file completato.")
		return True
	else:
		return False




