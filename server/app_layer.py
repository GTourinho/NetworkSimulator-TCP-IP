from socket import *

class AppLayer:
    def __init__(self, server):
        self.serversocket = socket(AF_INET, SOCK_STREAM)
        self.serversocket.bind(('localhost',9000))
        self.serversocket.listen(5)
        self.server = server
        
    def listen(self):
        (clientsocket, address) = self.serversocket.accept()
        msg = clientsocket.recv(11).decode()
        if msg == 'get_id':
            self.server.clients_count += 1
            self.server.lastReceived.append(' ')
            clientsocket.sendall(str(self.server.clients_count).encode())
        elif 're' in msg:
            clientsocket.sendall(self.server.lastReceived[int(msg[2:])].encode())
        else:
            self.server.lastReceived[int(msg[1:])] = msg[:1]
            clientsocket.sendall(msg.encode())
        clientsocket.shutdown(SHUT_WR)

