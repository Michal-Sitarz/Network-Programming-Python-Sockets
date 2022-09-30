import socket

# SETUP connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.5", 8088))
print("Connected.")

# Send message to a client
data = client_socket.recv(1024) # receive
message = data.decode()
print(message)

# Receive message from a client
message_back = "Client: Roger, roger."
data = message_back.encode()
client_socket.send(data)


# Close connection
client_socket.close()
print("Connection closed.")