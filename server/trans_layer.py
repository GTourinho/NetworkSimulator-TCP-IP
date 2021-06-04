from socket import *

class TransLayer:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('localhost',9000))
        self.socket.listen(5)
    def handshake(self):
        return self.socket.accept()
    def receivemsg(self, client, n):
        byteMessage = bytearray()
        done = False
        while not done:
            packet = client.recv(3)
            #if endmessage
            if packet[0] == 42 and packet[1] == 42 and packet[2] == 42:
                done = True
            #validate the checksum
            elif packet[0] + packet[1] == 255:
                byteMessage.insert(packet[2], packet[0])
                ack = chr(packet[2]).encode()
                self.sendmsg(client, ack)
        return byteMessage
    def sendmsg(self, client, msg):
        client.sendall(msg)
    def close(self, client):
        client.shutdown(SHUT_WR)