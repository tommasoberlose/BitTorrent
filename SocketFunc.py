import socket

####### SOCKET

def create_socket_server(myHost, port):
	s = None
	for res in socket.getaddrinfo(None, int(port), socket.AF_UNSPEC,socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
	    af, socktype, proto, canonname, sa = res
	    try:
	    	s = socket.socket(af, socktype, proto)
	    except socket.error as msg:
	    	s = None
	    	continue
	    try:
	    	s.bind(sa)
	    	s.listen(100)
	    except socket.error as msg:
	    	s.close()
	    	s = None
	    	continue
	    break
	return s

def create_socket_client(myHost, port):
	s = None
	for res in socket.getaddrinfo(myHost, int(port), socket.AF_UNSPEC, socket.SOCK_STREAM):
	    af, socktype, proto, canonname, sa = res
	    try:
	        s = socket.socket(af, socktype, proto)
	    except socket.error as msg:
	        s = None
	        continue
	    try:
	        s.connect(sa)
	    except socket.error as msg:
	        s.close()
	        s = None
	        continue
	    break
	return s

def forward(pk, addr, l): 
	if pk != bytes(const.ERROR_PKT, "ascii"):
		for x in l:
			if addr != x[0]:
				s = func.create_socket_client(func.roll_the_dice(x[0]), x[1])
				if not(s is None):
					s.sendall(pk)
					#write_daemon_success("Daemon", "-", "Forward da " + addr + " a " + x[0])
					s.close()
