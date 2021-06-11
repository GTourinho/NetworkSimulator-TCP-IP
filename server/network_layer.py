from socket import *
from random import randint
import struct

#This is just where the (real socket of) simulator is running
s = ('127.0.0.1',9000)

class NetworkLayer:
    def __init__(self):
        self.myIp = self.randomIpGenerator()
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(s)
        self.socket.listen(5)   

    def handshake(self):
        return self.socket.accept()

    def randomIpGenerator(self):
        myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        while len(myip) != 15:
            myip = inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))
        return myip

    def send(self, client, packet, destinyIp):
        datagram = self.myIp.encode()
        datagram += destinyIp
        packet += datagram
        client.sendall(packet)

    def receive(self, client):
        packet = client.recv(33)
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
        client.shutdown(SHUT_WR)