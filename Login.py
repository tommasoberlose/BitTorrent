import Package as pack
import Constant as const
import SocketFunc as sfunc
import TextFunc as tfunc
import Function as func
import sys

# >> PEER
def login(host, t_host):

	if t_host[0] == "":
		nGroup = input("Inserire il numero del gruppo del tracker: ")
		nElement = input("Inserire il numero dell'elemento del gruppo del tracker: ")
		t_host = [("172.030." + tfunc.format_string(nGroup, const.LENGTH_SECTION_IPV4, "0") + 
						"." + tfunc.format_string(nElement, const.LENGTH_SECTION_IPV4, "0") + 
						"|fc00:0000:0000:0000:0000:0000:" + tfunc.format_string(nGroup, const.LENGTH_SECTION_IPV6, "0") + 
						":" + tfunc.format_string(nElement, const.LENGTH_SECTION_IPV6, "0")), const.TPORT]

	tfunc.warning("\n>>> LOGIN")
	s = sfunc.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1])
	pk = pack.request_login(host)
	if s is None:
		tfunc.error("Errore nell'apertura della socket per il login")
		return const.ERROR_LOG
	else:
		s.sendall(pk)
		ricevutoByte = s.recv(const.LENGTH_PACK)
		sessionID = ricevutoByte[4:20]
		s.close()
		return t_host, sessionID

# >> TRACKER
def reconnect_user(ip, port, listUsers, name, addr):
	pk = const.ERROR_PKT
	listaUtenti = []
	if [ip, port] in listUsers.values():
		listaUtenti = list(listUsers.items())
		for i in listaUtenti:
			if i[1] == [ip,port]:
				pk = pack.answer_login_old_user(i[0])
				break

	if pk == const.ERROR_PKT: 
		tfunc.write_daemon_success(name, addr[0], "LOGIN OK")
		pk = pack.answer_login()
	else:
		tfunc.write_daemon_success(name, addr[0], "RECONNECT OK")

	listUsers[pk[4:]] = [ip, port]
	return pk


# >> PEER
def try_connection(host):
	s = sfunc.create_socket_client(func.roll_the_dice(host), const.TPORT)
	pk = pack.confirm()
	if s is None:
		sys.exit(-1)
	else:
		s.sendall(pk)
		s.close()