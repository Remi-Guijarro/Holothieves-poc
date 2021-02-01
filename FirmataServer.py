
import pyfirmata
import time

board = pyfirmata.Arduino('COM4')
print("Communication Successfully started")


#Joystick
a0_joystick = board.get_pin('a:0:i')
a1_joystick = board.get_pin('a:1:i')
isVentFinished = False

#Keypad
pos = 0
password = ['9', '2', '6', '1']
test = ['0', '0', '0', '0']
isVerified = True

#Alarm
d0_alarm = board.get_pin('d:3:p')
d1_alarm = board.get_pin('d:5:o')
isAlarmOn = False

#WaterSensor
a3_waterSensor = board.get_pin('a:4:i')
isWet = True
isWaterSensorFinished=False
sensorLimit = 0.1
sensor_value = 0

#Card
isCard = True

#Button
d0_button = board.get_pin('d:7:i')
isButtonPressed = False
buttonCanBePressed = False
bothButtonsArePressed=False

#Méthode permettant de lire les valeurs en X et Y du joystick
def joystick_xy():
    xValue = a0_joystick.read()
    yValue = a1_joystick.read()
    #print(xValue)
    #print(yValue)
    return [xValue, yValue]


#Méthode appelée des qu'on reçoit un message provenant de la carte Arduino
def on_message_received(*args, **kwargs):
    print("on_message_received()")

    #Si le message est vide, on ne fait rien
    if len(args) == 0 or args[0]==0:
        return
    c = chr(args[0])

    #Si le message est "x" (veut dire que le capteru RFID a été activé), on lance la méthode de désactivation du RFID
    if c == 'x' and isCard == False:
        print("on_card_received()")
        on_card_received()
    #Si c'est un message provenant du digicode, on lance la méthode de traitement des données venant du digicode
    elif isVerified == False:
        on_key_received(c)

#Méthode permettant d'envoyé un message à la carte Arduino lui disant qu'on veut activer le digicode
def send_keypad_command():
    while isVerified==False:
        board.send_sysex(0x08, [])
        print("KeyPad")

#Méthode permettant d'envoyé un message à la carte Arduino lui disant qu'on veut activer le capteur RFID
def send_card_command():
    global isCard
    while isCard==False:
        board.send_sysex(0x09, [])
        time.sleep(0.5)
    
#Méthode de traitement des données provenant du digicode
def on_key_received(c):
    global test, pos, isVerified, isAlarmOn, isWet
    print("on_key_received()")
    print(c)
    #Si le joueur presse la touche '*', on réinitialise le code en cours
    if c == '*':
        print("remise à 0")
        pos = 0
        test = ['0', '0', '0', '0']
        return False
    test[pos] = c
    pos = pos + 1
    #Si le digicode à renvoyé 4 valeurs d'affillé
    if pos == 4:
        print("pos=4")
        #On regarde si c'est le bon code qui a été entré
        if test[0] == password[0] and test[1] == password[1] and test[2] == password[2] and test[3] == password[3]:

            isAlarmOn = True
            isWet = False
            isVerified = True
            print("verified")
            return True
        #Sinon, on attend un autre code
        else:
            print("failed")
            pos = 0
            test = ['0', '0', '0', '0']
            return False

#Méthode appelée lorsque le capteur RFID a été actionné
def on_card_received():
    global isCard
    isCard = True
    print("Open")
    return True

#Méthode permettant de lancer l'alarme réelle (LED rouge + active buzzer)
def trigger_alarm():
    while isAlarmOn:
        d0_alarm.write(0.5)
        d1_alarm.write(1)
        time.sleep(0.4)
        d0_alarm.write(0.1)
        d1_alarm.write(0)
        time.sleep(0.2)
    d0_alarm.write(0)
    return

#Méthode permettant de traiter les données venant du water sensor
def waterSensor():
    global isAlarmOn, isWet, isWaterSensorFinished, sensor_value, buttonCanBePressed
    #Si le water sensor n'a pas encore été activé
    while isWet==False:
        time.sleep(0.2)
        #On lit sa valeur
        sensor_value = a3_waterSensor.read()
        print(sensor_value)
        #Si sa valeur est supérieure au seuil choisi, On dit que le water sensor a été activé
        if sensor_value > sensorLimit:
            print("in_water")
            isWet = True
            isWaterSensorFinished = True
            isAlarmOn = False
            buttonCanBePressed = True

#Méthode permettant de stream le bouton réel (afin de détecter si les 2 boutons ont été appuyé pile en meme temps)
def button_pressed():
    global isButtonPressed, buttonCanBePressed, isCard, bothButtonsArePressed
    #Si les 2 boutons n'ont pas encore été appuyés en même temps
    while not bothButtonsArePressed:
        #On lit la valeur du bouton sur l'Arduino
        value = d0_button.read()
        print("value :", value)
        #Si sa valeur est False (i.e. on est en traind d'appuyer sur le bouton)
        if value == False:
            isButtonPressed = True
            #buttonCanBePressed=False
            isCard = False
            print("Button_OK")
        else:
            isButtonPressed=False
    return


#Méthode permettant d'initialisé la communication pyfirmata entre le serveur et l'arduino
def start_iterator():
    it = pyfirmata.util.Iterator(board)
    it.start()
    board.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, on_message_received)


            
        
        
        
        

