import Constant as const
import TextFunc as tfunc
import Login as logi
import Logout as logo
import Add as add
import Search as src

# MENU

while True:
	print ("\n\nScegli azione PEER:\nlogin\t - Login\nquit\t - Quit\n\n")
	choice = input()

	if (choice == "login" or choice == "l"):
		tfunc.warning("\nP2P >> PEER LOGIN")
		sessionID = logi.login()
		if sessionID != bytes(const.ERROR_LOG, "ascii"):
			tfunc.success("Session ID: " + str(sessionID, "ascii"))

			while True:
				print ("\n\nScegli azione PEER LOGGATO:\nadd\t - Add File\nsearch\t - Search and Download\nlogout\t - Logout\n\n")
				choice_after_log = input()

				if (choice_after_log == "add" or choice_after_log == "a"):
					tfunc.warning("\n>>> ADD FILE")
					fileName = input("Quale file vuoi inserire?\n")
					if fileName is not "0":
						add.add(fileName, ip, sessionID, ipTracker)

				elif (choice_after_log == "search" or choice_after_log == "s"):
					tfunc.warning("\n>>> SEARCH")
					query = input("\nInserisci il nome del file da cercare: ")
					while(len(query) > const.LENGTH_QUERY):
						tfunc.error("Siamo spiacenti ma accettiamo massimo 20 caratteri.")
						query = input("\nInserisci il nome del file da cercare: ")
					src.search()

				elif (choice_after_log == "logout" or choice_after_log == "l"):
					logo.logout(ip, ipTracker, sessionID)
					break

				else:
					tfunc.error("Wrong Choice!")

		else:
			tfunc.error("Errore Login")	

	elif (choice == "quit" or choice == "q"):
		break

	else:
		tfunc.error("Wrong Choice")