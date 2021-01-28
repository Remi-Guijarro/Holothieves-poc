import socket
#import importlib

import pyfirmata
import _thread
import time

import FirmataServer
from FirmataServer import *
#import FirmataServer as firmataServer


#import serial
#from serial import *

#stopLoopVerified = False;

keypadMsgSent=False
waterMsgSent=False
alarmActivated=False
buttonMSGSent=False
rfidMSGSent=False




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

            #print('#'+client_msg+'#')

        except:
            #print("except")
            client_msg = ""
        if client_msg == "stop_read_joystick":
            print("stop_read_joystick")
            #write_command_to_arduino("stop_joystick_read\n")
            FirmataServer.isVentFinished = True
            FirmataServer.isVerified = False
            client_socket.setblocking(True)
            break
        else:
            #arduino_data = ser.readline()
            xValue , yValue = joystick_xy()
            string = str(xValue)+";"+str(yValue)
            print(string)
            data = bytes(string, 'utf-8')
            #print(arduino_data)
            mysend(client_socket, data)
            #print("ok")
    return
















            


if __name__ == "__main__":

    PORT = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', PORT))
    print("waiting on port:", PORT)
    server_socket.listen(5)
    client, address = server_socket.accept()
    print("{} connected".format(address))

    start_iterator()

    #Joystick
    #a0 = boardJoystick.get_pin('a:0:i')
    #a1 = boardJoystick.get_pin('a:1:i')
    #itJoystick = pyfirmata.util.Iterator(boardJoystick)
    #itJoystick.start()


    while 1:
        time.sleep(0.1)
        #msg = myreceive(client)
        client.setblocking(False)
        msg=""
        try:
            msg = client.recv(1024)
            msg = msg.decode("utf-8").strip()
            print("msg : "+msg)
        except:
            client_msg = ""


        #msg = client.recv(1024)
        #msg = msg.decode("utf-8")



        #print(msg)
        #print("b'read_joystick'")

        if msg == "read_joystick" and FirmataServer.isVentFinished==False:
            print("read_joystick")
            joystick_streaming(client)
            #print("sortie joystick_streaming")
        #if FirmataServer.isVerified and stopLoopVerified==False:
        #   print("code bon")
        #    stopLoopVerified=True

        if FirmataServer.isVerified==False and FirmataServer.isVentFinished==True:
            _thread.start_new_thread(send_keypad_command, ())
        if FirmataServer.isWet==False and FirmataServer.isVerified==True:
            _thread.start_new_thread(waterSensor, ( ))
            #print("waterSensor")
        if FirmataServer.isAlarmOn and not alarmActivated:
            _thread.start_new_thread(trigger_alarm, ())
            alarmActivated=True
            print(alarmActivated)

        if FirmataServer.buttonCanBePressed:
            print("button")
            _thread.start_new_thread(button_pressed, ())

        if FirmataServer.isCard==False and FirmataServer.buttonCanBePressed==False and msg=="read_RFID":
            print("RFID")
            _thread.start_new_thread(send_card_command, ())


        #if FirmataServer.isCard == False:
        #    send_card_command()

        #FirmataServer.sensor_value = FirmataServer.a3_waterSensor.read()
        #print(FirmataServer.sensor_value)

        if FirmataServer.isVentFinished==True and FirmataServer.isVerified==True and keypadMsgSent==False:
            str = "Keypad_OK"
            keypad_data = bytes(str, 'utf-8')
            mysend(client, keypad_data)
            keypadMsgSent=True
        if FirmataServer.isWaterSensorFinished and waterMsgSent==False:
            #print("Send()")
            str = "Water_"
            water_data = bytes(str, 'utf-8')
            mysend(client, water_data)
            waterMsgSent=True
        if FirmataServer.isButtonPressed and buttonMSGSent==False:
            str = "Button_"
            button_data = bytes(str, 'utf-8')
            mysend(client, button_data)
            buttonMSGSent = True
        if FirmataServer.isCard and FirmataServer.isButtonPressed and rfidMSGSent==False:
            print("Send RFID")
            str = "RFID_"
            rfid_data = bytes(str, 'utf-8')
            mysend(client, rfid_data)
            rfidMSGSent==True

        #if FirmataServer.isWet==True and FirmataServer.isCard==True:
        #    mysend(client, "RFID_OK")


        #elif msg == "read_keypad":
        #    print("read_keypad")
        #    keypad_streaming(client)
        #    print("sortie keypad_streaming")
        #elif msg == "disconnection":
        #    print("Close")
        #    client.close()
        #    server_socket.close()
        #    break