from socket import *

class TransLayer:
    def __init__(self):
        #TCP
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('localhost',9000))
        self.socket.listen(5)
    def handshake(self):
        return self.socket.accept()
    def receivemsg(self, client, n):
        return client.recv(11)
    def sendmsg(self, client, msg):
        client.sendall(msg)
    def close(self, client):
        client.shutdown(SHUT_WR)