from socket import *
import select
from random import random
from random import randint

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
            ackId, checksum, message = packet       
            bytesum = message + ackId
            while bytesum > 127:
                bytesum += 1
                bytesum = bytesum >> 1
            #if endmessage
            if message == 42 and checksum == 42 and ackId == 42:
                done = True
            #validate the checksum
            elif bytesum + checksum == 255:
                messageTable[ackId] = message
                ack = chr(ackId).encode()
                self.sendack(client, ack)
        for byte in messageTable:
            if byte == None:
                break
            byteMessage.append(byte)
        return byteMessage

    def sendack(self, client, msg):
        msg = int.from_bytes(msg, 'little', signed = True)
        checksum = ~msg
        if random() < 0.8:
            packet = checksum.to_bytes(1, byteorder ='little', signed = True)
        else:
            packet = randint(-127,127).to_bytes(1, byteorder ='little', signed = True)   
        if random() < 0.8:
            packet += msg.to_bytes(1, byteorder ='little', signed = True)
        else:
            packet += randint(-127,127).to_bytes(1, byteorder ='little', signed = True)
        client.sendall(packet)


    def sendmsg(self, client, msg):
        ackTimeout = 0.001
        done = False
        msg = int.from_bytes(msg, 'little', signed = True)
        while not done:
            checksum = ~msg
            if random() < 0.8:
                packet = checksum.to_bytes(1, byteorder ='little', signed = True)
            else:
                packet = randint(-127,127).to_bytes(1, byteorder ='little', signed = True)   
            if random() < 0.8:
                packet += msg.to_bytes(1, byteorder ='little', signed = True)
            else:
                packet += randint(-127,127).to_bytes(1, byteorder ='little', signed = True)    
            received_ack, _, _ = select.select([self.socket], [], [], ackTimeout)
            try:
                client.sendall(packet)
            except:
                done = True
            if received_ack: done = True
            
    def close(self, client):
        client.shutdown(SHUT_WR)