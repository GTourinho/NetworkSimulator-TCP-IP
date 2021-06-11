from time import perf_counter
import select
from random import random
from random import randint
import network_layer

class TransLayer:
    def __init__(self):
        self.networkLayer = network_layer.NetworkLayer()
        self.ack_table = []
        
    def handshake(self):
        self.networkLayer.handshake()

    #Selective-Repeat
    def sendmsg(self, message, destinyIp):
        if destinyIp.decode() == '255.255.255.255':
            getAddrMsg = 'get'
            self.networkLayer.send(getAddrMsg.encode(), destinyIp)
            packet, destinyIp = self.networkLayer.receive()
        timeout_table = [0] * len(message)
        self.ack_table = [False] * len(message)
        done = False
        ackTimeout = 0.00001
        while not done:
            done = True
            for id, byte in enumerate(message):
                currTime = perf_counter()
                #if not ack and timed out
                if self.ack_table[id] == False:
                    done = False
                    if currTime > timeout_table[id]:
                        timeout_table[id] = perf_counter() + 0.00001
                        #checksum for the packet                   
                        bytesum = id + byte
                        while bytesum > 127:
                            bytesum += 1
                            bytesum = bytesum >> 1
                        checksum = ~bytesum

                        #add id, checksum and byte with random chance of corrupting
                        if random() < 0.8:
                            packet = id.to_bytes(1, byteorder ='little', signed = True)
                        else:
                            packet = randint(-127,127).to_bytes(1, byteorder ='little', signed = True)
                        if random() < 0.8:
                            packet += checksum.to_bytes(1, byteorder ='little', signed = True)
                        else:
                            packet += randint(-127,127).to_bytes(1, byteorder ='little', signed = True)
                        if random() < 0.8:
                            packet += byte.to_bytes(1, byteorder ='little', signed = True)
                        else:
                            packet += randint(-127,127).to_bytes(1, byteorder ='little', signed = True)
                        self.networkLayer.send(packet, destinyIp)

                #check if any ack received, then update ack table
                received_ack, _, _ = select.select([self.networkLayer.linkLayer.socket], [], [], ackTimeout)
                if received_ack:
                    packet, originIp = self.networkLayer.receive()

                    checksum, byteId = packet
                    if byteId + checksum == 255:
                        self.ack_table[byteId] = True

        endMessage = '***'
        self.networkLayer.send(endMessage.encode(), destinyIp)

    def receivemsg(self):
        done = False    
        while not done:
            packet = self.networkLayer.receive()
            packet, originIp = self.networkLayer.receive()
            checksum, msg = packet
            if msg + checksum == 255:
                done = True
                ack = msg.to_bytes(1, byteorder ='little', signed = True)
                self.networkLayer.send(ack, originIp)
        return msg.to_bytes(1, byteorder ='little', signed = True), originIp

    def close(self):
        self.networkLayer.close()