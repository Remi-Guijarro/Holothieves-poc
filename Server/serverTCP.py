import socket
import pyfirmata
import _thread
import time
import arduinoFirmataClient
from arduinoFirmataClient import *

#Booléens permettant de lancer les différents threads une seule fois
keypadLaunched=False
waterLaunched=False
alarmLaunched=False
buttonLaunched=False
RFIDLaunched=False

#Booléen permettant d'envoyer une seule fois les message de réussite de chaque élément IoT au casque
keypadMsgSent=False
waterMsgSent=False
alarmActivated=False
buttonMSGSent=False
rfidMSGSent=False


#Méthode permettant de faire un envoie de message au client TCP (casque) sans perdre de message
def mysend(client_socket, data):
        totalsent = 0
        MSGLEN = len(data)
        while totalsent < MSGLEN:
            sent = client_socket.send(data[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

#Méthode permettant de faire une réception de message venant du client TCP (casque) sans perdre de message
def myreceive(_socket):
        chunks = []
        MSGLEN = 2048
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = _socket.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

#Méthode gérant le streaming du joystick
def joystick_streaming(client_socket):
    #write_command_to_arduino("read_joystick")

    client_socket.setblocking(False)
    #Tant qu'on ne rencontre pas re "return" ou un "break"
    while 1:
        #Délais permettant de ne pas avoir trop de perte de FPS liée au streaming dans le casque
        time.sleep(0.5)

        #On regarde si le casque nous a envoyé un message
        try:
            client_msg = client_socket.recv(1024)
            #On transform le message en string
            client_msg = client_msg.decode("utf-8").strip()
        except:
            #print("except")
            client_msg = ""
            #Si on a reçu un message du casque "stop_read_joystick"
        if client_msg == "stop_read_joystick":
            print("stop_read_joystick")
            #Ceci veut dire que l'on a fini le labyrinthe donc on change les différents booléens
            arduinoFirmataClient.isVentFinished = True
            arduinoFirmataClient.isVerified = False
            client_socket.setblocking(True)
            #On sort de la méthode (i.e. on arrete de stream le joystick au casque)
            break
        #Si on doit toujours stream le joystick au casque
        else:
            #On appelle la méthode joystick_xy() de FirmataServer.py afin de récupérer les valeurs en X et Y du joystick
            xValue , yValue = joystick_xy()
            #On traite ces valeurs afin de les envoyer au casque
            string = str(xValue)+";"+str(yValue)
            print(string)
            data = bytes(string, 'utf-8')
            #On envoie les valeurs du joystick au casque
            mysend(client_socket, data)

    return


#Méthode "main" appelée à chaque frame
if __name__ == "__main__":
    #On choisit le port sur lequel on va communiquer avec le casque
    PORT = 8888

    #On crée une socket serveur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #On bind la socket serveur sur le port choisis
    server_socket.bind(('', PORT))
    print("waiting on port:", PORT)
    #On place le serveur en mode écoute, il attend donc qu'un client TCP se connecte à lui (le casque)
    server_socket.listen(5)
    #client = socket client TCP, address = adresse IP du client TCP
    client, address = server_socket.accept()
    print("{} connected".format(address))

    start_iterator()

    #On lance une boucle infinie tant que l'on ne s'est pas déconnecté du client
    while 1:
        time.sleep(0.1)

        client.setblocking(False)

        #On essaye de récupérer un message provenant du client TCP
        try:
            msg = client.recv(1024)
            msg = msg.decode("utf-8").strip()
            print("msg : "+msg)
        except:
            msg = ""

        #Si le client nous a envoyé le message "read_joystick"
        if msg == "read_joystick" and arduinoFirmataClient.isVentFinished==False:
            #On lance le streaming du joystick
            print("read_joystick")
            joystick_streaming(client)

        #Si on veut les valeurs du digicode
        if arduinoFirmataClient.isVerified==False and arduinoFirmataClient.isVentFinished==True and keypadLaunched==False:
            print("Keypad launched !")
            _thread.start_new_thread(send_keypad_command, ())
            keypadLaunched = True

        #Si on veut les valeurs du water level sensor
        if arduinoFirmataClient.isWet==False and arduinoFirmataClient.isVerified==True and waterLaunched==False:
            _thread.start_new_thread(waterSensor, ( ))
            waterLaunched=True
            print("water launched !")

        #Si on veut déclencher l'alarme réelle (LED rouge + active buzzer)
        if arduinoFirmataClient.isAlarmOn and not alarmActivated:
            _thread.start_new_thread(trigger_alarm, ())
            alarmActivated=True
            print(alarmActivated)

        #Si on veut streamer le bouton réel
        if arduinoFirmataClient.buttonCanBePressed and arduinoFirmataClient.bothButtonsArePressed==False and buttonLaunched==False:
            print("button")
            _thread.start_new_thread(button_pressed, ())
            buttonLaunched=True

        #Si on reçoit un message du casque disant que les 2 boutons ont été appuyés en meme temps
        if msg=="read_RFID":
            arduinoFirmataClient.bothButtonsArePressed=True
        # Si on veut lancer le capteur RFID
        if arduinoFirmataClient.isCard==False and arduinoFirmataClient.bothButtonsArePressed==True and RFIDLaunched==False: #and msg=="read_RFID":
            print("RFID")
            RFIDLaunched=True
            send_card_command()
        #On gère ici les envoit des différents messages de réussite des éléments IoT au casque afin qu'il puisse déclencher les bonnes actions de jeu
        if arduinoFirmataClient.isVentFinished==True and arduinoFirmataClient.isVerified==True and keypadMsgSent==False:
            str = "Keypad_OK"
            keypad_data = bytes(str, 'utf-8')
            mysend(client, keypad_data)
            keypadMsgSent=True
        if arduinoFirmataClient.isWaterSensorFinished and waterMsgSent==False:
            #print("Send()")
            str = "Water_"
            water_data = bytes(str, 'utf-8')
            mysend(client, water_data)
            waterMsgSent=True
        if arduinoFirmataClient.isButtonPressed and buttonMSGSent==False:
            str = "Button_"
            button_data = bytes(str, 'utf-8')
            mysend(client, button_data)
        if arduinoFirmataClient.isCard and arduinoFirmataClient.bothButtonsArePressed and rfidMSGSent==False:
            rfidMSGSent = True
            print("Send RFID")
            str = "RFID_"
            rfid_data = bytes(str, 'utf-8')
            mysend(client, rfid_data)
        #Si on reçoit le message "disconnection" venant du casque, alors on déconnecte le casque du serveur et on eteint le serveur TCP
        if msg == "disconnection":
            print("Close")
            client.close()
            server_socket.close()
            break

