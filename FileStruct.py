import string
import random
import Constant as const
import TextFunc as tfunc
import Package as pack

# Crea una stringa contenente tutte le parti a 1
# >> TRACKER
def create_total_part(lenFile, lenPart):
	k = int(int(lenFile)/int(lenPart))
	if (int(lenFile) % int(lenPart)) > 0:
		k += 1 
	return "1" * k 

# >> PEER
def create_empty_part(lenFile, lenPart):
	k = int(int(lenFile)/int(lenPart))
	if (int(lenFile) % int(lenPart)) > 0:
		k += 1 
	return "0" * k 

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
 
# >> TRACKER
def update_memory(sessionID, md5, partN, listFile):
	file = listFile[md5]
	if not sessionID in file.listOwner:
		file.listOwner[sessionID] = create_empty_part(file.lenFile, file.lenPart)

	listToUpdate = list(file.listOwner[sessionID])
	listToUpdate[int(partN) - 1] = "1"
	file.listOwner[sessionID] = "".join(listToUpdate)
	nPart = count_part(file.listOwner[sessionID])
	return pack.answer_update_tracker(nPart)

# >> PEER, TRACKER
def count_part(s):
	sl = list(s)
	part = 0
	for i in sl:
		part += int(i)
	return part

# >> TRACKER
def get_part_for_logout(sessionID, listFile):
	listF = []
	listHitpeer = []
	nPart = 0
	ndPart = 0
	listF = list(listFile.values())
	for fileC in listF:
		listHitpeer = list(fileC.listOwner.items())
		if sessionID in fileC.listOwner:
			actual_str = fileC.listOwner[sessionID]
			nPart += count_part(fileC.listOwner[sessionID])
			for peer in listHitpeer:
				if peer[0] != sessionID:
					actual_str = tfunc.count_sub_string(actual_str, peer[1])
					if count_part(actual_str) == 0:
						break
			ndPart += count_part(actual_str) 		

	return nPart, ndPart

# >> TRACKER
def find_file_from_string(listFile, sessionID, query):
	listFounded = []
	listF = list(listFile.items())
	for fileC in listF:
		if (sessionID != fileC[1].sessionIDUploader) or (query.strip() == "*"):
			if (query.strip() in str(fileC[1].filename, "ascii")) or (query.strip() == "*"):
				listFounded.append([fileC[0], fileC[1].filename, fileC[1].lenFile, fileC[1].lenPart])

	return listFounded

# >> TRACKER
def find_hitpeer_from_md5(listFile, listUsers, sessionID, md5):
	fileC = listFile[md5]
	listFounded = []
	listP = list(fileC.listOwner.items())
	for part in listP:
		if part[0] != sessionID:
			listFounded.append([listUsers[part[0]][0], listUsers[part[0]][1], part[1]])
	return listFounded

# >> TRACKER
def get_bytes_from_partlist(part):
	partS = ""
	lenP = len(part) / 8
	if (len(part) % 8) != 0:
		lenP += 1
	tfunc.reverse_format_string(part, lenP * 8, "0")
	for x in range(0, int(lenP)):
		partS += chr(int(part[x:x+8], 2))
	print(partS)
	return bytes(partS, "latin")

# >> PEER
def find_part_from_hitpeer(nHitPeer, part, listPartOwned, md5, lenFile, lenPart):
	listPart = {}
	myPart = listPartOwned[md5]
	listHitpeer = []

	print(part)
	
	for n in range(0, nHitPeer):
		pointer = n * (60 + len(myPart))
		ip = part[0 + pointer:55 + pointer]
		port = part[55 + pointer:60 + pointer]
		memory = part[60 + pointer:60 + int(len(myPart)/8) + pointer]
		partList = ""

		for j in range(0, len(memory)):
			partL = bin(ord(memory[j:j+1]))[2:]
			partList += tfunc.reverse_format_string(partL, const.LENGTH_NPART, "0")
			print(partList)

		partList = partList[0:-(8 - ((int(lenFile) / int(lenPart)) % 8))]
		print(((int(lenFile) / int(lenPart)) % 8))
		print(partList)

			
		listHitpeer.append([[ip, port], partList])

	for x in range(0, len(myPart)):
		if list(myPart)[x] == '0':
			listPart[x + 1] = []
			for p in range(0, nHitPeer):
				if list(listHitpeer[p][1])[x] == "1":
					listPart[x + 1].append(listHitpeer[p][0])
				else:
					del listPart[x + 1]
	print(listPart)

	listResult = []
	listPartSorted = sorted(listPart.items(), key=lambda x:len(x[1]))
	for el in listPartSorted:
		listResult.append([el[0], random.choice(el[1])])



	return listResult