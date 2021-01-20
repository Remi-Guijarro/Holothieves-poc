
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem4301') # declare arduino board with serial communication port
print("Communication Successfully started")

pos = 0
password = ['1', '2', '3', '4']
test = ['0', '0', '0', '0']
isVerified = False

def on_string_received(*args, **kwargs):
    global test, pos, isVerified
    if isVerified:
        return
    c = chr(args[0])
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
    

if __name__ == '__main__':
    it = pyfirmata.util.Iterator(board)
    it.start()
    
    board.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, on_string_received)
    print("loop")
    while True:
        board.send_sysex(0x08, [])
