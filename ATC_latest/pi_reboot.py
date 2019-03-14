import time
import logging
import os
import subprocess

os.system("sudo rm reboot.log")
os.system("sudo rm atc.log")
os.system("sudo rm algo.log")

logging.basicConfig(filename='/home/pi/atc-module/reboot.log')

minutes = 60

if __name__ == '__main__':
	timeout = time.time() + 60*minutes
	while(1):
		x =int((timeout - time.time())/60)
		if x == minutes-1:
			string = "Minutes left:" + str(x)
			logging.warning(string)
			minutes = minutes - 1
		if time.time() > timeout:
			logging.warning("Rebooting")
			os.system("sudo reboot")

