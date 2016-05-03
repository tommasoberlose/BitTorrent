# COSTANTI

CODE_QUERY = "QUER"
CODE_ANSWER_QUERY = "AQUE"

CODE_SEARCH = "FIND"
CODE_ANSWER_SEARCH = "AFIN"

CODE_NEAR = "NEAR"
CODE_ANSWER_NEAR = "ANEA"

CODE_DOWNLOAD = "RETR"
CODE_ANSWER_DOWNLOAD = "ARET"

CODE_SN = "SUPE"
CODE_ANSWER_SN = "ASUP"

CODE_LOGIN = "LOGI"
CODE_ANSWER_LOGIN = "ALGI"

CODE_ADDFILE = "ADFF"
CODE_REMOVEFILE = "DEFF"

CODE_LOGOUT = "LOGO"
CODE_ANSWER_LOGOUT = "ALGO"

CODE_CLOSE = "QUIT"



# FUNZIONI

# PKT SN
def request_sn(ip, port):
	pk_id = func.random_pktid(const.LENGTH_PKTID)
	port = func.format_string(port, const.LENGTH_PORT, "0")
	step = func.format_string(const.TTL_SN, const.LENGTH_TTL, "0")
	pack = bytes(const.CODE_SN, "ascii") + bytes(pk_id, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") + bytes(step, "ascii")
	return pack

def answer_sn(pk_id, ip):
	port = func.format_string(const.PORT_SN, const.LENGTH_PORT, "0")
	pack = bytes(const.CODE_ANSWER_SN, "ascii") + pk_id + bytes(ip, "ascii") + bytes(port, "ascii")
	return pack


def forward_sn(pack):
	step = modify_ttl(pack[80:82])
	if step != 0:
		step = func.format_string(str(step), const.LENGTH_TTL, "0")
		pack = pack[0:80] + bytes(step, "ascii")
		return pack
	else: 
		return bytes(const.ERROR_PKT, "ascii")

# PKT LOGIN
def request_login(ip):
	port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	pack = bytes(const.CODE_LOGIN, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") 
	return pack

def answer_login():
	sessionID = func.random_sessionID(const.LENGTH_SESSIONID);
	pack = bytes(const.CODE_ANSWER_LOGIN, "ascii") + bytes(sessionID, "ascii")
	return pack

def request_add_file(sessionID, md5, fileName):
	fileName = func.format_string(fileName, const.LENGTH_FILENAME, " ")
	pack = bytes(const.CODE_ADDFILE, "ascii") + sessionID + bytes(md5, "ascii") + bytes(fileName, "ascii")
	return pack

def request_remove_file(sessionID, md5):
	pack = bytes(const.CODE_REMOVEFILE, "ascii") + sessionID + bytes(md5, "ascii")
	return pack

def request_logout(sessionID):
	pack = bytes(const.CODE_LOGOUT, "ascii") + sessionID
	return pack

def answer_logout(nDelete):
	nDelete = func.format_string(str(nDelete), const.LENGTH_ITEM_REMOVED, "0")
	pack = bytes(const.CODE_ANSWER_LOGOUT, "ascii") + bytes(nDelete, "ascii")
	return pack


# PKT del SN alla rete
def query(ip, query):
	pk_id = func.random_pktid(const.LENGTH_PKTID)
	port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	step = func.format_string(const.TTL, const.LENGTH_TTL, "0")
	query = func.format_string(str(query, "ascii"), const.LENGTH_QUERY, " ")
	pack = bytes(const.CODE_QUERY, "ascii") + bytes(pk_id, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") + bytes(step, "ascii") + bytes(query, "ascii")
	return pack

def forward_query(pack):
	step = modify_ttl(pack[80:82])
	if step > 0:
		step = func.format_string(str(step), const.LENGTH_TTL, "0")
		pack = pack[0:80] + bytes(step, "ascii") + pack[82:]
		return pack
	else: 
		return bytes(const.ERROR_PKT, "ascii")


def answer_query(pktID, ip, port, md5, fileName):
	#port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	fileName = func.format_string(fileName, const.LENGTH_FILENAME, " ")
	return bytes(const.CODE_ANSWER_QUERY, "ascii") + pktID + ip + port + bytes(md5, "ascii") + bytes(fileName, "ascii")

# PKT SEARCH PEER al SN
def request_search(sessionID, query):
	query = func.format_string(query, const.LENGTH_QUERY, " ")
	pack = bytes(const.CODE_SEARCH, "ascii") + sessionID + bytes(query, "ascii")
	return pack

def modify_ttl(step):
	step = int(step)
	step = step - 1
	return step

def close():
	return bytes(const.CODE_CLOSE, "ascii")

def request_download(md5):
	pack = bytes(const.CODE_DOWNLOAD, "ascii") + md5
	return pack
