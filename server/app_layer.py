from socket import *

class AppLayer:
    #Begin server on port 9000
    def __init__(self, server):
        self.serversocket = socket(AF_INET, SOCK_STREAM)
        self.serversocket.bind(('localhost',9000))
        self.serversocket.listen(5)
        self.server = server
    def listen(self):
        #Wait for client message
        (clientsocket, address) = self.serversocket.accept()
        msg = clientsocket.recv(11).decode()
        #New client, generate id
        if msg == 'get_id':
            self.server.clients_count += 1
            self.server.lastReceivedByClient.append(' ')
            clientsocket.sendall(str(self.server.clients_count).encode())
        #Recover last char sent by client
        elif 're' in msg:
            clientsocket.sendall(self.server.lastReceivedByClient[int(msg[2:])].encode())
        #Send received char back to client
        else:
            self.server.lastReceivedByClient[int(msg[1:])] = msg[:1]
            clientsocket.sendall(msg.encode())
        clientsocket.shutdown(SHUT_WR)

