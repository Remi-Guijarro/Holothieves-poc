import socket
import serial
import time

#Serial takes these two parameters: serial device and baudrate
ser = serial.Serial('/dev/ttyACM0', 500000, write_timeout=4)

def write_command_to_arduino(command):
    ser.write(command.encode())

def joystick_streaming(socket_info):
    write_command_to_arduino('read_joystick')
    while 1:
        s.setblocking(False)
        try:
            socket_data, addr = s.recvfrom(1024)
            socket_data = socket_data.decode('utf-8')
        except:
            socket_data = ""
        if socket_data == "stop_joystick_read":
            write_command_to_arduino("stop_joystick_read")
            s.setblocking(True)
            return
        else:
            arduino_data = ser.readline()
            print(arduino_data)
            s.sendto(arduino_data,(socket_info[0], socket_info[1])) # send joystick data over udp 


def print_to_lcd(socket_info):
    message_to_print, addr = s.recvfrom(1024)
    print("message to print : " , message_to_print.decode("utf-8"))
    write_command_to_arduino(message_to_print.decode("utf-8"))
    


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM ->  specifies datagram (udp) sockets.
    port = 30000
    s.bind(("", port))
    print("waiting on port:", port)
    while 1:
        socket_data, addr = s.recvfrom(1024)
        socket_data = socket_data.decode('utf-8')
        print(socket_data)
        if socket_data == "read_joystick":
            joystick_streaming(addr)
        if socket_data == "print_lcd":
            write_command_to_arduino("print_lcd")
            print_to_lcd(addr)