import sys
import json

sys.path.append("/usr/lib/freecad-python3/lib")
import FreeCAD, Draft, Part
import Mesh

sys.path.append("/home/ubuntu/3DuF-server/partpipeline/threedprinting")
from export import exportToSTL

class Component:
    def __init__(self, obj, entity, position, params):
        '''Add some custom properties to our General Component feature'''
        [x,y,z] = position
        pnt = FreeCAD.Vector(x,y,z)
        
        
        # for key, item in params.items():
        #     print(key, item)
        #     setattr(obj.addProperty("App::PropertyLength", key, entity, key + "of component"), key, item)

        obj.addProperty("App::PropertyString", "Params", entity, "Params of component").Params = json.dumps(params)
        obj.addProperty("App::PropertyPosition", "Position", entity, "Position of component").Position = pnt
        obj.addProperty("App::PropertyString", "Type", entity, "Type of component").Type = entity
        obj.Proxy = self
        obj.Label = "3DuF_Object"

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        # Need error checking for if the file doesn't exist
        myDocument = FreeCAD.open(u"/home/ubuntu/3DuF-server/partpipeline/threedprinting/components/sources/" + fp.Type + u".FCStd")
        sheet = myDocument.getObject("Spreadsheet")
        sketch = myDocument.getObject("Sketch")
        
        for key, item in json.loads(fp.Params).items():
            sheet.set(key, str(item))
        sheet.set("x", str(fp.Position[0]))
        sheet.set("y", str(fp.Position[1]))
        sheet.set("z", str(fp.Position[2]))
        sheet.recompute()
        
        myDocument.recompute()        

        extr = myDocument.Extrude
        fp.Shape = Part.getShape(extr)
        print("here")

def makePort(position, radius=0.005, height=0.010):
    D=FreeCAD.newDocument()
    a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Port")
    params = {"radius": radius, "height":height}
    Component(a, "PORT", position, params)
    D.recompute()
    return a

def makeDroplet(position, waterInputWidth=0.600, oilInputWidth=0.600, orificeSize=0.200,orificeLength=0.300,outputLength=0.600,outputWidth=0.600, height=0.250):
    D = FreeCAD.newDocument()
    a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "DropletGenerator")
    params = {"waterInputWidth": waterInputWidth, "oilInputWidth":oilInputWidth, "orificeSize":orificeSize, "orificeLength":orificeLength,"outputLength":outputLength,"outputWidth":outputWidth,"height":height}
    Component(a, "NOZZLE DROPLET GENERATOR", position, params)
    D.recompute()
    return a

exportToSTL([makePort([0,0,0])], u"Port")
# exportToSTL([makeDroplet([0,0,0])],u"DropletGeneratorComp")