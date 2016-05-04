import string

class FileStruct:
	
	# In teoria i dati salvati qui dentro dovrebbero essere byte
	def __init__(self, filename, lenFile, lenParti, sessionIDUploader, listOwner):
		self.filename = filename
		self.lenFile = lenFile
		self.lenParti = lenParti
		self.sessionIDUploader = sessionIDUploader
		self.listOwner = listOwner # [[sessionID1, parti], [sessionID2, parti], ecc]

	# Funzione per aggiungere un possessore alla lista
	def add_owner(self, newOwner):
		self.listOwner.append(newOwner)

	# Funzione di stampa 
	def printStruct(self):
		print("\n")
		print("File:")
		print(str(self.filename, "ascii") + str(self.lenFile, "ascii") + str(self.lenParti, "ascii"))
		print("\n")
		print("ID dell'utente che l'ha caricato:")
		print(str(self.sessionIDUploader, "ascii"))
		print("\n")
		print("Lista owner:")
		print(self.listOwner)
		print("\n")

	# Funzione che ritorna le parti per un dato sessionID (relativo a un file)
	# Se non c'è ritorna False	
	# Il controllo funziona a byte
	def get_part_by_sessionID(self, sessionID):
		for owner in self.listOwner:
			if sessionID == owner[0]:
				return owner[1]
		return False

