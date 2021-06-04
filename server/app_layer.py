import trans_layer

class AppLayer:
    #Begin server on port 9000
    def __init__(self, server):
        self.serversocket = trans_layer.TransLayer()
        self.server = server
    def listen(self):
        #Wait for client message then handshake
        (client, address) = self.serversocket.handshake()
        msg = self.serversocket.receivemsg(client, 11).decode()
        print(msg)
        #New client, generate id
        if msg[:6] == 'get_id':
            self.server.clients_count += 1
            self.server.lastReceivedByClient.append(' ')
            self.serversocket.sendmsg(client, str(self.server.clients_count).encode())
        #Recover last char sent by client
        elif 're' in msg:
            self.serversocket.sendmsg(client, self.server.lastReceivedByClient[int(msg[2:])].encode())
        #Send received char back to client
        else:
            self.server.lastReceivedByClient[int(msg[1:])] = msg[0]
            self.serversocket.sendmsg(client, msg.encode())
        self.serversocket.close(client)