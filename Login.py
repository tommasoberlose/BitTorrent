import Package as pack

def login(host, t_host):
	tfunc.warning("\n>>> LOGIN")
	s = func.create_socket_client(func.roll_the_dice(t_host[0]), t_host[1])
	pk = pack.request_login(host)
	if s is None:
		tfunc.error("Errore nell'apertura della socket per il login")
		return const.ERROR_LOG
	else:
		s.sendall(pk)
		ricevutoByte = s.recv(const.LENGTH_PACK)
		sessionID = ricevutoByte[4:20]
		s.close()
		return sessionID