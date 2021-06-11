from random import randint
from socket import *
import struct
import link_layer

class NetworkLayer:
    def __init__(self):
        self.myIp = self.randomIpGenerator()
        print('Client ip:', self.myIp)
        self.linkLayer = link_layer.LinkLayer()

    def handshake(self):
        self.linkLayer.handshake()

    def randomIpGenerator(self):
        myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        while len(myip) != 15:
            myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        return myip

    def send(self, packet, destinyIp):
        datagram = self.myIp.encode()
        datagram += destinyIp
        packet += datagram
        self.linkLayer.send(packet)

    def receive(self):
        packet = self.linkLayer.receive()
        
        packet, datagram = packet[:2], packet[2:32]
        originIp, destinyIp = datagram[:15], datagram[15:].decode()

        if destinyIp == self.myIp:
            return packet, originIp

        elif destinyIp == '255.255.255.255':
            sendIpMsg = 'sin'
            self.send(sendIpMsg.encode(), originIp)

        self.close()
        return None    

    def close(self):
        self.linkLayer.close()