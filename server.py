import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM ->  specifies datagram (udp) sockets.
port = 30000
s.bind(("", port))
print("waiting on port:", port)
while 1:
	data, addr = s.recvfrom(1024)
	print(data)