from socket import *

class TransLayer:
    def __init__(self):
        #TCP
        self.socket = socket(AF_INET, SOCK_STREAM)
    def handshake(self, ip, port):
        self.socket.connect((ip, port))
    def sendmsg(self, message):
        self.socket.send(message)
    def receivemsg(self, n):
        return self.socket.recv(n)
    def close(self):
        self.socket.close()




