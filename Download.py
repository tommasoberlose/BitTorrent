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
import Function as func
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
			listPart = fs.find_part_from_hitpeer(int(ricevutoByte[4:7]), ricevutoByte[7:], listPartOwned, md5)

			for part in listPart:
				daemonThreadD = daemonDnl.DaemonDownload(host, t_host, sessionID, fileName, md5, part[0], part[1], listPartOwned, lenFile, lenPart)
				daemonThreadD.setName("DAEMON DOWNLOAD PART " + str(part[0]) + " di " + str(fileName, "ascii"))
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
		return byte(const.ERROR_PKT, "ascii")
	else:
		pk = pack.request_hitpeer(sessionID, md5)
		s.sendall(pk)

		return s.recv(4 * const.LENGTH_PACK)

# >> PEER
def update_own_memory(md5, partN, listPartOwned, value):
	listToUpdate = list(listPartOwned[md5])
	listToUpdate[partN - 1] = value
	listPartOwned[md5] = "".join(listToUpdate)


# >> PEER
def save_and_open_file(fileN):
	
	#### OPEN TUTTE LE PART, PRENDO, CREO FILE, APRO E POI CHIEDO SE DEVO ELIMINARLO

	fileName = str(fileN, "ascii")
	
	fileDnl = open((const.FILE_COND + fileName),'r+b')
	lenFile = (os.stat(const.FILE_COND + fileName).st_size) - const.LENGTH_HOST
	print(lenFile)
	s = fileDnl.read(lenFile)
	open((const.FILE_COPY + fileName), 'wb').write(s)
	
	print("File scaricato correttamente, desideri aprirlo? S/N \n\n")
	choice = input()
	if (choice == "S" or choice == "s"):
		try:
			os.system("open " + const.FILE_COPY + fileName)
		except:
			try:
				os.system("start " + const.FILE_COPY + fileName)
			except:
				print("Apertura non riuscita")

	print ("Vuoi eliminare il file appena scaricato? S/N \n\n")
	choiceDel = input()
	if (choiceDel == "S" or choiceDel == "s"):
		os.remove(const.FILE_COPY + fileName)
		print ("File rimosso con successo.")
	

# >> PEER
def create_part(ricevutoByte, fileName, partN, lenFile, lenPart):  #se il file non esiste, creo il file intero vuoto e mi sposto sulla parte e ci scrivo sopra. Poi se cè già mi sposto e scrivo. 
	notExists = False
	startPos = int(lenPart) * (partN - 1)
	if os.path.exists(const.FILE_COND + str(fileName, "ascii")):
		fileDnl = open((const.FILE_COND + str(fileName, "ascii")), 'r+b')
	else:
		notExists = True
		fileDnl = open((const.FILE_COND + str(fileName, "ascii")),'w+b')
		fileDnl.write(b'\x00' * startPos)

	#tail = extract_tail(lenPart, partN, fileDnl, lenFile)
	fileDnl.seek(startPos, 0)
	fileDnl.write(ricevutoByte)
	if notExists:
		fileDnl.write(b'\x00' * (lenFile - startPos - lenPart))
	fileDnl.close()
	#fileDnl.write(ricevutoByte + tail)

# >> PEER NON DA CONSIDERARE
def check_ended_download(fileName, md5, listPartOwned):
	if len(listPartOwned[md5]) == fs.count_part(listPartOwned[md5]):
		tfunc.success("Download del file completato.")
		return True
	else:
		return False

def extract_tail(lenPart, partN, fileDnl, lenFile):
	startPos = int(lenPart * (partN))
	fileDnl.seek(startPos, 0)
	return fileDnl.read(lenFile - startPos)




