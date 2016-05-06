import Constant as const
import FileStruct as fs

# >> PEER
def add_to_list_owner(md5, lenFile, listPartOwned):
	listPartOwned[md5] = fs.create_total_part(lenFile, const.LENGTH_PART)

# >> PEER
def check_presence(nPart, md5, listPartOwned):
	if listPartOwned[md5][nPart - 1] == "1":
		return True
	else: return False