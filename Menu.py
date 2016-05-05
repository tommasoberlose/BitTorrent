import Constant as const
import TextFunc as tfunc
import Login as logi
import Logout as logo
import Add as add
import Search as src
import Daemon as daemon

# MENU

def menu(host, T, t_host):
	while True:
		print ("Scegli azione PEER:\nlogin\t - Login\nquit\t - Quit\n\n")
		choice = input()

		if (choice == "login" or choice == "l"):
			t_host, sessionID = logi.login(host, t_host)
			if sessionID != bytes(const.ERROR_LOG, "ascii"):
				tfunc.success("Session ID: " + str(sessionID, "ascii"))

				daemonThreadP = daemon.PeerDaemon(host)
				daemonThreadP.setName("DAEMON PEER")
				daemonThreadP.start()

				while True:
					print ("\n\nScegli azione PEER LOGGATO:\nadd\t - Add File\nsearch\t - Search and Download\nlogout\t - Logout\n\n")
					choice_after_log = input()

					if (choice_after_log == "add" or choice_after_log == "a"):
						add.add(host, sessionID, t_host)

					elif (choice_after_log == "search" or choice_after_log == "s"):
						src.search(sessionID, host, t_host)

					elif (choice_after_log == "logout" or choice_after_log == "l"):
						if (logo.logout(host, t_host, sessionID) > 0):
							break

					else:
						tfunc.error("Wrong Choice!")

			else:
				tfunc.error("Errore Login")	

		elif (choice == "quit" or choice == "q"):
			logo.quit(host)
			break

		else:
			tfunc.error("Wrong Choice")