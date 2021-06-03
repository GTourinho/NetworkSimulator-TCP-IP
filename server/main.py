import app_layer

class Server:
    def __init__(self):
        self.lastReceivedByClient = []
        self.clients_count = -1
        self.appLayer = app_layer.AppLayer(self)

#Begin server
server = Server()

while 1:
    server.appLayer.listen()