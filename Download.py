import DaemonDownload as daemonDnl
import Search as src
import FileStruct as fs
import Package as pack
import SocketFunc as sfunc
import threading
from threading import *
import TextFunction as tfunc
import Constant as const

###### DOWNLOAD FILE

# Funzione di download
# >> PEER
def start_download(host, t_host, selectFile, sessionID, listPartOwned):	

	md5 = selectFile[1]
	fileName = selectFile[2]
	ricevutoByte = request_memory_of_hitpeer(t_host, sessionID, md5)

	if str(ricevutoByte[0:4], "ascii") == pack.CODE_ANSWER_FIND_PART:
		nHitPeer = int(ricevutoByte[4:7])
		if nHitPeer != 0:
			listPart = fs.find_part_from_hitpeer(int(ricevutoByte[4:7]), ricevutoByte[7:])

			for part in list(listPart.items()):
				daemonThreadD = daemonDnl.DaemonDownload(host, t_host, sessionID, fileName, md5, part, listPartOwned)
				daemonThreadD.setName("DAEMON DOWNLOAD PART " + part[0] " di " + fileName)
				daemonThreadD.start()


			# Controllo se ho finito di scaricare il file
			if not check_ended_download(fileName, md5, listPartOwned):
		    	threading.Timer(60, start_download).start()
		    else:
				save_and_open_file(fileName)
		else:
			tfunc.error("Non ci sono hitpeer disponibili da cui scaricare il file.")


	
		


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
def update_own_memory(md5, partN, listPartOwned):
	listPartOwned[md5][partN - 1] = "1"

# >> PEER
def save_and_open_file(fileName):
	# Salvare il file data aprirlo??
	print("prima o poi aprirò il file e te lo farò vedere stronzo")
	#### OPEN TUTTE LE PART, PRENDO, CREO FILE, APRO E POI CHIEDO SE DEVO ELIMINARLO
	"""
	open((const.FILE_COND + nomeFile),'wb').write(ricevutoByte)
	print("File scaricato correttamente, apertura in corso...")
	try:
		os.system("open " + const.FILE_COND + nomeFile)
	except:
		try:
			os.system("start " + const.FILE_COND + nomeFile)
		except:
			print("Apertura non riuscita")
	"""

# >> PEER
def create_part(ricevutoByte, fileName, md5, partN):
	open((const.FILE_COND + fileName + const.EXT_PART),'wb').write(ricevutoByte)

# >> PEER
def check_ended_download(fileName, md5, listPartOwned):
	if len(listPartOwned[md5]) == fs.count_part(listPartOwned[md5]):
		tfunc.success("Download del file completato.")
		c = input("Aprire il file? (S/N)")
		if (c == "s") or (c == "S"):
			return True
		else:
			return False