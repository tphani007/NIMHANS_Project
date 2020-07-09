import xml.etree.ElementTree as ET

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    v = []
    for region in root.findall("./Annotation/Regions/Region"):
        temp = []
        label = region.get("Text").replace(" ", "") + region.get("Id")
        temp.append(region.get("Type"))
        temp.append(label)
        for vertex in region.findall("./Vertices/Vertex"):
            x = vertex.get("X")
            y = vertex.get("Y")
            temp.append([x,y])
        v.append(temp)
    dest = xmlfile[:-4] + "_" + str(v[0][2][0]) + "_" + str(v[0][2][1]) + "_" + str(v[0][4][0]) + "_" + str(v[0][4][1]) + ".txt"
    f = open(dest,"w")
    for i in range(len(v)):
        f.write(str(v[i][0]) + " ")
        f.write(str(v[i][1]) + " ")
        for j in range(2,len(v[i])):
            f.write(str(v[i][j][0]) + " " + str(v[i][j][1]) + " ")
        f.write("\n")

    return dest

if __name__ == "__main__":
    input_file = input("Enter the name of the xml file that has to be parsed: ")
    output_file = input("Enter the name of the output file: ")
    parseXML(input_file, output_file)
