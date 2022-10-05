import socket

print("[ SERVER ]")

# SETUP connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.5", 8088)) # 0.0.0.0 will bind to ALL available IP addresses

server_socket.listen()
print("Waiting for connection...")

connection_socket, address = server_socket.accept()
print("Client connected!")

## Functions
def send_text(sending_socket, text):
    text = text + "\n"
    data = text.encode() # standard UTF-8 encoding (each char into byte)
    sending_socket.send(data)

# Send messages from a server
message = "Server: Thanks for connecting.\nHere's new line message."
send_text(connection_socket, message)
message = "Server: Another message here!\nAnd another new line message."
send_text(connection_socket, message)


# Receive message back to server
data = connection_socket.recv(1024)
message_back = data.decode()
print(message_back)


# Close connections
connection_socket.close()
server_socket.close()
print("Connection closed.")


