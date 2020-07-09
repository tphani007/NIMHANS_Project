from Visualize.parseXML import *
from Visualize.genTilesForRoi import *
from Visualize.labelStatus import *
from Visualize.createXML import *

class VisualizeTiles(object):
    def __init__(self, xml_filename, tilesize):
        self.xml_filename = xml_filename
        self.tilesize = tilesize

    def setXMLFilename(self, filename):
        self.xml_filename = filename

    def getXMLFilename(self):
        return self.xml_filename

    def setTilesize(self, tilesize):
        self.tilesize = tilesize

    def getTilesize(self):
        return self.tilesize

    def parseXMLContents(self):
        self.roi_filename = parseXML(self.xml_filename)

    def getROITiles(self):
        roi = getROI(self.roi_filename)
        return getTiles(roi, self.tilesize)

    def getAnnotations(self):
        return makeAnnotations(self.roi_filename)

    def updateTileStatus(self, tiles, label, annotations):
        poly = None
        for annotation in annotations:
            if (annotation.getLabel() == label):
                poly = annotation
                break
        self.output_file = self.roi_filename[:-4] + "_status_" + label + ".txt"
        updateStatus(tiles, poly, self.output_file)

    def generateXML(self):
        genXML(self.output_file, self.tilesize)

    def run(self, label):
        self.parseXMLContents()
        tiles = self.getROITiles()
        annotations = self.getAnnotations()
        self.updateTileStatus(tiles, label, annotations)
        self.generateXML()

if __name__ == "__main__":
    processing = VisualizeTiles("sample002_dual.xml", 256)
    # processing.parseXMLContents()
    # tiles = processing.getROITiles()
    # annotations = processing.getAnnotations()
    # processing.updateTileStatus(tiles, "rect5", annotations)
    # processing.generateXML()
    processing.run("rect5")    
    

    


    

    


    