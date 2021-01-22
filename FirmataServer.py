
import pyfirmata
import time





def on_key_received(*args, **kwargs):
    global test, pos, isVerified
    if isVerified:
        return
    c = chr(args[0])
    print('#', c)
    if c == '*':
        print("remise à 0")
        pos = 0
        test = ['0', '0', '0', '0']
        return
    test[pos] = c
    pos = pos + 1
    if pos == 4:
        if test[0] == password[0] and test[1] == password[1] and test[2] == password[2] and test[3] == password[3]:
            isVerified = True
            print("verified")
        else:
            print("failed")
        pos = 0
        test = ['0', '0', '0', '0']


def on_card_received(*args, **kwargs):
    global isCard
    if len(args) > 0:
        c = chr(args[0])
        if c == 'x':
            isCard = True
            print("Open")


def trigger_alarm():
    alarmBoard.digital[3].mode = pyfirmata.OUTPUT  # set digital pin to output mode
    alarmBoard.digital[5].mode = pyfirmata.OUTPUT
    BUZZER_PIN = alarmBoard.get_pin('d:3:p')  # set digital pin 3 to pwn communication
    BUZZER_PIN.write(0.5)  # analog write equivalent
    alarmBoard.digital[5].write(1)  # digital write equivalent
    time.sleep(1)
    BUZZER_PIN.write(0.1)
    alarmBoard.digital[5].write(0)


if __name__ == '__main__':
    #a0 = boardKeypad.get_pin('a:0:i')

    a0 = boardJoystick.get_pin('a:0:i')
    a1 = boardJoystick.get_pin('a:1:i')

    itJoystick = pyfirmata.util.Iterator(boardJoystick)
    itJoystick.start()
        
    #itKeypad = pyfirmata.util.Iterator(boardKeypad)
    #itKeypad.start()
    
    #itRFID = pyfirmata.util.Iterator(boardRFID)
    #itRFID.start()
    
    #boardKeypad.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, on_key_received)
    #boardRFID.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, on_card_received)
    
    
    
    print("loop")
    while True:
        time.sleep(0.1)
        #if isVerified == False:
            #boardKeypad.send_sysex(0x08, [])
        #if isCard == False:
            #boardRFID.send_sysex(0x09, [])
        #if isWet == False:
        #    sensorValue = a0.read()
        #    print(sensorValue)
        #if sensorValue > sensorLimit:
        #        print("in_water")
        #        isWet = True
        if isVentFinished==False:
            xValue = a0.read()
            yValue = a1.read()
            print(xValue)
            print(yValue)
        #if isAlarmOn:
            #trigger_alarm()

