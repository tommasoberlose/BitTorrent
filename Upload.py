import Constant as const
import TextFunc as tfunc
import Package as pack
import hashlib
import os
###### UPLOAD FILE 

# >> PEER
def upload(md5, nPart, ss, listPartOwned):
	nomeFile = find_file_by_md5(md5)
	if nomeFile != const.ERROR_FILE:

		print("Upload parte " + nPart)

		f = open((const.FILE_COND + nomeFile), 'rb')

		fileLength = os.stat(const.FILE_COND + nomeFile).st_size

		lenPart = fileLength / len(listPartOwned[md5])

		if (lenPart % const.LENGTH_PACK) > 0:
			nChunk = int(lenPart / const.LENGTH_PACK) + 1 
		else:
			nChunk = int(lenPart / const.LENGTH_PACK)

		nChunk = tfunc.format_string(str(nChunk), const.LENGTH_NCHUNKS, "0")
		pk = bytes(pack.CODE_ANSWER_DOWNLOAD, "ascii") + bytes(nChunk, "ascii")
		ss.sendall(pk)

		f.seek(int(nPart) * int(lenPart), 0)

		i = 0
		while True:
			line = f.read(const.LENGTH_PACK)
			dimLine = tfunc.format_string(str(len(line)), const.LENGTH_NCHUNK, "0")
			pk = bytes(dimLine, "ascii") + line
			ss.sendall(pk)
			i = i + 1
			if (i == (int(nChunk) - 1)):
				line = f.read(const.LENGTH_PACK - (int(lenPart) % const.LENGTH_PACK))
				dimLine = tfunc.format_string(str(len(line)), const.LENGTH_NCHUNK, "0")
				pk = bytes(dimLine, "ascii") + line
				ss.sendall(pk)
				break

# >> PEER
def find_file_by_md5(md5):
	file_list = os.listdir(const.FILE_COND)
	for filef in file_list:
		if not filef.endswith('~'):
			md5File = hashlib.md5(open(const.FILE_COND + filef,'rb').read()).hexdigest()
			if str(md5, "ascii") == md5File:
				return filef
	return const.ERROR_FILE
