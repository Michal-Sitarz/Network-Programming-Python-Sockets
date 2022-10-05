import socket

print("[ CLIENT ]")

# SETUP connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.5", 8088))
print("Connected.")

def get_text(receiving_socket):
    buffer = ""

    is_socket_open = True
    while is_socket_open:
        # read any data from the socket
        data = receiving_socket.recv(1024)

        # if no data is returned, the socket must be closed
        if not data:
            is_socket_open = False
        
        # else add the data to the buffer
        buffer += data.decode()

        # is there a "terminator" character in the buffer?
        terminator_index = buffer.find("\n")
        # if index value of terminator is > -1, it means that "\n" must be found/exist
        while terminator_index > -1:
            # get the completed/terminated message from the buffer
            message = buffer[:terminator_index] # all until terminator char
            # remove this message from the buffer
            buffer = buffer[terminator_index+1:] # from terminator char till end
            # yield the message (return a message while continuing the while loop)
            yield message
            # is there another terminator in the buffer?
            terminator_index = buffer.find("\n")


# Receive message in a client
message = next(get_text(client_socket))
print(message)
message = next(get_text(client_socket))
print(message)

# Using below function will hang both client and server (as while loop gets stuck in infinite)
# Uncomment it to run it!
# for message in get_text(client_socket):
#     print(message)

# Send message back from a client
message_back = "Client: Roger, roger."
data = message_back.encode()
client_socket.send(data)


# Close connection
client_socket.close()
print("Connection closed.")