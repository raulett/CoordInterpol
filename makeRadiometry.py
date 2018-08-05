import transformCoord
import coordFunction
import MagnTimeTransfirm
import datetime
from tkinter import filedialog

tableLonLatAlt = transformCoord.openGpxFiles()
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
filesRad = filedialog.askopenfilenames(title = ("Choose rad file"))
val_points = []
for file in filesRad:
    fileRad = open(file, 'r')
    lines = fileRad.readlines()
    for line in lines:
        value = line.replace('\n', '').split(';')
        time = int(value[0])/1000-(3600*8)
        dose = float(value[1].replace(',', '.'))
        val_points.append((time, dose))
    fileRad.close()
def getKey(item):
    return item[0]
val_points = sorted(val_points, key=getKey)

fileRes = filedialog.asksaveasfile('w')
fileRes.write('doseRate, uSv/h' + '\t' + 'TIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\n')
for point in val_points:
    LatLonAlt = LatLonAltInterpolFunc.getLatLonAlt(point[0])
    resPoint = point + LatLonAlt
    fileRes.write(str(resPoint[1]) + '\t' + str(datetime.datetime.fromtimestamp(resPoint[0]).strftime('%d-%m-%YT%H:%M:%S,%f'))
                  + '\t' + str(resPoint[2]) + '\t' + str(resPoint[3]) + '\t' + str(resPoint[4]) + '\n')
fileRes.close()