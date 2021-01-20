
import pyfirmata
import time

boardKeypad = pyfirmata.Arduino('/dev/cu.usbmodem4301')
#boardRFID = pyfirmata.Arduino('/dev/cu.usbmodem4301')
print("Communication Successfully started")

pos = 0
password = ['1', '2', '3', '4']
test = ['0', '0', '0', '0']
isVerified = False

isCard = False

isWet = False
sensorLimit = 0.1

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


if __name__ == '__main__':
    a0 = boardKeypad.get_pin('a:0:i')
        
    itKeypad = pyfirmata.util.Iterator(boardKeypad)
    itKeypad.start()
    
    #itRFID = pyfirmata.util.Iterator(boardRFID)
    #itRFID.start()
    
    boardKeypad.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, on_key_received)
    #boardRFID.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, on_card_received)
    
    
    
    print("loop")
    while True:
        time.sleep(0.1)
        #if isVerified == False:
            #boardKeypad.send_sysex(0x08, [])
        #if isCard == False:
            #boardRFID.send_sysex(0x09, [])
        if isWet == False:
            sensorValue = a0.read()
            print(sensorValue)
            if sensorValue > sensorLimit:
                print("in_water")
                isWet = True
