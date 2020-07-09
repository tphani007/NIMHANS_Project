# class Rectangle:
#     def __init__(self, x1, y1, x2, y2):
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2

#     def setCoordinates(self, x1, y1, x2, y2):
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2
        
#     def getCoordinates(self):
#         return [(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2)]

#     def getBoundary(self):
#         min_x = min([self.x1,self.x2])
#         max_x = max([self.x1,self.x2])
#         min_y = min([self.y1,self.y2])
#         max_y = max([self.y1,self.y2])
#         return [(min_x,min_y),(max_x,min_y),(max_x,max_y),(min_x,max_y)]
    
#     def checkPoint(self,x,y):
#         if(self.x1<x<self.x2 and self.y1<y<self.y2): # Inside
#             return 0
#         elif((x==self.x1 and self.y1<=y<=self.y2) or (x==self.x2 and self.y1<=y<=self.y2) or (y==self.y1 and self.x1<=x<=self.x2) or (y==self.y2 and self.x1<=x<=self.x2)):
#             return 1 # Boundary
#         return -1 # Outside

#     def checkTile(self,i,j,x,y):
#         x_1 = (i-1)*x
#         x_2 = i*x
#         y_1 = (j-1)*y
#         y_2 = j*y

#         count = []

#         count.append(self.checkPoint(x_1,y_1))
#         count.append(self.checkPoint(x_2,y_1))
#         count.append(self.checkPoint(x_2,y_2))
#         count.append(self.checkPoint(x_1,y_2))
        
#         if(count==0):
#             return "Inside"
#         elif(count==1):
#             return "Inside Intersecting"
#         elif(count==2):
#             return "Overlap"
#         elif(count==-1 or count==-2):
#             return "Intersect"
#         else:
#             return "Outside"
# from shapely.geometry import Polygon
import shapely
from Classes.polygon import Polygon

class Rectangle(Polygon):
    def __init__(self, vertices, label = ""):
        self.x1 = vertices[0][0]
        self.x2 = vertices[1][0]
        self.y1 = vertices[0][1]
        self.y2 = vertices[2][1]
        Polygon.__init__(self, vertices, label)

    def getArea(self):
        length = abs(self.x1 - self.x2)
        width = abs(self.y1 - self.y2)
        return length*width

    def getBounds(self):
        min_x = min([self.x1,self.x2])
        max_x = max([self.x1,self.x2])
        min_y = min([self.y1,self.y2])
        max_y = max([self.y1,self.y2])
        return (min_x, min_y, max_x, max_y)

    def pointLocation(self, x, y):
        if((x == self.x1 and self.y1 <= y <= self.y2) or (x == self.x2 and self.y1 <= y <= self.y2) or (y == self.y1 and self.x1 <= x <= self.x2) or (y == self.y2 and self.x1 <= x <= self.x2)):
            return 1 # Boundary
        elif(self.x1 < x < self.x2 and self.y1 < y < self.y2): # Inside
            return 0 # Inside
        return -1 # Outside


    
        

