from parchmint import Device
import sys
import json
from threedprinting.components.port import createPort, makePort
from threedprinting.components.port import makeDroplet
from threedprinting.components.connection import createConnection
from threedprinting.components.box import makeBox
from threedprinting.export import exportToSTL

file_path = sys.argv[1]
print("File Name: " + file_path)
device = None
with open(file_path) as data_file:
    text = data_file.read()
    device_json = json.loads(text)
    device = Device(device_json)

components = []
connections = []

for component in device.components:
    if component.entity == "PORT":
        x = (component.xpos)
        y = (component.ypos)
        print(x,y)
        pos = [x,y,-5]
        port = makePort(pos)
        components.append(port)
    elif component.entity == "NOZZLE DROPLET GENERATOR":
        x = (component.xpos)
        y = (component.ypos)
        print(x,y)
        pos = [x,y,-5]
        droplet = makeDroplet(pos)
        components.append(droplet)
    else:
        x = (component.xpos)
        y = (component.ypos)
        print(x,y)
        pos = [x,y,-5]
        box = makeBox(pos)
        components.append(port)
for connection in device.connections:
    dictionary = connection.__dict__
    waypoints = dictionary["params"].get_param("wayPoints")
    P = []
    for (x,y) in waypoints:
        x = x
        y = y
        P.append((x,y,0))
    
    connectionObject = createConnection(P)
    connections.append(connectionObject)


combined = components + connections
exportToSTL(combined, u"Lshape")
