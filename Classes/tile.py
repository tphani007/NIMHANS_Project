from Classes.polygon import Polygon

# Considering origin to be top left
class Tile(Polygon):
    def __init__(self, size, x, y, label=""):
        self.size = size
        # Top left corner
        self.x1 = x
        self.y1 = y
        # Bottom right corner
        self.x2 = self.x1 + self.size
        self.y2 = self.y1 + self.size
        self.labelStatus = {}
        vertices = [(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2), (self.x1, self.y1)]
        Polygon.__init__(self, vertices, label)

    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def setVertices(self, x, y):
        # Top left corner
        self.x1 = x
        self.y1 = y
        # Bottom right corner
        self.x2 = self.x1 + self.size
        self.y2 = self.y1 + self.size
        vertices = [(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2), (self.x1, self.y1)]
        Polygon.setVertices(self, vertices)

    def updateLabelStatus(self, poly):
        label = poly.label
        isInsideTile = (self).contained(poly)
        isIntersection = poly.intersection(self)
        isContained = poly.contained(self)
        if (isInsideTile):
            self.labelStatus[label] = 3 # polygon lies inside tile
        elif (isContained):
            self.labelStatus[label] = 0 # tile lies completely inside the boundary of the polygon
        elif (isIntersection):
            self.labelStatus[label] = 1 # tile intersects the boundary of the polygon
        else:
            self.labelStatus[label] = 2 # tile lies completely outside the boundary of the polygon
    
    def getLabelStatus(self):
        return self.labelStatus