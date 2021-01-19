
import pyfirmata
import time
import serial

board = pyfirmata.Arduino('/dev/cu.usbmodem4301') # declare arduino board with serial communication port
ser = serial.Serial('/dev/cu.usbmodem4301', 115200, write_timeout=4)
print("Communication Successfully started")

def _messageHandler(self, *args, **kwargs):
    print(pyfirmata.util.two_byte_iter_to_str(args))
    
def read_command_from_arduino():
    return ser.readline().decode("utf-8").strip()

#Keypad
#row
#r1 = board.get_pin('d:11:i')
#r2 = board.get_pin('d:10:i')
#r3 = board.get_pin('d:9:i')
#r4 = board.get_pin('d:8:i')
#rows = [r1, r2, r3, r4]
#print("rows")

#col
#c1 = board.get_pin('d:5:i')
#c2 = board.get_pin('d:4:i')
#c3 = board.get_pin('d:3:i')
#c4 = board.get_pin('d:2:i')
#cols = [c1, c2, c3, c4]
#print("cols")

m = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
    ]
    
#pos = 0

#password = ['1', '2', '3', '4']
#isSuccessful = False

if __name__ == '__main__':
#Keypad start initialisation
    # Start iterator to receive input data
    it = pyfirmata.util.Iterator(board)
    it.start()
    
#    board.add_cmd_handler(pyfirmata.pyfirmata.STRING_DATA, _messageHandler)
    
#    for r in rows:
#        r.mode = pyfirmata.INPUT
#    for c in cols:
#        c.mode = pyfirmata.INPUT
#Keypad end initialisation
    
    while True:
        time.sleep(1)
        print(read_command_from_arduino())
        #print(board.readline())
        
