import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Reading the inputs from a txt file
def readInputs(txtfile, grid_size):
    f = open(txtfile, "r")
    
    # The grid values
    x = grid_size
    y = grid_size
    
    values = [] # The tile values
    v = f.readlines() 
    n = len(v)
    for i in range(n):
        temp = v[i].split()
        a = float(temp[0])
        b = float(temp[1])
        c = temp[2]
        if(c=="Inside"):
            c = 0
        elif(c=="On"):
            c = 1
        elif(c=="Outside"):
            c = 2
        values.append([a,b,c])
    
    n = len(values)

    # Converting the (i,j) values of the tiles to Vertices
    for i in range(n):
        c = []
        a = values[i][0]
        b = values[i][1]
        c.append([a,b])
        c.append([a+x,b])
        c.append([x+a,y+b])
        c.append([a,y+b])
        c.append(values[i][2])
        values[i] = c
    
    return values

# Collecting the inputs from a CSV file
def collectInputs(csvfile, filenum, boundFile, grid_size):
    data = pd.read_csv(csvfile)
    fname = []
    truths = []
    
    # Considering the values of a specific file
    for i in range(len(data)):
        j = 0
        while(j<(len(data['filename'][i])-5)):
            if(data['filename'][i][j]+data['filename'][i][j+1]+data['filename'][i][j+2]+data['filename'][i][j+3]+data['filename'][i][j+4]+data['filename'][i][j+5]=="le-002"):
                fname.append(data['filename'][i][60:])
                if(data['TruePositive'][i]==1):
                    truths.append(0)
                elif(data['TrueNegative'][i]==1):
                    truths.append(1)
                elif(data['FalsePositive'][i]==1):
                    truths.append(2)
                elif(data['FalseNegative'][i]==1):
                    truths.append(3)
            j+=1
    
    # Extracting the values from the file names
    values = []
    for i in fname:
        x = ""
        y = ""
        a = ""
        b = ""
        for j in range(len(i)-2):
            if(i[j]+i[j+1]=="-r"):
                k = j+2
                while(i[k]!="-"):
                    x += i[k]
                    k += 1
                k+=2
                while(i[k]!="-"):
                    y += i[k]
                    k += 1
                k+=2
                while(i[k]!="-"):
                    a += i[k]
                    k += 1
                k+=2
                while(i[k]!="-"):
                    b += i[k]
                    k += 1

                x = int(x) # Row value
                y = int(y) # Coloumn value
                a = int(a) # X value of the first index
                b = int(b) # Y value of the first index
                values.append([x,y,a,b])
    
    final = []
    f = open(boundFile,"r")
    temp = f.readlines()
    
    # Getting the offset values corresponding to each file
    if(filenum == "002"):
        temp = temp[0].split()
        h = int(temp[0]) 
        bound_x = int(temp[1])
        bound_y = int(temp[2])
    elif(filenum == "004"):
        temp = temp[1].split()
        h = int(temp[0])
        bound_x = int(temp[1])
        bound_y = int(temp[2])
    elif(filenum == "005"):
        temp = temp[2].split()
        h = int(temp[0])
        bound_x = int(temp[1])
        bound_y = int(temp[2])
    elif(filenum == "006"):
        temp = temp[3].split()
        h = int(temp[0])
        bound_x = int(temp[1])
        bound_y = int(temp[2])

    # Converting the values from Openslide to Imagescope
    for i in range(len(values)):
        temp = []
        actual_x = h - abs(values[i][3]-bound_y)
        actual_y = abs(values[i][2]-bound_x)
        temp.append([actual_x,actual_y])
        temp.append([actual_x+grid_size,actual_y])
        temp.append([actual_x+grid_size,actual_y+grid_size])
        temp.append([actual_x,actual_y+grid_size])
        temp.append(truths[i])
        final.append(temp)
    return final

