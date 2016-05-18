import Constant as const
import TextFunc as tfunc
import Package as pack
import hashlib
import os
import FileStruct as fs

###### UPLOAD FILE 

# >> PEER
def upload(md5, nPart, ss, listPartOwned, name, addr):
	nomeFile = find_file_by_md5(md5, listPartOwned)
	if nomeFile != const.ERROR_FILE:

		f = open((const.FILE_COND + nomeFile), 'rb')
		lenPart = int(listPartOwned[md5][2])

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
			try:
				line = f.read(const.LENGTH_PACK)
				dimLine = tfunc.format_string(str(len(line)), const.LENGTH_NCHUNK, "0")
				#print(len(line) * int(nChunk))
				pk = bytes(dimLine, "ascii") + line
				ss.sendall(pk)
				i = i + 1
				if (i == (int(nChunk) - 1)):
					line = f.read(const.LENGTH_PACK - (int(lenPart) % const.LENGTH_PACK))
					dimLine = tfunc.format_string(str(len(line)), const.LENGTH_NCHUNK, "0")
					pk = bytes(dimLine, "ascii") + line
					ss.sendall(pk)
					break
			except Exception as e:
				tfunc.write_daemon_error(name, addr[0], "ERRORE UPLAD: {0}".format(e))
				break

		tfunc.write_daemon_success(name, addr[0], "Upload parte " + str(int(nPart)) + " (" + str(fs.count_one_in_part(listPartOwned[md5][0])) + "/" + str(len(listPartOwned[md5][0])) + ")")

# >> PEER
def find_file_by_md5(md5, listPartOwned):
	if md5 in listPartOwned:
		return str(listPartOwned[md5][3], "ascii").strip()
	else:
		return const.ERROR_FILE
