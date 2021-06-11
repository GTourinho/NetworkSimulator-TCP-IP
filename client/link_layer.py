from socket import *
from random import randint

#This is just where the (real socket of) simulator is running
s = ('127.0.0.1',9000)

class LinkLayer:
    def __init__(self):
        self.myMac = self.randomMacGenerator()
        self.arp_table = {}
        print('Client mac:', self.myMac)

    def handshake(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(s)

    def randomMacGenerator(self):
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (randint(0, 255), randint(0, 255),
                             randint(0, 255), randint(0, 255),
                             randint(0, 255),
                             randint(0, 255))

    def send(self, packet):
        destinyIp = packet[17:]
        if destinyIp == b'255.255.255.255' or destinyIp not in self.arp_table:
            destinyMac = b'FF:FF:FF:FF:FF:FF'
        else:
            destinyMac = self.arp_table[destinyIp]
        frame = self.myMac.encode()
        frame += destinyMac
        packet += frame
        self.socket.send(packet)

    def receive(self):
        packet = self.socket.recv(66)
        
        packet, frame = packet[:32], packet[32:]
        originMac, destinyMac = frame[:17], frame[17:].decode()

        if originMac not in self.arp_table:
            originIp = packet[2:17]
            self.arp_table[originIp] = originMac

        if destinyMac == self.myMac:
            return packet

        elif destinyMac == 'FF:FF:FF:FF:FF:FF':
            return packet

        self.close()
        return None    

    def close(self):
        self.socket.close()