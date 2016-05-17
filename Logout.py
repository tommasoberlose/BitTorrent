import Package as pack
import Function as func
import SocketFunc as sFunc
import Constant as const
import TextFunc as tfunc
import FileStruct as fs
import time


# >> PEER
def logout(ip55, t_host, sessionID):
	tfunc.warning("\n>>> LOGOUT")
	result = -1
	pk = pack.request_logout(sessionID)
	s = sFunc.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1]);
	if s is None:
		tfunc.error("Errore nella creazione della socket per il logout.")
	else:
		s.sendall(pk)
		ricevutoByte = s.recv(const.LENGTH_PACK)
		if str(ricevutoByte[:4], "ascii") == pack.CODE_LOGOUT_DENIED:
			tfunc.error("Siamo spiacenti ma il logout risulta impossibile poichè si è in possesso di parti di file uniche.\n" + \
				"Sono state scaricate " + str(int(ricevutoByte[4:])) + " parti del file, fatevi il conto di quante ne mancano.")
		elif str(ricevutoByte[:4], "ascii") == pack.CODE_ANSWER_LOGOUT:	
			tfunc.success("Logout eseguito con successo.\nAvevi " + str(int(ricevutoByte[4:])) + " parti, peccato tu te ne vada, addio.")
			time.sleep(const.TIME_TO_UPDATE)
			pk = pack.close()
			sD = sFunc.create_socket_client(func.roll_the_dice(ip55), const.PORT);
			if sD is None:
				tfunc.error("Errore nella chiusura del demone")
			else:
				sD.sendall(pk)
				sD.close()
			tfunc.success("Chiusura del peer eseguito con successo, arrivederci.\n\n")
			result = 1
		else:
			tfunc.error("Errore nel codice di logout.")
		s.close()

	return result

# >> TRACKER
def try_logout(sessionID, listFile, listUsers):
	nPart, ndPart = fs.get_part_for_logout(sessionID, listFile)
	if ndPart != 0:
		return pack.reject_logout(nPart - ndPart)
	else:
		remove_user(sessionID, listFile, listUsers)
		return pack.answer_logout(nPart)

# >> PEER
def quit(ip55):
	tfunc.warning("\n>>> QUIT")
	pk = pack.close()
	s = sFunc.create_socket_client(func.roll_the_dice(ip55), const.TPORT);
	if s is None:
		tfunc.error("Errore nella chiusura del demone tracker")
	else:
		s.sendall(pk)
		s.close()
		tfunc.success("Chiusura del demone tracker eseguito con successo, arrivederci.\n\n")

# >> TRACKER
def remove_user(sessionID, listFile, listUsers):
	del listUsers[sessionID]
	list_file_from_dict = list(listFile.items())
	for fileC in list_file_from_dict:
		if sessionID in fileC[1].listOwner:
			del fileC[1].listOwner[sessionID]

	d = {key: value for (key, value) in list_file_from_dict}
	return d