import Package as pack
import Function as func
import SocketFunc as sFunc
import Constant as const
import TextFunc as tfunc


def logout(ip55, ipTracker55, sessionID):
	tfunc.warning("\n>>> LOGOUT")
	result = -1
	pk = pack.request_logout(sessionID)
	s = sFunc.create_socket_client(func.roll_the_dice(ipTracker55), const.TPORT);
	if s is None:
		tfunc.error("Errore nella creazione della socket per il logout.")
	else:
		s.sendall(pk)
		ricevutoByte = s.recv(const.LENGTH_PACK)
		if ricevutoByte[:4].decode("ascii") == "NLOG":
			tfunc.error("Siamo spiacenti ma il logout risulta impossibile poichè si è in possesso di parti di file uniche.\n" +
				+ "Sono state scaricate " + str(int(ricevutoByte[4:])) + " parti del file, fatevi il conto di quante ne mancano.")
		elif ricevutoByte[:4].decode("ascii") == "ALOG":	
			tfunc.success("Logout eseguito con successo.\nAvevi " + str(int(ricevutoByte[4:])) + " parti, peccato tu te ne vada, addio.")
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