import app_layer

appLayer = app_layer.AppLayer()

while 1:
    msg = input().lower().split()
    appLayer.send_receive(msg)
