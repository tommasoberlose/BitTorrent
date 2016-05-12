import Constant as const
import SocketFunc as sfunc
import Function as func
import string
import os
import hashlib
import TextFunc as tfunc
import Package as pack
import FileStruct as fs
import PartFunc as pfunc

# Le variabili in ingresso sono stringhe
# >> PEER
def add(ip55, sessionID, t_host, listPartOwned):
	tfunc.warning("\n>>> ADD FILE")
	fileName = input("Quale file vuoi inserire?\n")
	if fileName != "0":
		if os.path.exists(const.FILE_COND + fileName):
			if not check_add(fileName, ip55):
				open((const.FILE_COND + fileName), 'ab').write(bytes(ip55, "ascii"))
			md5File = hashlib.md5(open((const.FILE_COND + fileName),'rb').read()).hexdigest()
			lenFile = os.stat(const.FILE_COND + fileName).st_size
			pk = pack.request_add_file(sessionID, lenFile, md5File, tfunc.format_string(fileName, const.LENGTH_FILENAME, " "))
			s = sfunc.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1]);
			if s is None:
				tfunc.error("Errore, tracker non attivo.")
			else:
				s.sendall(pk)
				ricevutoByte = s.recv(const.LENGTH_PACK)
				if(ricevutoByte[:4].decode("ascii") == pack.CODE_ANSWER_ADDFILE):
					tfunc.success("Il file " + fileName + " è stato aggiunto con successo.\nÈ stato diviso in " + str(int(ricevutoByte[4:])) + " parti.")
					pfunc.add_to_list_owner(md5File, lenFile, listPartOwned)
				else:
					tfunc.error("Errore nella ricezione del codice di aggiunta file.")
				s.close()
		else:
			tfunc.error("Errore: file non esistente.")


# >> TRACKER
def add_file_to_list(fileName, lenFile, lenPart, sessionIDUploader, md5, listFile, name, addr):
	if md5 not in listFile:
		fileToAdd = fs.FileStruct(fileName, lenFile, lenPart, sessionIDUploader)
		fileToAdd.add_owner_total()
		listFile[md5] = fileToAdd 
		tfunc.write_daemon_success(name, addr[0], "ADD FILE " + str(fileName, "ascii").strip())
		return pack.answer_add_file(fileToAdd.nPart)
	else:
		return pack.answer_add_file(listFile[md5].nPart)

# >> PEER
def check_add(fileName, ip55):
	f = open((const.FILE_COND + fileName),'rb')
	f.seek(-len(ip55), 2)
	if (f.read(len(ip55)) == bytes(ip55,"ascii")):
		return True
	else:
		return False
