# Связывает файлы магнитометра с данными координат из GPX
# Сдвиг времени (часовой пояс) задается в файле transformCoord.openGpxFiles

from GetSpatialData import openGpxFiles
import coordFunction
from getMagnData import getMagnData
import datetime
from tkinter import filedialog

tableLonLatAlt = openGpxFiles.openGpxFiles()
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
magnDataPoints = getMagnData()
magnDataResult = []
fileRes = filedialog.asksaveasfile('w')
fileRes.write('FIELD' + '\t' + 'qmc'  + '\t' + 'st' + '\t' + 'TIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\n')
for point in magnDataPoints:
    LatLonAlt = LatLonAltInterpolFunc.getLatLonAlt(point[0])
    resPoint = point + LatLonAlt
    fileRes.write(str(int(resPoint[1])/1000) + '\t' + str(resPoint[2])  + '\t' + str(resPoint[3])  + '\t'
                  + str(datetime.datetime.fromtimestamp(resPoint[0]).strftime('%d-%m-%YT%H:%M:%S,%f')) + '\t'
                  + str(resPoint[4]) + '\t' + str(resPoint[5]) + '\t' + str(resPoint[6]) + '\n')
fileRes.close()