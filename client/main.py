import app_layer

appLayer = app_layer.AppLayer()

while 1:
    msg = input().split()
    msg[0] = msg[0].lower()
    appLayer.send_receive(msg)
