import shapefile

def read(file):
    print("Reading from shapefile " + str(file))
    return shapefile.Reader(shp = file)

def process(sf, anonymizer, decimals,shapefileOut):
    print("Processing the Shapefile")
   # print(sf)
   # print(anonymizer)
   # print(decimals)
    out = shapefile.Writer()
    for shape in sf.shapes():
        for i in range(len(shape.points)):
            shape.points[i] = anonymizer(shape.points[i][0], shape.points[i][1], decimals)
        out._shapes.append(shape)
    print(len(out._shapes))
    return out

def write(writer: shapefile.Writer, output):
    writer.saveShp(output)
