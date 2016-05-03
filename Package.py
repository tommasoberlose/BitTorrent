import TextFunc as tfunc
improt Function as func

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


# FUNZIONI

# PKT LOGIN
def request_login(ip):
	port = tfunc.format_string(const.PORT, const.LENGTH_PORT, "0")
	pack = bytes(const.CODE_LOGIN, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") 
	return pack

def answer_login():
	sessionID = func.random_sessionID(const.LENGTH_SESSIONID);
	pack = bytes(const.CODE_ANSWER_LOGIN, "ascii") + bytes(sessionID, "ascii")
	return pack

# PKT ADD FILE
def request_add_file(sessionID, md5, fileName):
	fileName = tfunc.format_string(fileName, const.LENGTH_FILENAME, " ")
	pack = bytes(const.CODE_ADDFILE, "ascii") + sessionID + bytes(md5, "ascii") + bytes(fileName, "ascii")
	return pack

def answer_add_file(nPart):
	nPart = tfunc.format_string(str(nPart), const.LENGTH_NPART, "0")
	pack = bytes(const.CODE_ANSWER_ADDFILE, "ascii") + bytes(nPart, "ascii")
	return pack

# PKT SEARCH FASE 1

# PKT SEARCH FASE 2

# PKT LOGOUT
def request_logout(sessionID):
	pack = bytes(const.CODE_LOGOUT, "ascii") + sessionID
	return pack

def answer_logout(nPart):
	nPart = tfunc.format_string(str(nPart), const.LENGTH_ITEM_REMOVED, "0")
	pack = bytes(const.CODE_ANSWER_LOGOUT, "ascii") + bytes(nPart, "ascii")
	return pack

def reject_logout(nPart):
	nPart = tfunc.format_string(str(nPart), const.LENGTH_ITEM_REMOVED, "0")
	pack = bytes(const.CODE_LOGOUT_DENIED, "ascii") + bytes(nPart, "ascii")
	return pack

# PKT CLOSE PROGRAM
def close():
	return bytes(const.CODE_CLOSE, "ascii")

# PKT DOWNLOAD
def request_download(md5, ):
	pack = bytes(const.CODE_DOWNLOAD, "ascii") + md5
	return pack
