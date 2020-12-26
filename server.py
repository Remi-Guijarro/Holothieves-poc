import socket
import serial

#Serial takes these two parameters: serial device and baudrate
ser = serial.Serial('/dev/ttyACM0', 115200)

def write_command_to_arduino(command):
    ser.write(command)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM ->  specifies datagram (udp) sockets.
    port = 30000
    s.bind(("", port))
    print("waiting on port:", port)
    while 1:
        data, addr = s.recvfrom(1024)
        print(data)
        write_command_to_arduino(data)
