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
	print(str(text).rjust(shutil.get_terminal_size((80, 20))[0]))

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