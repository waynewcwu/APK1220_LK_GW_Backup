import time
import json
import datetime
from FTPLIB import ftpsend
from configparser import ConfigParser
import paho.mqtt.client as mqtt
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
#import subprocess

#StopSevCMD = "sudo -S service FA_WaterLeak stop"

#log init
log_filename = datetime.datetime.now().strftime("./log/%Y-%m-%d_%H_%M.log")
#log_filename = datetime.datetime.now().strftime("/usr/local/bin/00048963/FA_WaterLeak/log/%Y-%m-%d_%H_%M.log")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    handlers = [TimedRotatingFileHandler(filename =log_filename ,when="D",interval=1,backupCount=30)]
                    )

#Define ENS message file
leakEvent = './WaterLKEvent.txt'
recoverEvent = "./recoverEvent.txt"
cinfig_path = "./appsettings.txt"
#leakEvent = '/usr/local/bin/00048963/FA_WaterLeak/WaterLKEvent.txt'
#recoverEvent = "/usr/local/bin/00048963/FA_WaterLeak/recoverEvent.txt"
#cinfig_path = "/usr/local/bin/00048963/FA_WaterLeak/appsettings.txt"
Configloader = ConfigParser()
Configloader.read(cinfig_path)

MQTTServerIP = Configloader["MQTT"]["ip"]
MQTTServerPort = int(Configloader["MQTT"]["port"])
MQTTTopic = Configloader["MQTT"]["topic"]
MQTTTopic = MQTTTopic.split(",")

def writeEventDoc(path,msg):
    newData = ""
    with open(path,"r",encoding="utf-8") as file:
        data =  file.read()
        newData = data[:data.find(":")+1]+str(msg)+data[data.find("."):]
    with open(path,"w",encoding="utf-8") as file:
        file.write(newData)
def on_connect(client,userdata,flags,rc):
    print("Connected with result code :"+str(rc))
    for topic in MQTTTopic:
        client.subscribe(topic)
        print("broker:%s Listen to %s"%(MQTTServerIP,topic))
        
def on_message(client,userdata,msg):
    try:
        print(msg.topic)
        data = msg.payload.decode()
        print(data)
        data = json.loads(data)
        if(data['Status']=="Leak"):
        #if(data['Status1']=="OK"):
            print("detect Water Leak")
            writeEventDoc(leakEvent,data['location'])
            ftpsend(leakEvent)
        if(data['Status']=="Recovery_OK"):
            writeEventDoc(recoverEvent,data['location'])
            print("recover")
            ftpsend(recoverEvent)
    except Exception as e:
        print(e)
 
def mqtt_client():
    mqttc = mqtt.Client("mqttClient")
    # ~ mqttc.username_pw_set("smgarc1","arc1")
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(MQTTServerIP, MQTTServerPort)
    mqttc.loop_forever()

if __name__ == '__main__':
#	if len(sys.argv) > 1 and sys.argv[1] =="stop":
#		subprocess.run(StopSevCMD, shell=True, check=True, input=b"12345678\n")
#		logging.info("Stop lightdm.")
#		sys.exit(0)
	
	mqtt_client()


