
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
password = ['1', '2', '3', '4']
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
isCard = False#True

#Button
#?

def joystick_xy():
    xValue = a0_joystick.read()
    yValue = a1_joystick.read()
    print(a3_waterSensor.read())
    print(xValue)
    print(yValue)
    return [xValue, yValue]



def on_message_received(*args, **kwargs):
    print("on_message_received()")
    print(len(args))
    print(args[0])
    if len(args) == 0 or args[0]==0:
        return
    c = chr(args[0])
    print("c :"+c+"c")
    if c == 'x' and isCard == False:
        print("on_card_received()")
        on_card_received()
    elif isVerified == False:
        on_key_received(c)

def send_keypad_command():
    board.send_sysex(0x08, [])
    print("KeyPad")
    
def send_card_command():
    board.send_sysex(0x09, [])

def on_key_received(c):
    global test, pos, isVerified, isAlarmOn, isWet
    print("on_key_received()")
    print(c)
    if c == '*':
        print("remise à 0")
        pos = 0
        test = ['0', '0', '0', '0']
        return False
    test[pos] = c
    pos = pos + 1
    if pos == 4:
        print("pos=4")
        if test[0] == password[0] and test[1] == password[1] and test[2] == password[2] and test[3] == password[3]:

            isAlarmOn = True
            isWet = False
            isVerified = True
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
    while isAlarmOn:
        d0_alarm.write(0.5)
        d1_alarm.write(1)
        time.sleep(0.4)
        d0_alarm.write(0.1)
        d1_alarm.write(0)
        time.sleep(0.2)
    d0_alarm.write(0)
    return



def waterSensor():
    global isAlarmOn, isWet, isCard, isWaterSensorFinished, sensor_value
    sensor_value = a3_waterSensor.read()
    print(sensor_value)
    if sensor_value > sensorLimit:
        print("in_water")
        isWet = True
        isWaterSensorFinished=True
        isAlarmOn = False
        isCard = False


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
        
        #if isVentFinished == False:
        #    xy = joystick_xy()
            #envoie xy au caque
            #change la valeur de isVentFinished à True quand le drone est à la fin du labyrinthe
            #change la valeur de isVerified à False """"""
            
        #if isVerified == False:
        #    send_keypad_command()
            #envoyer un message au casque quand le code est bon
            
        if isAlarmOn:
            trigger_alarm()
            
        #if isWet == False:
        #    waterSensor()
            #envoyer un message au casque quand l'alarme est désactivé
            
        #if isCard == False:
        #    print("RFID")
        #    send_card_command()
            #envoyer un message au casque quand la carte est passé
            
        #button ?
            
        
        
        
        

