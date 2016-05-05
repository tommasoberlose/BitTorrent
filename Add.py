import Constant as const
import SocketFunc as sfunc
import Function as func
import string
import os
import hashlib
import TextFunc as tfunc
import Package as pack

# Le variabili in ingresso sono stringhe
def add(ip55, sessionID, t_host):
	tfunc.warning("\n>>> ADD FILE")
	fileName = input("Quale file vuoi inserire?\n")
	if fileName != "0":
		if os.path.exists(const.FILE_COND + fileName):
			open((const.FILE_COND + fileName), 'ab').write(bytes(ip55, "ascii"))
			md5File = hashlib.md5(open((const.FILE_COND + fileName),'rb').read()).hexdigest()
			lenFile = os.stat(const.FILE_COND + fileName).st_size
			pk = pack.request_add_file(sessionID, lenFile, md5File, tfunc.format_string(fileName, const.LENGTH_FILENAME, " "))
			s = sfunc.create_socket_client(func.roll_the_dice(t_host[0]), const.TPORT);
			if s is None:
				tfunc.error("Errore, tracker non attivo.")
			else:
				s.sendall(pk)
				ricevutoByte = s.recv(const.LENGTH_PACK)
				if(ricevutoByte[:4].decode("ascii") == pack.CODE_ANSWER_ADDFILE):
					tfunc.success("Il file " + fileName + " è stato aggiunto con successo.\nÈ stato diviso in " + str(int(ricevutoByte[4:])) + " parti.")
				else:
					tfunc.error("Errore nella ricezione del codice di aggiunta file.")
				s.close()
		else:
			tfunc.error("Errore: file non esistente.")