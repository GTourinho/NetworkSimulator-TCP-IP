from socket import *
import select
from random import random
from random import randint
import network_layer

class TransLayer:
    def __init__(self):
        self.socket = network_layer.NetworkLayer()

    def handshake(self):
        return self.socket.handshake()

    def receivemsg(self, client, n):
        messageTable = [None] * n
        byteMessage = bytearray()
        done = False
        while not done:
            packet = self.socket.receive(client)
            if packet is None: return None
            packet, originIp = packet
            if packet == b'get': continue
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
                self.sendack(client, ack, originIp)
        for byte in messageTable:
            if byte == None:
                break
            byteMessage.append(byte)
        return byteMessage, originIp

    def sendack(self, client, msg, destinyIp):
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
        self.socket.send(client, packet, destinyIp)

    def sendmsg(self, client, msg, destinyIp):
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
            received_ack, _, _ = select.select([self.socket.linkLayer.socket], [], [], ackTimeout)
            try:
                self.socket.send(client, packet, destinyIp)
            except:
                done = True
            if received_ack: done = True
            
    def close(self, client):
        self.socket.close(client)