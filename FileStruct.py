import string

class FileStruct:
	
	# In teoria i dati salvati qui dentro dovrebbero essere byte
	def __init__(self, filename, lenFile, lenPart, sessionIDUploader, listOwner):
		self.filename = filename
		self.lenFile = lenFile
		self.lenPart = lenPart
		self.sessionIDUploader = sessionIDUploader
		self.listOwner = listOwner # [[sessionID1, parti], [sessionID2, parti], ecc ecc] le parti sono una stringa

	# Funzione per aggiungere un possessore alla lista
	def add_owner(self, newOwner):
		self.listOwner.append(newOwner)

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

	# Funzione che ritorna le parti per un dato sessionID (relativo a un file)
	# Se non c'è ritorna False	
	# Il controllo funziona a byte
	def get_part_by_sessionID(self, sessionID):
		for owner in self.listOwner:
			if sessionID == owner[0]:
				return owner[1]
		return False

	# Crea una stringa contenente tutte le parti a 1
	def create_total_part(lenFile, lenPart):
		return "1" * int(lenFile/lenPart + 1)

