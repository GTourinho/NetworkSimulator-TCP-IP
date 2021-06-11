from random import randint
from socket import *
import struct
import link_layer

class NetworkLayer:
    def __init__(self):
        self.myIp = self.randomIpGenerator()
        print('Server Ip:', self.myIp)
        self.linkLayer = link_layer.LinkLayer()

    def handshake(self):
        return self.linkLayer.handshake()

    def randomIpGenerator(self):
        myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        while len(myip) != 15:
            myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        return myip

    def send(self, client, packet, destinyIp):
        datagram = self.myIp.encode()
        datagram += destinyIp
        packet += datagram
        self.linkLayer.send(client, packet)

    def receive(self, client):
        packet = self.linkLayer.receive(client)
        packet, datagram = packet[:3], packet[3:33]
        originIp, destinyIp = datagram[:15], datagram[15:].decode()
        if destinyIp == self.myIp:
            return packet, originIp
        elif destinyIp == '255.255.255.255':
            sendIpMsg = 'si'
            self.send(client, sendIpMsg.encode(), originIp)
            return packet, originIp
        self.close(client)
        return None    

    def close(self, client):
        self.linkLayer.close(client)