import string
import random
import socket
import shutil
import os
import sys
import hashlib
import time
import Constant as const
import Function as func
import Package as pack

# Random Functions
def random_pktid(length):
   return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length))

def random_sessionID(length):
   return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length))

def writeHelp():
	func.warning("\nPOSSIBILI ARGOMENTI:")
	print("Super Nodo\t-sn")
	print("Set Default Ip\t-ip group identifier")
	print("Change Port\t-p port")
	print("Change Port SN\t-pSN port")
	print("Change time\t-t time")
	print("Change ttl\t-ttl ttl")
	print("")
	sys.exit(-1)


###### IP

def roll_the_dice(ip):
	return random.choice([ip[0:15], ip[16:55]])

def get_ipv4(ip):
	return ip[0:15]

def get_ipv6(ip):
	return ip[16:55]


###### SEARCH FILE

def search_file(query, listFiles, listUsers): 
	listResultQuery = []
	for f in listFiles:
		if query in f[1]:
			for i in listUsers:
				if i[2] == f[2]:
					listResultQuery.append([f[0], bytes(func.format_string(str(f[1],"ascii"), const.LENGTH_FILENAME, " "),"ascii"), i[0], i[1]])
					break
	return listResultQuery


def add_pktid(pktid, list_pkt, port):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if (pktid == lista[0]):# and (port == lista[2]):
			return False
	pkTime = time.time() * 1000
	add_list = [pktid, pkTime, port]
	list_pkt.append(add_list)
	return True

def clear_pktid(list_pkt):
	x = 0
	for i in list_pkt:
		pkTime = i[1]
		nowtime = time.time() * 1000
		diff = nowtime - pkTime
		if diff >= const.MAX_TIME:
			del list_pkt[x]
			x -= 1
		x += 1
	return list_pkt

def check_query(pktid, list_pkt, port):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if (pktid == lista[0]):# and (port == lista[2]):
			return True
	return False

def check_sn(pktid, list_pkt):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if pktid == lista[0]:
			return True
	return False

def remove_pktid(pktid, list_pkt):
	i = 0
	for lista in list_pkt:
		if pktid == lista[0]:
			del list_pkt[i]
			i -= 1
		i += 1


###### UPLOAD FILE 

def upload(nomeFile, ss):
	f = open((const.FILE_COND + nomeFile), 'rb')

	fileLength = os.stat(const.FILE_COND + nomeFile).st_size
	nChunk = int(fileLength / const.LENGTH_PACK) + 1 

	nChunk = format_string(str(nChunk), const.LENGTH_NCHUNKS, "0")
	pk = bytes(const.CODE_ANSWER_DOWNLOAD, "ascii") + bytes(nChunk, "ascii")
	ss.sendall(pk)

	i = 0
	while True:
		line = f.read(const.LENGTH_PACK)
		dimLine = format_string(str(len(line)), const.LENGTH_NCHUNK, "0")
		pk = bytes(dimLine, "ascii") + line
		ss.sendall(pk)
		#print(pack)
		i = i + 1
		if i == int(nChunk):
			break

def find_file_by_md5(md5):
	file_list = os.listdir(const.FILE_COND)
	for filef in file_list:
		if not filef.endswith('~'):
			md5File = hashlib.md5(open(const.FILE_COND + filef,'rb').read()).hexdigest()
			if str(md5, "ascii") == md5File:
				return filef
	return const.ERROR_FILE


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

# Scelta random tra Supernodi

def choose_SN(sn_network):
	choose = random.sample(sn_network, 1)
	choose = choose[0]
	for n in sn_network:
		if not n == choose:
			del n
	return choose


####### USERS
def countUserFile(sessionID, listFiles):
	i = 0
	for f in listFiles:
		if f[2] == sessionID:
			i += 1
	return i

def isUserLogged(sessionID, listUsers):
	for user in listUsers:
		if sessionID == user[2]:
			return True
	return False

def reconnect_user(ip, listUsers):
	pk = const.ERROR_PKT
	for user in listUsers:
		if user[0] == ip:
			pk = pack.answer_login()[:4] + user[2]
			break
	return pk

def check_file(listFiles, ricevutoByte):
	fileConfronto = [ricevutoByte[20:52], ricevutoByte[52:152], ricevutoByte[4:20]]
	for file in listFiles:
		if (file[0] == fileConfronto[0]) and (file[2] == fileConfronto[2]):
			return False
	return True

def send_afin(conn, listResultQuery):
	if len(listResultQuery) != 0:
		nMd5 = 0

		listResultQuery.sort()

		md5 = b''
		for x in listResultQuery:
			if md5 != x[0]:
				md5 = x[0]
				nMd5 += 1

		
		pk = bytes(const.CODE_ANSWER_SEARCH, "ascii") + bytes(func.format_string(str(nMd5), const.LENGTH_NIDMD5, "0"), "ascii")

		actualMd5 = b''

		for i in listResultQuery:
			if i[0] != actualMd5:
				#actualMd5 = listResultQuery[0][0]
				# calcolo numero copie
				actualMd5 = i[0]
				copy = 0
				for x in listResultQuery:
					if x[0] == actualMd5:
						copy += 1

				pk = pk + i[0] + i[1] + bytes(func.format_string(str(copy), const.LENGTH_NCOPY, "0"), "ascii")

			pk = pk + i[2] + i[3] 


	else:
		pk = bytes(const.CODE_ANSWER_SEARCH, "ascii") + bytes("0" * const.LENGTH_NIDMD5, "ascii")  

	conn.sendall(pk)







