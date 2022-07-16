# Связывает файлы магнитометра с данными координат из GPX
# Сдвиг времени (часовой пояс) задается в файле transformCoord.openGpxFiles

from GetSpatialData import openGpxFiles
import coordFunction
from getMagnData import getMagnData
import datetime
from tkinter import filedialog

filesCoord = filedialog.askopenfilenames(title = ("Choose gpx coord files"), filetypes = (("Template files", "*.gpx"),("All files", "*.*")))
tableLonLatAlt = openGpxFiles.openGpxFiles(filesCoord)
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
filesMagn = filedialog.askopenfilenames(title = ("Choose Magnetic files"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
magnDataPoints = getMagnData(filesMagn)
magnDataResult = []
fileRes = filedialog.asksaveasfile('w')
fileRes.write('FIELD' + '\t' + 'qmc'  + '\t' + 'st' + '\t' + 'TIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\n')
for point in magnDataPoints:
    LatLonAlt = LatLonAltInterpolFunc.getLonLatAlt(point[0])
    resPoint = point + LatLonAlt
    fileRes.write(str(int(resPoint[1])/1000) + '\t' + str(resPoint[2])  + '\t' + str(resPoint[3])  + '\t'
                  + str(datetime.datetime.fromtimestamp(resPoint[0]).strftime('%d-%m-%YT%H:%M:%S,%f')) + '\t'
                  + str(resPoint[4]) + '\t' + str(resPoint[5]) + '\t' + str(resPoint[6]) + '\n')
fileRes.close()