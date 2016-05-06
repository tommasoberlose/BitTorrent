import string

# Crea una stringa contenente tutte le parti a 1
def create_total_part(lenFile, lenPart):
	k = int(int(lenFile)/int(lenPart))
	if (int(lenFile) % int(lenPart)) > 0:
		k += 1 
	return "1" * k 

class FileStruct:
	
	# In teoria i dati salvati qui dentro dovrebbero essere byte
	def __init__(self, filename, lenFile, lenPart, sessionIDUploader):
		self.filename = filename
		self.lenFile = lenFile
		self.lenPart = lenPart
		self.sessionIDUploader = sessionIDUploader
		self.listOwner = {}
		self.nPart = 0
		#self.listOwner[sessionIDUploader] = create_total_part(lenFile, lenPart) # [[sessionID1, parti], [sessionID2, parti], ecc ecc] le parti sono una stringa
		#self.nPart = len(self.listOwner[sessionIDUploader])

	# Funzione di stampa 
	def printStruct(self):
		print("\n")
		print("File:")
		print(str(self.filename, "ascii") + str(self.lenFile, "ascii") + str(self.lenPart, "ascii"))
		print("\n")
		print("ID dell'utente che l'ha caricato:")
		print(str(self.sessionIDUploader, "ascii"))
		print("\n")
		print("Lista owner:")
		print(self.listOwner)
		print("\n")

	def add_owner(self, sessionID, part):
		self.listOwner[sessionID] = part

	def add_owner_total(self):
		self.listOwner[self.sessionIDUploader] = create_total_part(self.lenFile, self.lenPart)
		self.nPart = len(self.listOwner[self.sessionIDUploader])

	# Funzione che ritorna le parti per un dato sessionID (relativo a un file)
	# Se non c'è ritorna False	
	# Il controllo funziona a byte
	def get_part_by_sessionID(self, sessionID):
		if sessionID in self.listOwner:
			return self.listOwner[sessionID]
		else:
			return False
 
def update_memory(sessionID, md5, partN, listFile):
	file = listFile[md5]
	memory_of_user = file.listOwner[sessionID]
	sl = list(memory_of_user)
	sl[partN - 1] = '1'
	file.listOwner[sessionID] = "".join(sl)
	nPart = count_part(file.listOwner[sessionID])
	return pack.answer_update_tracker(nPart)

def count_part(s):
	sl = list(s)
	part = 0
	for i in sl:
		part += int(i)
	return part
		 
def get_part_for_logout(sessionID, listFile):
	listF = []
	listHitpeer = []
	nPart = 0
	ndPart = 0
	listF = list(listFile.values())
	for file in listF:
		listHitpeer = list(file.listOwner.items())
		actual_str = file.listOwner[sessionID]
		nPart += count_part(file.listOwner[sessionID])
		for peer in listHitpeer:
			if peer[0] != sessionID:
				actual_str = tfunc.count_sub_string(actual_str, peer[1])
				if count_part(actual_str) == 0:
					break
		ndPart += count_part(actual_str) 		

	return nPart, ndPart


def find_file_from_string(listFile, query):
	listFounded = []
	listF = list(listFile.items())
	for file in listF:
		if query in file[1].filename:
			listFounded.append([file[0], file[1].filename, file[1].lenFile, file[1].lenPart])

	return listFounded

def find_hitpeer_from_md5(listFile, listUsers, sessionID, md5):
	file = listFile[md5]
	listFounded = []
	listP = list(file.listOwner.items())
	for part in listP:
		if part[0] != sessionID:
			listFounded.append([listUsers[sessionID][0], listUsers[sessionID][1], part[1]])

	return listFounded


def get_bytes_from_partlist(part):
	partS = ""
	lenP = len(part) / 8
	if (len(part) % 8) != 0:
		lenP += 1
	for x in range(0, lenP):
		partS += chr(int(part[x:x+8], 2))
	return partS