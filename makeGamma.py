import transformCoord
import coordFunction
import datetime
from tkinter import filedialog

tableLonLatAlt = transformCoord.openGpxFiles()
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
filesRad = filedialog.askopenfilenames(title = ("Choose Magnetic files"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
val_points = []
for file in filesRad:
    fileRad = open(file, 'r')
    lines = fileRad.readlines()
    for line in lines:
        value = line.replace('\n', '').split('\t')
        kDOSE = value[4]
        uDOSE = value[5]
        integralCH = value[6]
        dateTime = datetime.datetime.strptime(value[0], "%d.%m.%YT%H:%M:%S").timestamp()
        val_points.append((dateTime, (kDOSE, uDOSE, integralCH)))
    fileRad.close()
    val_points = dict((x,y) for x, y in val_points)
    vals = []
    for key in val_points.keys():
        vals.append((key, val_points[key][0], val_points[key][1], val_points[key][2]))
    def getKey(item):
        return item[0]
    val_points = sorted(vals, key=getKey)
gammaDataResult = []
fileRes = filedialog.asksaveasfile('w')
fileRes.write('DATETIME\tLAT\tLON\tALT\tkDOSE\tuDOSE\tintegralCH\n')
for point in val_points:
    LatLonAlt = LatLonAltInterpolFunc.getLatLonAlt(point[0])
    resPoint = point + LatLonAlt
    fileRes.write(str(datetime.datetime.fromtimestamp(resPoint[0]).strftime('%d-%m-%YT%H:%M:%S,%f')) + '\t' + str(resPoint[5])  + '\t' + str(resPoint[4])  + '\t'
                  + str(resPoint[6]) + '\t' + str(resPoint[1]) + '\t' + str(resPoint[2]) + '\t' + str(resPoint[3]) + '\n')
fileRes.close()