from socket import *

class AppLayer:
    def __init__(self):
        self.id = self.get_id()
    def get_id(self):
        mysock = socket(AF_INET, SOCK_STREAM)
        mysock.connect(('127.0.0.1', 9000))
        msg_id = 'get_id'
        mysock.send(msg_id.encode())
        my_id = mysock.recv(9).decode() #1b clients max
        mysock.close()
        return my_id
    def send_receive(self, msg):
        mysock = socket(AF_INET, SOCK_STREAM)
        mysock.connect(('127.0.0.1', 9000))
        if msg[0] == 'send':
            mysock.send(msg[1][0].encode() + self.id.encode()) #1ª char se tiver +
        elif msg[0] == 'receive':
            msg[0] = 're' + self.id
            mysock.send(msg[0].encode())
        data = mysock.recv(1)
        print('Caractere: ', data.decode())
        mysock.close()
    

