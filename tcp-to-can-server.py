import socket
import os
import can

# CAN initialization
def can_set_normal():
    os.system('sudo ip link set can0 type can bitrate 1000000')
    os.system('sudo ifconfig can0 up')
    print("CAN port initialized")

def can_set_loopback():
    os.system('sudo ip link set can0 down')
    os.system('sudo ip link set can0 type can bitrate 1000000 loopback on')
    os.system('sudo ip link set can0 up type can bitrate 1000000')
    print("CAN port initialized (loopback mode)")

can_set_loopback()
can0 = can.interface.Bus(channel='can0', bustype='socketcan') #SocketCAN native

print("Starting [TCP-to-CAN server]")
## SERVER start-up
server_ipaddress = "0.0.0.0" # 0.0.0.0 binds to ALL available IP addresses
server_port = 3090

# Connection setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ipaddress, server_port)) 
server_socket.listen()
print("Waiting for TCP connection...")

(client_socket, client_address) = server_socket.accept()
print("TCP client connected!")

## SERVER functions
def send_text(sending_socket, text):
    text = text + "\n"
    data = text.encode() # standard UTF-8 (each char into byte)
    sending_socket.send(data)

def get_can_data(message):
    if(len(message) > 8):
        message = message[:8]
    encoded_for_can = message.encode('ascii')
    can_data = bytearray(encoded_for_can)
    return can_data

try:
    while True:
        ## Rx (TCP)
        data = client_socket.recv(1024)
        message_decoded = data.decode()
        print(">> Message received: ", message_decoded)

        # Tx (CAN)
        print("Sending CAN message...")
        can_data = get_can_data(message_decoded)
        can_msg = can.Message(arbitration_id=0x123, data=can_data, is_extended_id=False)
        #can_msg = can.Message(arbitration_id=0x123, data=[0,1,2,3,4,5,6,7,8,9], is_extended_id=False)
        can0.send(can_msg)
        print("CAN message sent.")

        # Tx (TCP)
        # message_sent = "Message acknowledged"
        # send_text(client_socket, message_sent)
except Exception as e: 
    print(e)
finally:
    ## SERVER shut-down
    client_socket.close()
    server_socket.close()
    print("[TCP-to-CAN server] Connections closed.")
