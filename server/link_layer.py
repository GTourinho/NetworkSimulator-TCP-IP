from socket import *
from random import randint
import struct

#This is just where the (real socket of) simulator is running
s = ('127.0.0.1',9000)

class LinkLayer:
    def __init__(self):
        self.myMac = self.randomMacGenerator()
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(s)
        self.socket.listen(5)   
        self.arp_table = {}
        print('Server mac:', self.myMac)

    def handshake(self):
        return self.socket.accept()

    def randomMacGenerator(self):
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (randint(0, 255), randint(0, 255),
                                randint(0, 255), randint(0, 255),
                                randint(0, 255),
                                randint(0, 255))
    def send(self, client, packet):
        destinyIp = packet[17:]
        if destinyIp == b'255.255.255.255' or destinyIp not in self.arp_table:
            destinyMac = b'FF:FF:FF:FF:FF:FF'
        else:
            destinyMac = self.arp_table[destinyIp]
        frame = self.myMac.encode()
        frame += destinyMac
        packet += frame
        client.sendall(packet)

    def receive(self, client):
        packet = client.recv(67)
        
        packet, frame = packet[:33], packet[33:]
        originMac, destinyMac = frame[:17], frame[17:].decode()

        if originMac not in self.arp_table:
            originIp = packet[3:18]
            self.arp_table[originIp] = originMac

        if destinyMac == self.myMac:
            return packet

        elif destinyMac == 'FF:FF:FF:FF:FF:FF':
            return packet

        self.close(client)
        return None    

    def close(self, client):
        client.shutdown(SHUT_WR)