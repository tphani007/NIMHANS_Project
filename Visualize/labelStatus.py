import sys
sys.path.insert(0,'..')

from Classes.polygon import Polygon
from Classes.rectangle import Rectangle
from Classes.ellipse import Ellipse
from Classes.tile import Tile
import math
import pickle

def makeAnnotations(filename):
    annotations = []
    with open(filename, "r") as file:
        lines = file.readlines()[1:]
        for line in lines:
            line = line.split()
            type_name = line[0]
            label = line[1]
            if (type_name == "1"):            
                p1 = (float(line[2]), float(line[3]))
                p2 = (float(line[4]), float(line[5]))
                p3 = (float(line[6]), float(line[7]))
                p4 = (float(line[8]), float(line[9]))
                vertices = [p1, p2, p3, p4, p1]
                annotation = Rectangle(vertices, label) 
                annotations.append(annotation)
            elif (type_name == "2"):
                x1 = float(line[2])
                y1 = float(line[3])
                x2 = float(line[4])
                y2 = float(line[5])
                annotation = Ellipse(x1, y1, x2, y2, label)
                annotations.append(annotation)
            else:
                i = 2
                vertices = []
                while (i < len(line)):
                    vertex = (float(line[i]), float(line[i+1]))
                    vertices.append(vertex)
                    i += 2
                annotation = Polygon(vertices, label)
                annotations.append(annotation)
        return annotations

def updateStatus(tiles, poly, filename):
    with open(filename, "w") as file:
        label = poly.getLabel()
        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                tiles[i][j].updateLabelStatus(poly)
                topleftX, topleftY = tiles[i][j].getVertices()[0]
                status = tiles[i][j].getLabelStatus()[label]
                if (status == 0 or status == 3):
                    file.write(str(topleftX) + " " + str(topleftY) + " " + "Inside\n")
                elif (status == 1):
                    file.write(str(topleftX) + " " + str(topleftY) + " " + "On\n")
                else:
                    file.write(str(topleftX) + " " + str(topleftY) + " " + "Outside\n")
    
if __name__ == "__main__":
    input_file = input("Enter the name of the parsed xml file that contains the annotations: ")
    tile_file = input("Enter the name of the file that contains the files: ")
    output_file = input("Enter the name of the parsed xml file that contains the annotations: ")
    poly = makeAnnotations(input_file)[0]
    file = open(tile_file, "rb")
    tiles = pickle.load(file)
    # for i in range(len(tiles)):
    #     for j in range(len(tiles[0])):
    #         tiles[i][j].updateLabelStatus(poly)
    #         dicti = tiles[i][j].getLabelStatus()
    #         label = poly.getLabel()
    #         status = dicti[label]
    #         print("i =", i, "j =", j, "status =", status)
    updateStatus(tiles, poly, output_file)


