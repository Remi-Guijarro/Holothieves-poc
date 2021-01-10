
import serial
import time

#Serial takes these two parameters: serial device and baudrate
ser = serial.Serial('/dev/cu.usbmodem2401', 115200, write_timeout=4)

def write_command_to_arduino(command):
    ser.write(command.encode())

def read_command_from_arduino():
    return ser.readline().decode("utf-8").strip()

if __name__ == "__main__":
    isMessageSent = False
    while 1:
        message = read_command_from_arduino()
        if message == "in_water" and isMessageSent == False:
            isMessageSent = True
            write_command_to_arduino('ok\n')
            print("In Water bis")