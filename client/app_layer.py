from socket import *

class AppLayer:
    def __init__(self):
        self.id = self.get_id()
    #Client id
    def get_id(self):
        mysock = socket(AF_INET, SOCK_STREAM)
        #Handshaking
        mysock.connect(('127.0.0.1', 9000))
        msg_id = 'get_id'
        mysock.send(msg_id.encode())
        my_id = mysock.recv(9).decode()
        mysock.close()
        return my_id
    #Send message to server
    def send_receive(self, msg):
        mysock = socket(AF_INET, SOCK_STREAM)
        #Handshaking
        mysock.connect(('127.0.0.1', 9000))
        #Send char + id
        if msg[0] == 'ping':
            mysock.send(msg[1][0].encode() + self.id.encode())
        #Send "receive back last char sent" request
        elif msg[0] == 'recover':
            msg[0] = 're' + self.id
            mysock.send(msg[0].encode())
        #Receive back char
        data = mysock.recv(1)
        print('Echo:', data.decode())
        mysock.close()
    

