import trans_layer

class AppLayer:
    def __init__(self):
        self.transLayer = trans_layer.TransLayer()
        self.id = self.get_id()

    #Client id
    def get_id(self):
        #Handshaking
        self.transLayer.handshake()
        msg_id = 'get_id'
        ip = '255.255.255.255'
        ip = ip.encode()
        self.transLayer.sendmsg(msg_id.encode(), ip)
        my_id, serverIp = self.transLayer.receivemsg()
        my_id = my_id.decode()
        self.serverIp = serverIp.decode()
        self.transLayer.close()
        return my_id
        
    #Send message to server
    def send_receive(self, msg):
        self.transLayer.handshake()
        #Send char + id
        if msg[0] == 'ping':
            self.transLayer.sendmsg(msg[1][0].encode() + self.id.encode(), self.serverIp.encode())
        #Send "receive back last char sent" request
        elif msg[0] == 'recover':
            msg[0] = 're' + self.id
            self.transLayer.sendmsg(msg[0].encode(), self.serverIp.encode())
        #Receive back char
        data, originIp = self.transLayer.receivemsg()
        print('Echo:', data.decode())
        self.transLayer.close()