from shapely.geometry import Polygon as SPoly
from shapely.geometry import Point as SPoint

class Polygon(object):
    def __init__(self, vertices, label=""):
        self.label = label
        self.vertices = vertices
        self.polygon = SPoly(vertices)

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def getArea(self):
        return (self.polygon).area

    def setVertices(self, vertices):
        self.vertices = vertices
        self.polygon = SPoly(vertices)

    def getVertices(self):
        return self.vertices

    def intersection(self, poly):
        return (self.polygon).intersects(poly.polygon)

    def contained(self, poly):
        return (self.polygon).contains(poly.polygon)

    def getBounds(self):
        return (self.polygon).bounds

    def pointLocation(self, x, y):
        point = SPoint(x, y)
        if ((self.polygon).touches(point)):
            return 1 # Boundary
        elif ((self.polygon).contains(point)):
            return 0 # Inside
        else:
            return 2 # Outside