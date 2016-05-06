import TextFunc as tfunc
import Function as func
import Constant as const

# COSTANTI

CODE_LOOK = "LOOK"
CODE_ANSWER_LOOK = "ALOO"

CODE_FIND_PART = "FCHU"
CODE_ANSWER_FIND_PART = "AFCH"

CODE_DOWNLOAD = "RETP"
CODE_ANSWER_DOWNLOAD = "AREP"

CODE_UPDATE_PART = "RPAD"
CODE_ANSWER_UPDATE_PART = "APAD"

CODE_LOGIN = "LOGI"
CODE_ANSWER_LOGIN = "ALGI"

CODE_ADDFILE = "ADDR"
CODE_ANSWER_ADDFILE = "AADR"

CODE_LOGOUT = "LOGO"
CODE_ANSWER_LOGOUT = "ALGO"
CODE_LOGOUT_DENIED = "NLOG"

CODE_CLOSE = "QUIT"
CODE_CONFIRM = "CONF"


# FUNZIONI

# PKT LOGIN
def request_login(ip):
	port = tfunc.format_string(const.PORT, const.LENGTH_PORT, "0")
	pack = bytes(CODE_LOGIN, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") 
	return pack

def answer_login():
	sessionID = func.random_string(const.LENGTH_SESSIONID);
	pack = bytes(CODE_ANSWER_LOGIN, "ascii") + bytes(sessionID, "ascii")
	return pack

def answer_login_old_user(sessionID):
	pack = bytes(CODE_ANSWER_LOGIN, "ascii") + sessionID
	return pack

# PKT ADD FILE
def request_add_file(sessionID, lenFile, md5, fileName):
	lenFile = tfunc.format_string(str(lenFile), const.LENGTH_LENFILE, " ")
	lenPart = tfunc.format_string(str(const.LENGTH_PART), const.LENGTH_LENPART, " ")
	fileName = tfunc.format_string(fileName, const.LENGTH_FILENAME, " ")
	pack = bytes(CODE_ADDFILE, "ascii") + sessionID + bytes(lenFile, "ascii") + bytes(lenPart, "ascii") + bytes(fileName, "ascii") + bytes(md5, "ascii") 
	return pack

def answer_add_file(nPart):
	nPart = tfunc.format_string(str(nPart), const.LENGTH_NPART, "0")
	pack = bytes(CODE_ANSWER_ADDFILE, "ascii") + bytes(nPart, "ascii")
	return pack

# PKT SEARCH FASE 1

def request_look(sessionID, query):
	query = tfunc.format_string(query, const.LENGTH_QUERY, " ")
	pack = bytes(CODE_LOOK, "ascii") + sessionID + bytes(query, "ascii")
	return pack

def answer_look(listFounded):
	nidmd5 = len(listFounded)
	pack = bytes(CODE_ANSWER_LOOK, "ascii") + bytes(tfunc.format_string(str(nidmd5), const.LENGTH_NIDMD5, "0"), "ascii") 
	for x in range(0, nidmd5):
		pack += listFounded[x][0] + listFounded[x][1] + listFounded[x][2] + listFounded[x][3]
	return pack

# PKT SEARCH FASE 2

def request_hitpeer(sessionID, md5):
	pack = bytes(CODE_FIND_PART, "ascii") + sessionID + md5
	return pack

def answer_hitpeer(listFounded):
	nHitPeer = len(listFounded)
	pack = bytes(CODE_ANSWER_FIND_PART, "ascii") + bytes(tfunc.format_string(str(nHitPeer), const.LENGTH_NIDMD5, "0"), "ascii") 
	for x in range(0, nHitPeer):
		pack += bytes(listFounded[x][0], "ascii") + bytes(listFounded[x][1], "ascii") + bytes(fs.get_bytes_from_partlist(listFounded[x][2]), "ascii")
	return pack

# PKT LOGOUT
def request_logout(sessionID):
	pack = bytes(CODE_LOGOUT, "ascii") + sessionID
	return pack

def answer_logout(nPart):
	nPart = tfunc.format_string(str(nPart), const.LENGTH_ITEM_REMOVED, "0")
	pack = bytes(CODE_ANSWER_LOGOUT, "ascii") + bytes(nPart, "ascii")
	return pack

def reject_logout(nPart):
	nPart = tfunc.format_string(str(nPart), const.LENGTH_ITEM_REMOVED, "0")
	pack = bytes(CODE_LOGOUT_DENIED, "ascii") + bytes(nPart, "ascii")
	return pack

# PKT CLOSE PROGRAM
def close():
	return bytes(CODE_CLOSE, "ascii")

# PKT CONFIRM DAEMON
def confirm():
	return bytes(CODE_CONFIRM, "ascii")

# PKT DOWNLOAD
def request_download(md5, partNum):
	partNum = tfunc.format_string(str(partNum), const.LENGTH_NPART, "0")
	pack = bytes(CODE_DOWNLOAD, "ascii") + md5 + bytes(partNum, "ascii")
	return pack

def answer_download(): # DA FARE
	pack = ""
	return pack

# PKT UPDATE TRACKER
def request_update_tracker(sessionID, md5, partNum):
	partNum = tfunc.format_string(str(partNum), const.LENGTH_NPART, "0")
	pack = bytes(CODE_UPDATE_PART, "ascii") + sessionID + md5 + bytes(partNum, "ascii")
	return pack

def answer_update_tracker(nPart):
	nPart = tfunc.format_string(str(nPart), const.LENGTH_ITEM_REMOVED, "0")
	pack = bytes(CODE_ANSWER_UPDATE_PART, "ascii") + bytes(nPart, "ascii")
	return pack