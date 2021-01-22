import socket
#import importlib

import pyfirmata
import time

from FirmataServer import *
#import FirmataServer as firmataServer


#import serial
#from serial import *

#boardKeypad = pyfirmata.Arduino('/dev/cu.usbmodem4301')
#boardRFID = pyfirmata.Arduino('/dev/cu.usbmodem4301')
boardJoystick = pyfirmata.Arduino('COM4')
#alarmBoard = pyfirmata.arduino('COM4')
print("Communication Successfully started")


pos = 0
password = ['1', '2', '3', '4']
test = ['0', '0', '0', '0']
isVerified = False

isCard = False

isWet = False
sensorLimit = 0.1


isVentFinished = False

isAlarmOn = False


#importlib.import_module("FirmataServer")

#ser = serial.Serial('COM4', 115200, write_timeout=4)


#def write_command_to_arduino(command):
    #ser.write(command.encode())


def mysend(client_socket, data):
        totalsent = 0
        MSGLEN = len(data)
        while totalsent < MSGLEN:
            sent = client_socket.send(data[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent


def myreceive(_socket):
        chunks = []
        MSGLEN = 2048
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = _socket.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)


def joystick_streaming(client_socket):
    #write_command_to_arduino("read_joystick")

    client_socket.setblocking(False)
    while 1:
        time.sleep(0.5)
        try:
            client_msg = client_socket.recv(1024)

            client_msg = client_msg.decode("utf-8").strip()

            print('#'+client_msg+'#')

        except:
            print("except")
            client_msg = ""
        if client_msg == "stop_read_joystick":
            print("stop_read_joystick")
            write_command_to_arduino("stop_joystick_read\n")
            client_socket.setblocking(True)
            break
        else:
            #arduino_data = ser.readline()
            xValue = a0.read()
            yValue = a1.read()
            print(type(xValue))
            string = str(xValue)+";"+str(yValue)
            print(string)
            data = bytes(string, 'utf-8')
            #print(arduino_data)
            mysend(client_socket, data)
            print("ok")
    return


def keypad_streaming(client_socket):
    write_command_to_arduino("read_keypad")
    client_socket.setblocking(False)
    while 1:
        try:
            client_msg = client_socket.recv(1024)
            client_msg = client_msg.decode("utf-8").strip()
            print('#' + client_msg + '#')
        except:
            print("except")
            client_msg = ""
        if client_msg == "stop_read_keypad":
            print("stop_read_keypad")
            write_command_to_arduino("stop_read_keypad\n")
            client_socket.setblocking(True)
            break
        else:
            #arduino_data = ser.readline()
            print(arduino_data)
            mysend(client_socket, arduino_data)
            print("ok")
    return













            


if __name__ == "__main__":

    PORT = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', PORT))
    print("waiting on port:", PORT)
    server_socket.listen(5)
    client, address = server_socket.accept()
    print("{} connected".format(address))

    #Joystick
    a0 = boardJoystick.get_pin('a:0:i')
    a1 = boardJoystick.get_pin('a:1:i')
    itJoystick = pyfirmata.util.Iterator(boardJoystick)
    itJoystick.start()


    while 1:
        time.sleep(0.1)
        #msg = myreceive(client)

        msg = client.recv(1024)
        msg = msg.decode("utf-8")



        #print(msg)
        #print("b'read_joystick'")
        if msg == "read_joystick":
            print("read_joystick")
            joystick_streaming(client)
            print("sortie joystick_streaming")
        elif msg == "read_keypad":
            print("read_keypad")
            keypad_streaming(client)
            print("sortie keypad_streaming")
        elif msg == "disconnection":
            print("Close")
            client.close()
            server_socket.close()
            break