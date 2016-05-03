
###### DOWNLOAD FILE

# Funzione di download
def download(selectFile):	
	print ("\n>>> DOWNLOAD")

	md5 = selectFile[1]
	nomeFile = selectFile[2].decode("ascii").strip()
	ip = selectFile[3]
	port = selectFile[4]

	# Con probabilità 0.5 invio su IPv4, else IPv6
	ip = func.roll_the_dice(ip.decode("ascii"))
	print("Connessione con:", ip)

	# Mi connetto al peer

	sP = func.create_socket_client(ip, port)
	if sP is None:
	    print ('Error: could not open socket in download')
	else:
		pk = pack.request_download(md5)
		sP.sendall(pk)

		nChunk = int(sP.recv(const.LENGTH_HEADER)[4:10])
					
		ricevutoByte = b''

		i = 0
		
		while i != nChunk:
			ricevutoLen = sP.recv(const.LENGTH_NCHUNK)
			while (len(ricevutoLen) < const.LENGTH_NCHUNK):
				ricevutoLen = ricevutoLen + sP.recv(const.LENGTH_NCHUNK - len(ricevutoLen))
			buff = sP.recv(int(ricevutoLen))
			while(len(buff) < int(ricevutoLen)):
				buff = buff + sP.recv(int(ricevutoLen) - len(buff))
			ricevutoByte = ricevutoByte + buff
			i = i + 1

		sP.close()
		
		# Salvare il file data
		open((const.FILE_COND + nomeFile),'wb').write(ricevutoByte)
		print("File scaricato correttamente, apertura in corso...")
		try:
			os.system("open " + const.FILE_COND + nomeFile)
		except:
			try:
				os.system("start " + const.FILE_COND + nomeFile)
			except:
				print("Apertura non riuscita")