import logging
import subprocess
import time

# Configure logging, including filename and format
logging.basicConfig(filename='./log/display_sw.log', level=logging.INFO, format='%(asctime)s - %(message)s')
#logging.basicConfig(filename='/usr/local/bin/00048963/CheckDisSW/log/display_sw.log', level=logging.INFO, format='%(asctime)s - %(message)s')
WithoutDisConfCMD = "sudo -S cp /usr/share/X11/xorg.conf.d/xorg.conf_bk_no_monitor /usr/share/X11/xorg.conf.d/xorg.conf"
WithDisConfCMD = "sudo -S cp /usr/share/X11/xorg.conf.d/xorg.conf_with_monitor /usr/share/X11/xorg.conf.d/xorg.conf"
StoplightdmCMD = "sudo -S service lightdm stop"
StartlightdmCMD = "sudo -S service lightdm start"
def is_display_connected():
	try:
		# Run xrandr command and capture output
		xrandr_output = subprocess.check_output(["xrandr"]).decode("utf-8")
		
		# Check if the output contains a connected display
		return " connected " in xrandr_output
		
	except subprocess.CalledProcessError as e:
		logging.error(f"Error running xrandr: {e}")
		return False

def Conf_to_Dum_Display():
	try:
		#stop lightdm servce
		subprocess.run(StoplightdmCMD, shell=True, check=True, input=b"12345678\n")
		logging.info("Stop lightdm.")
		time.sleep(3)
		#configure to Dummy
		subprocess.run(WithoutDisConfCMD, shell=True, check=True, input=b"12345678\n")
		logging.info("Set Xrog to Dummy Display.")
		#time.sleep(0.5)
		#start lightdm servce
		subprocess.run(StartlightdmCMD, shell=True, check=True, input=b"12345678\n")
		logging.info("Start lightdm.")
		time.sleep(1)
		#recover back physical configuration
		subprocess.run(WithDisConfCMD, shell=True, check=True, input=b"12345678\n")
		logging.info("Recover back physical configuration, Wait next reboot")
	except subprocess.CalledProcessError as e:
		ogging.info(f"Stop Commamd Error, Error Msg:{e}")

# ~ def Conf_to_Phy_Displaｙ():
# ~ #stop lightdm servce
# ~ try:
# ~ subprocess.run(StoplightdmCMD, shell=True, check=True, input=b"12345678\n")
# ~ logging.info("Stop lightdm.")
# ~ except subprocess.CalledProcessError as e:
# ~ ogging.info(f"Stop Commamd Error, Error Msg:{e}")
# ~ time.sleep(5)
# ~ #configure to Physical
# ~ try:
# ~ subprocess.run(WithDisconfCMD, shell=True, check=True, input=b"12345678\n")
# ~ logging.info("Set Xrog to Physical Display.")
# ~ except subprocess.CalledProcessError as e:
# ~ ogging.info(f"Set Commamd Error, Error Msg:{e}")
# ~ try:
# ~ subprocess.run(StartlightdmCMD, shell=True, check=True, input=b"12345678\n")
# ~ logging.info("Start lightdm.")



if __name__ == "__main__":
	# Write output to the log
	if is_display_connected():
		logging.info("Physical display detected.")

	else:
		logging.info("No physical display detected.")
		Conf_to_Dum_Display()
