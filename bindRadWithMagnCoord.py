#Связывает данные дозы с координатами из магнитки.
import transformCoord
import radTimeTransform
import coordFunction
from tkinter import filedialog
import datetime

tableLonLatAlt = transformCoord.openMagnFiles()
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
radData = radTimeTransform.getRadData_unixtimeDoseOnly()
radData = radTimeTransform.fillDataHoles(radData)


fileRes = filedialog.asksaveasfile('w',)
fileRes.write('doseRate, uSv/h' + '\t' + 'TIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\n')
for point in radData:
    LatLonAlt = LatLonAltInterpolFunc.getLatLonAlt(point[0])
    resPoint = point + LatLonAlt
    fileRes.write(str(resPoint[1]) + '\t' + str(datetime.datetime.fromtimestamp(resPoint[0]).strftime('%d-%m-%YT%H:%M:%S,%f'))
                  + '\t' + str(resPoint[2]) + '\t' + str(resPoint[3]) + '\t' + str(resPoint[4]) + '\n')
fileRes.close()