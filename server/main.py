import app_layer

class Server:
    def __init__(self):
        self.lastReceived = []
        self.clients_count = -1
        self.appLayer = app_layer.AppLayer(self)

server = Server()

while 1:
    server.appLayer.listen()