def makeAnnotation(final, dest, num):
    root = ET.Element("Annotations")
    root.set("MicronsPerPixel","0.500000")

    for j in range(num):
        a1 = ET.Element("Annotation")
        a1.set("Id", str(j+1))
        a1.set("Name","")
        a1.set("ReadOnly","0")
        a1.set("NameReadOnly","0")
        a1.set("LineColorReadOnly","0")
        a1.set("Incremental","0")
        a1.set("Type","4")
        if(j==0):
            a1.set("LineColor","65280")
        elif(j==1):
            a1.set("LineColor","16744448")
        elif(j==2):
            a1.set("LineColor","255")
        elif(j==3):
            a1.set("LineColor","16776960")
        a1.set("Visible","1")
        a1.set("Selected","1")
        a1.set("MarkupImagePath","")
        a1.set("MacroName","")
        root.append(a1)

        b1 = ET.SubElement(a1,"Attributes")
        b2 = ET.SubElement(b1,"Attribute",{"Name":"Description","Id":"0","Value":"",})

        r1 = ET.SubElement(a1,"Regions")
        r2 = ET.SubElement(r1,"RegionAttributeHeaders")
        r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9999","Name":"Region","ColumnWidth":"-1",})
        r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9997","Name":"Length","ColumnWidth":"-1",})
        r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9996","Name":"Area","ColumnWidth":"-1",})
        r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"9998","Name":"Text","ColumnWidth":"-1",})
        r3 = ET.SubElement(r2,"AttributeHeader",{"Id":"1","Name":"Description","ColumnWidth":"-1",})

        # Making the regions to be marked
        for i in range(len(final)):
            if(final[i][4]==j):
                x1 = final[i][0][0]-final[i][1][0]
                x2 = final[i][0][1]-final[i][3][1]
                r = ET.SubElement(r1,"Region",{"Id":str(i+1),
                                                "Type":"1",
                                                "Zoom":"1",
                                                "Selected":"1",
                                                "ImageLocation":"",
                                                "ImageFocus":"-1",
                                                "Length":str(float(2*(x1+x2))),
                                                "Area":str(float(x1*x2)),
                                                "LengthMicrons":str(float(x1+x2)),
                                                "AreaMicrons":str(float((x1*x2)/4)),
                                                "Text":"",
                                                "NegativeROA":"0",
                                                "InputRegionId":"0",
                                                "Analyze":"0",
                                                "DisplayId":str(i+1),})
                att = ET.SubElement(r,"Attributes")
                ver = ET.SubElement(r,"Vertices")
                v1 = ET.SubElement(ver,"Vertex",{"X":str(final[i][0][0]),"Y":str(final[i][0][1]),"Z":"0",})
                v2 = ET.SubElement(ver,"Vertex",{"X":str(final[i][1][0]),"Y":str(final[i][1][1]),"Z":"0",})
                v3 = ET.SubElement(ver,"Vertex",{"X":str(final[i][2][0]),"Y":str(final[i][2][1]),"Z":"0",})
                v4 = ET.SubElement(ver,"Vertex",{"X":str(final[i][3][0]),"Y":str(final[i][3][1]),"Z":"0",})

    tree = ET.ElementTree(root)

    with open(dest, "wb") as files:
        tree.write(files)
    print("XML file created successfully!")

# Used to format an XML file to make it more readable
def formatXML(filename):
    with open(filename) as xmldata:
        xml = minidom.parseString(xmldata.read())
        xml_pretty = xml.toprettyxml()
        f = open(filename,"w")
        f.write(xml_pretty)

# Main function that generates the XML file
def genXML(filename,grid_size):
    if(filename.endswith(".csv")):
        f1 = collectInputs(filename, "002", "bounds.txt", grid_size)
        f2 = collectInputs(filename, "004", "bounds.txt", grid_size)
        f3 = collectInputs(filename, "005", "bounds.txt", grid_size)
        fname = filename[:-4]

        makeAnnotation(f1,fname + "_002.xml", 4)
        makeAnnotation(f2,fname + "_004.xml", 4)
        makeAnnotation(f3,fname + "_005.xml", 4)

        formatXML(fname + "_002.xml")
        formatXML(fname + "_004.xml")
        formatXML(fname + "_005.xml")
        
    elif(filename.endswith(".txt")):
        v = readInputs(filename, grid_size)
        fname = filename[:-4]
        makeAnnotation(v, fname + ".xml", 3)
        formatXML(fname + ".xml")

