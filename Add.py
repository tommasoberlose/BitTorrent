import Constant as const
import SocketFunc as sFunc
import Function as func
import string
import os
import hashlib

# Le variabili in ingresso sono stringhe
def add(ip55, sessionID, ipTracker55):
	func.warning("\n>>> ADD FILE")
	fileName = input("Quale file vuoi inserire?\n")
	if fileName is not "0":
		if os.path.exists(const.FILE_COND + fileName):
			open((const.FILE_COND + fileName), 'ab').write(bytes(ip55, "ascii"))
			md5File = hashlib.md5(open(("FileCondivisi/" + fileName),'rb').read()).hexdigest()
			pk = pack.request_add_file(sessionID, md5File, sFunc.format_string(fileName, const.LENGTH_FILENAME, " "))
			s = sFunc.create_socket_client(func.roll_the_dice(ipTracker55), const.TPORT);
			if s is None:
				tfunc.error("Errore, tracker non attivo.")
			else:
				s.sendall(pk)
				ricevutoByte = s.recv(const.LENGTH_PACK)
				if(ricevutoByte[:4].decode("ascii") == const.CODE_ANSWER_ADDFILE):
					tfunc.success("Il file " + fileName + " è stato aggiunto con successo.\nÈ stato diviso in " + str(int(ricevutoByte[4:])) + " parti.")
				else:
					tfunc.error("Errore nella ricezione del codice di aggiunta file.")
				s.close()
		else:
			tfunc.error("Errore: file non esistente.")