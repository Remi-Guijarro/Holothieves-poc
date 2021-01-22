
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem4301')
print("Communication Successfully started")


#Joystick
a0_joystick = board.get_pin('a:0:i')
a1_joystick = board.get_pin('a:1:i')
isVentFinished = False

#Keypad
pos = 0
password = ['1', '2', '3', '4']
test = ['0', '0', '0', '0']
isVerified = True

#Alarm
d0_alarm = board.get_pin('d:3:p')
d1_alarm = board.get_pin('d:5:o')
isAlarmOn = False

#WaterSensor
a3_waterSensor = board.get_pin('a:3:i')
isWet = True
sensorLimit = 0.1

#Card
isCard = True

#Button
d0_button = board.get_pin('d:4:i')
isButtonPressed = True

def joystick_xy():
    xValue = a0_joystick.read()
    yValue = a1_joystick.read()
    print(xValue)
    print(yValue)
    return [xValue, yValue]

def on_message_received(*args, **kwargs):
    if len(args) == 0:
        return
    c = chr(args[0])
    if c == 'x' and isCard == False:
        on_card_received()
    elif isVerified == False:
        on_key_received(c)

def send_keypad_command():
    board.send_sysex(0x08, [])
    
def send_card_command():
    board.send_sysex(0x09, [])

def on_key_received(c):
    global test, pos, isVerified
    if c == '*':
        print("remise à 0")
        pos = 0
        test = ['0', '0', '0', '0']
        return False
    test[pos] = c
    pos = pos + 1
    if pos == 4:
        if test[0] == password[0] and test[1] == password[1] and test[2] == password[2] and test[3] == password[3]:
            isVerified = True
            isAlarmOn = True
            isWet = False
            print("verified")
            return True
        else:
            print("failed")
            pos = 0
            test = ['0', '0', '0', '0']
            return False


def on_card_received():
    global isCard
    isCard = True
    print("Open")
    return True


def trigger_alarm():
    d0_alarm.write(0.5)
    d1_alarm.write(1)
    time.sleep(1)
    d0_alarm.write(0.1)
    d1_alarm.write(0)


def waterSensor():
    sensorValue = a0.read()
    if sensorValue > sensorLimit:
        print("in_water")
        isWet = True
        isAlarmOn = False
        isCard = False
    
    
def button_pressed():
    global isButtonPressed
    value = d0_button.read()
    if value != 0:
        isButtonPressed = True
        return True
    else:
        return False
    

def start_iterator():
    it = pyfirmata.util.Iterator(board)
    it.start()
    board.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, on_message_received)

if __name__ == '__main__':
    #la fonction main est à déplacer dans le serveur TCP
    start_iterator()
    
    print("loop")
    while True:
        time.sleep(0.1)
        
        #attend le casque
        
        if isVentFinished == False:
            xy = joystick_xy()
            #envoie xy au caque
            #change la valeur de isVentFinished à True quand le drone est à la fin du labyrinthe
            #change la valeur de isVerified à False """"""
            
        if isVerified == False:
            send_keypad_command()
            #envoyer un message au casque quand le code est bon
            
        if isAlarmOn:
            trigger_alarm()
            
        if isWet == False:
            waterSensor()
            #envoyer un message au casque quand l'alarme est désactivé
            
        if isCard == False:
            send_card_command()
            #envoyer un message au casque quand la carte est passé
            
        if isButtonPressed:
            if button_pressed():
                #envoyer un message au casque
                print("button pressed")
            
