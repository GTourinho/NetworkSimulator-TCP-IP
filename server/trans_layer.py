from socket import *

class TransLayer:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('localhost',9000))
        self.socket.listen(5)
    def handshake(self):
        return self.socket.accept()
    def receivemsg(self, client, n):
        messageTable = [None] * n
        byteMessage = bytearray()
        done = False
        while not done:
            packet = client.recv(3)
            message, checksum, ackId = packet
            #if endmessage
            if message == 42 and checksum == 42 and ackId == 42:
                done = True
            #validate the checksum
            elif message + checksum == 255:
                messageTable[ackId] = message
                ack = chr(ackId).encode()
                self.sendmsg(client, ack)
        for byte in messageTable:
            if byte == None:
                break
            byteMessage.append(byte)
        return byteMessage
    def sendmsg(self, client, msg):
        client.sendall(msg)
    def close(self, client):
        client.shutdown(SHUT_WR)