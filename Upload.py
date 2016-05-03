
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
