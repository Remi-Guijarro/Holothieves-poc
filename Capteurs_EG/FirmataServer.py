
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem4301') # declare arduino board with serial communication port

print("Communication Successfully started")

if __name__ == '__main__':
    it = pyfirmata.util.Iterator(board)
    it.start()
    
    while True:
        
