from GetSpatialData import openGpxFiles
import coordFunction

from datetime import *
from tkinter import filedialog

<<<<<<< HEAD
tableLonLatAlt = openGpxFiles.openGpxFiles()
=======
# Функционал для привязки координат к измерениям спектрометра МКСП от РАДЭК

tableLonLatAlt = transformCoord.openGpxFiles()
>>>>>>> develop
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
filesRad = filedialog.askopenfilenames(title = ("Choose Magnetic files"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
val_points = []
for file in filesRad:
    fileRad = open(file, 'r')
    lines = fileRad.readlines()
    for line in lines:
        value = line.replace('\n', '').split('\t')
        if ((len(value))!=10):
            continue

        gpsTime = value[1]
        T = value[9]

        try:
            k = int(value[2])
        except ValueError:
            continue

        try:
            dateTime = datetime.strptime(value[3], "%Y-%m-%dT%H:%M:%S").timestamp()
        except ValueError:
	        dateTime = 0

        val_points.append((dateTime, T))
    fileRad.close()

val_points = dict((x,y) for x, y in val_points)

vals = []
for key in val_points.keys():
    vals.append((key, val_points[key]))
def getKey(item):
    return item[0]
val_points = sorted(vals, key=getKey)

fileRes = filedialog.asksaveasfile('w')
fileRes.write('PAGE	PAGESTARTDATETIME	VALUE	GPSTIME	LAT	LON	ALT	SAT	PAGEENDDATETIME' + '\n')
for point in val_points:
	LatLonAlt = LatLonAltInterpolFunc.getLatLonAlt(point[0])
	resPoint = point + LatLonAlt
	fileRes.write('0' + '\t' + str(datetime.fromtimestamp(resPoint[0]).strftime('%y.%m.%dT%H:%M:%S')) + '\t'
	              + str(resPoint[1]) + '\t'
	              + str(datetime.fromtimestamp(resPoint[0]).strftime('%y.%m.%dT%H:%M:%S')) + '\t'
	              + str(resPoint[3]) + '\t' + str(resPoint[2])  + '\t' + str(resPoint[4]) + '\t'
	              + '0' + '\t' '0' + '\n')
fileRes.close()