from socket import *
from time import perf_counter
import select
from random import random
from random import randint

class TransLayer:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.ack_table = []
    def handshake(self, ip, port):
        self.socket.connect((ip, port))
    #Selective-Repeat
    def sendmsg(self, message):
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
                        #checksum is the inverse of the byte
                        checksum = ~byte
                        if random() > 0.5:
                            packet = byte.to_bytes(1, byteorder ='little', signed = True)
                        else:
                            packet = randint(0,127).to_bytes(1, byteorder ='little', signed = True)
                        packet += checksum.to_bytes(1, byteorder ='little', signed = True)
                        packet += id.to_bytes(1, byteorder ='little', signed = True)
                        self.socket.send(packet)
                #check if any ack received, then update ack table
                received_ack, _, _ = select.select([self.socket], [], [], ackTimeout)
                if received_ack:
                    byteId = self.socket.recv(1)
                    self.ack_table[int.from_bytes(byteId, 'little')] = True
        endMessage = '***'
        self.socket.send(endMessage.encode())
    def receivemsg(self, n):
        msg = self.socket.recv(n)
        return msg
    def close(self):
        self.socket.close()