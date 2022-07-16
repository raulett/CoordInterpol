# Модуль  перепривязывает координаты к данным радиометрии полученные с радиометра ATOM, Также позволяет учесть часовой
# пояс GPS и телефона. А также позволяет получить несколько файлов с несколькими временными сдвигами
from GetSpatialData import openGpxFiles
import coordFunction
import datetime
from tkinter import filedialog
from GetSpatialData.getSpatialCSV import getSpatialCSV

# Указать таймзону телефона (считаем, что GPS -UTC)
timezone = (8)

# Указать диапазон сдвигов данных Будет сформировано количество файлов с разными сдвигами
# в количестве dataTimeShift[1] - dataTimeShift[0]
dataTimeShift = (0, 1)
timedelta = 0

filesCSV = filedialog.askopenfilenames(title="Choose CSV coord files", filetypes=(("Template files", "*.txt"),
                                                                                  ("All files", "*.*")))
tableLonLatAlt = getSpatialCSV(filesCSV, ';')
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
filesRad = filedialog.askopenfilenames(title = ("Choose rad file"))
fileResName = filedialog.asksaveasfilename()

for delta in range(dataTimeShift[0], dataTimeShift[1]):
    localFileResName = fileResName
    localFileResName = localFileResName.split('.')[0] + '_shifted(%d).txt'%delta
    val_points = []
    for file in filesRad:
        fileRad = open(file, 'r')
        lines = fileRad.readlines()
        for line in lines:
            value = line.replace('\n', '').split(';')
            try:
                time = int(value[0]) - (timezone*3600)+ timedelta

                dose = float(value[1].replace(',', '.'))
            except ValueError as ex:
                print("radiometry file datetime parce error: {0}".format(ex))
                continue
            val_points.append((time, dose))
        fileRad.close()
    def getKey(item):
        return item[0]
    val_points = sorted(val_points, key=getKey)

    localFileRes = open(localFileResName, 'w')
    localFileRes.write('doseRate, uSv/h' + '\t' + 'TIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\n')
    for point in val_points:
        LatLonAlt = LatLonAltInterpolFunc.getLonLatAlt(point[0])
        resPoint = point + LatLonAlt
        localFileRes.write(str(resPoint[1]) + '\t' + str(datetime.datetime.fromtimestamp(resPoint[0]).strftime('%d-%m-%YT%H:%M:%S,%f'))
                      + '\t' + str(resPoint[2]) + '\t' + str(resPoint[3]) + '\t' + str(resPoint[4]) + '\n')
    localFileRes.close()