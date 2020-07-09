import sys
sys.path.insert(0,'..')

from Classes.polygon import Polygon
from Classes.rectangle import Rectangle
from Classes.tile import Tile
import math
import pickle

def getROI(filename):
    with open(filename, "r") as file:
        line = file.readlines()[0]
        line = line.split()
        p1 = (float(line[2]), float(line[3]))
        p2 = (float(line[4]), float(line[5]))
        p3 = (float(line[6]), float(line[7]))
        p4 = (float(line[8]), float(line[9]))
        vertices = [p1, p2, p3, p4, p1]
        roi = Rectangle(vertices)
        return roi

def getTiles(polygon, tilesize):
    xmin, ymin, xmax, ymax = polygon.getBounds()
    x = (math.floor(xmin/tilesize))
    y = (math.floor(ymin/tilesize))
    X = (math.ceil(xmax/tilesize))
    Y = (math.ceil(ymax/tilesize))
    tiles = []
    for i in range(x, X):
        row = []
        for j in range(y, Y):
            row.append(Tile(tilesize, i*tilesize, j*tilesize))
        tiles.append(row)

    return tiles

if __name__ == "__main__":
    input_roi_file = input("Enter the name of the parsed xml file that contains the rectangular ROI: ")
    output_pkl_file = input("Enter the name of the file into which the tiles will be saved: ")
    retTiles = getTiles(getROI(input_roi_file), 256)
    file = open(output_pkl_file, "wb") 
    pickle.dump(retTiles, file)
