# 發布者（publisher）指令稿 publisher1.py
import paho.mqtt.client as mqtt
import time
Pub_IP="10.210.129.111"
#Pub_IP="10.13.116.7"
Pub_Port=1883
Pub_Topic="12A/SMG/P5LAB"
Pub_Msq="00048963 pub1 1sec"


# 建立 MQTT Client 物件
client = mqtt.Client()

# 設定登入帳號密碼（若無則可省略）
#client.username_pw_set("myuser","mypassword")

# 連線至 MQTT 伺服器（伺服器位址,連接埠）
client.connect(Pub_IP, Pub_Port)

# 發布訊息至 自定義 主題
while True:
	client.publish(Pub_Topic, Pub_Msq)
	time.sleep(1)
