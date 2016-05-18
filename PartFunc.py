import Constant as const
import FileStruct as fs

# >> PEER
def add_to_list_owner(md5, lenFile, lenPart, listPartOwned, fileName):
	listPartOwned[bytes(md5, "ascii")] = [fs.create_total_part(lenFile, const.LENGTH_PART), lenFile, lenPart, bytes(fileName, "ascii")]

# >> PEER
def check_presence(nPart, md5, listPartOwned):
	if len(listPartOwned) == 0:
		return False
	if list(listPartOwned[md5][0])[nPart] == "1":
		return True
	else: return False

def calculate_part8(part):
	lenP = int(len(part) / 8)
	if (len(part) % 8) != 0:
		lenP += 1
	return lenP

def calculate_part(lenFile, lenPart):
	lenP = int(int(lenFile) / int(lenPart))
	if (int(lenFile) % int(lenPart)) != 0:
		lenP += 1
	return lenP

