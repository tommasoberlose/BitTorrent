import shutil

# COSTANTI

START_RED = "\033[91m"
END_RED = "\033[0m"

START_GREEN = "\033[92m"
END_GREEN = "\033[0m"

START_YELLOW = "\033[93m"
END_YELLOW = "\033[0m"

START_GREY = "\033[90m"
END_GREY = "\033[0m"

#FUNZIONI

def format_string(text, length, char):
	l = len(text)
	dif = length - l
	return char * dif + text 

def reverse_format_string(text, length, char):
	l = len(text)
	dif = length - l
	return text + char * dif

def reformat_string(text):
	return text.strip()

def	write_right_text(text):
	print("")
	print(str(text).rjust(shutil.get_terminal_size((80, 0))[0]))

def write_daemon_error(host, addr, text):
	write_right_text(">>> " + host + " [" + addr + "]: " + START_RED + "ERROR: " + text + END_RED)

def write_daemon_success(host, addr, text):
	write_right_text(">>> " + host + " [" + addr + "]: " + START_GREEN + "SUCCESS: " + text + END_GREEN)

def write_daemon_text(host, addr, text):
	write_right_text(">>>  " + host + " [" + addr + "]: " + text)

def error(text):
	print (START_RED + "Error: " + text + END_RED)

def success(text):
	print (START_GREEN + "Success: " + text + END_GREEN)

def warning(text):
	print (START_YELLOW + text + END_YELLOW)

def gtext(text):
	print (START_GREY + text + END_GREY)

def count_sub_string(s1, s2):
	s1l = list(s1)
	s2l = list(s2)
	for x in range(0, len(s1l)):
		if int(s1l[x]) and not int(s2l[x]):
			s1l[x] = "1"
		else:
			s1l[x] = "0"
	return "".join(s1l)

def format_filename(fileName, ip55):
	for i in range(0, len(fileName)):
		if(fileName[i] == "."):
			fileName = fileName[:i] + ip55[9:11] + ip55[13:15] + fileName[i:]
			break
	return fileName

# TEST
"""
print("Prova format_string 100 caratteri - " + format_string("Ciao", 100, " "))
print("Prova reverse_format_string 100 caratteri - " + reverse_format_string("Ciao", 100, " "))
print("Prova reformat_string - " + reformat_string(format_string("Ciao", 100, " ")))
write_right_text("Prova write_right_text")
write_daemon_error("170:30:1:1", "170:30:2:3", "Prova write_daemon_error")
write_daemon_success("170:30:1:1", "170:30:2:3", "Prova write_daemon_success")
write_daemon_text("170:30:1:1", "170:30:2:3", "Prova write_daemon_text")
error("Prova error")
success("Prova success")
warning("Prova warning")
gtext("Prova gtext")
"""