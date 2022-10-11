# TCP Server
import socket

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(("0.0.0.0", 8081))

tcp_server.listen()
connection_socket, address = tcp_server.accept()

data = connection_socket.recv(1024)
connection_socket.send(data)

################################################################

# UDP Server
import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("0.0.0.0", 20001))

data, client_address = udp_server.recvfrom(1024)
udp_server.sendto(data, client_address)
