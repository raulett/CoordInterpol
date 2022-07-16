from GetSpatialData import openGpxFiles
import coordFunction

from datetime import *
from tkinter import filedialog

filesRad = filedialog.askopenfilenames(title="Choose MKSP spectrum files")
tableLonLatAlt = openGpxFiles.openGpxFiles()

# Функционал для привязки координат к измерениям спектрометра МКСП от РАДЭК

# tableLonLatAlt = transformCoord.openGpxFiles()

LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)

val_points = []
print("val_points init")
for file in filesRad:
    print("file: {} init")
    fileRad = open(file, 'r')
    lines = fileRad.readlines()
    title = lines[0]
    lines_count = len(lines)
    lines_counter = 1
    for line in lines:
        print("Handling {} line of {}. There is {} value points now".format(lines_counter, lines_count, len(val_points)))
        lines_counter += 1
        value = line.replace('\n', '').split('\t')
        if (len(value)) != 17:
            continue

        try:
            # dateTime = datetime.strptime(value[3], "%Y-%m-%dT%H:%M:%S").timestamp()
            dateTime = datetime.strptime(value[0], '%d.%m.%YT%H:%M:%S').timestamp()
        except ValueError:
            print("Value error. Datetime parsing. value = {}".format(value[0]))
            dateTime = 0
            continue

        val_points.append((dateTime, line))
    fileRad.close()

val_points = dict((x,y) for x, y in val_points)

vals = []
for key in val_points.keys():
    vals.append((key, val_points[key]))
def getKey(item):
    return item[0]
val_points = sorted(vals, key=getKey)

fileRes = filedialog.asksaveasfile('w')
fileRes.write('LON\tLAT\tALT\t' + title)
val_points_counts = len(val_points)
points_counter = 1
for point in val_points:
    print("Handle point №{} of {}. ".format(points_counter, val_points_counts))
    points_counter += 1
    LonLatAlt = LatLonAltInterpolFunc.getLonLatAlt(point[0])
    resPoint = point + LonLatAlt
    # fileRes.write('0' + '\t' + str(datetime.fromtimestamp(resPoint[0]).strftime('%y.%m.%dT%H:%M:%S')) + '\t'
    #               + str(resPoint[1]) + '\t'
    #               + str(datetime.fromtimestamp(resPoint[0]).strftime('%y.%m.%dT%H:%M:%S')) + '\t'
    #               + str(resPoint[3]) + '\t' + str(resPoint[2])  + '\t' + str(resPoint[4]) + '\t'
    #               + '0' + '\t' '0' + '\n')
    fileRes.write(str(LonLatAlt[0]) + '\t' + str(LonLatAlt[1]) + '\t' + str(LonLatAlt[2])
                  + '\t' + str(point[1]))
fileRes.close()