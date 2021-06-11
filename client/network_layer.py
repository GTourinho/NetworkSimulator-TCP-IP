from socket import *
from random import randint
import struct

#This is just where the (real socket of) simulator is running
s = ('127.0.0.1',9000)

class NetworkLayer:
    def __init__(self):
        self.myIp = self.randomIpGenerator()
        print('Client ip:', self.myIp)

    def handshake(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 9000))

    def randomIpGenerator(self):
        myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        while len(myip) != 15:
            myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        return myip

    def send(self, packet, destinyIp):
        datagram = self.myIp.encode()
        datagram += destinyIp
        packet += datagram
        self.socket.send(packet)

    def receive(self):
        packet = self.socket.recv(32)
        
        packet, datagram = packet[:2], packet[2:32]
        originIp, destinyIp = datagram[:15], datagram[15:].decode()

        if destinyIp == self.myIp:
            return packet, originIp

        elif destinyIp == '255.255.255.255':
            self.send(self.myIp.encode(), originIp)

        self.close()
        return None    

    def close(self):
        self.socket.close()