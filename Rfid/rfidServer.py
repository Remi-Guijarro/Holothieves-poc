
import serial
import time

#Serial takes these two parameters: serial device and baudrate

device = '/dev/cu.usbmodem1401'
#'/dev/cu.usbmodem2401'

ser = serial.Serial(device, 115200, write_timeout=4)

def write_command_to_arduino(command):
    ser.write(command.encode())

def read_command_from_arduino():
    return ser.readline().decode("utf-8").strip()

if __name__ == "__main__":
    print("Start")
    isMessageSent = False
    waitForCard = True
    while 1:
        message = read_command_from_arduino()
        if waitForCard:
            write_command_to_arduino('ok\n')
            waitForCard = False
        if message == "Card" and isMessageSent == False:
            isMessageSent = True
            print("Open")