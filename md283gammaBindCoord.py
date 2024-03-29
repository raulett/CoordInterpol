# Модуль привязывает данные спектрометрии к координатам GPX, полученным из программы ASW от Радэка.

from GetSpatialData import openGpxFiles
import coordFunction

from datetime import *
from tkinter import filedialog

# radioCalculateBeginNum = 145
# radioCalculateEndNum = 937
# Номера каналов спектра, с какого по какой считать радиометрию
radioCalculateBeginNum = 54
radioCalculateEndNum = 368
timeshift = -1.5

tableLonLatAlt = openGpxFiles.openGpxFiles()
LatLonAltInterpolFunc = coordFunction.CoordFunction(tableLonLatAlt)
filesRad = filedialog.askopenfilenames(title=("Choose gamma files"),
                                       filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
val_points = []
for file in filesRad:
	fileRad = open(file, 'r')
	lines = fileRad.readlines()
	for line in lines:
		value = line.replace('\n', '').split('\t')
		if ((len(value)) != 13):
			continue

		Time = value[0]
		ch1Num = value[4]
		ch2Num = value[5]
		ch1En = value[6]
		ch2En = value[7]
		expoTime = value[8]
		U = value[9]
		Th = value[10]
		K = value[11]
		spectre = value[12]
		count = 0
		try:
			dateTime = datetime.strptime(Time, "%d.%m.%YT%H:%M:%S").timestamp()+timeshift
		except ValueError:
			dateTime = 0
			print("Error parsing datetime")
			continue

		# Посчитаем радиометрию с канала 400 кЭв по 2.8мЭв

		spectreList = spectre.split(';')
		if len(spectreList) > radioCalculateEndNum:
			for c in spectreList[radioCalculateBeginNum:radioCalculateEndNum]:
				try:
					count += int(c)
				except ValueError:
					print("Error spectre count to integer")
					continue

		val_points.append((dateTime, (count, ch1Num, ch2Num, ch1En, ch2En, expoTime, U, Th, K, spectre)))
	fileRad.close()

val_points = dict((x, y) for x, y in val_points)

vals = []
for key in val_points.keys():
	vals.append((key, val_points[key]))


def getKey(item):
	return item[0]


val_points = sorted(vals, key=getKey)

fileRes = filedialog.asksaveasfile('w')
fileRes.write('DATETIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\t' + 'Counts' + '\t' +
              'ch1Num' + '\t' + 'ch2Num' + '\t' + 'ch1En' + '\t' + 'ch2En' + '\t' +
              'expoTime' + '\t' + 'U' + '\t' + 'Th' + '\t' + 'K' + '\t' + 'spectre' + '\n')
for point in val_points:
	LatLonAlt = LatLonAltInterpolFunc.getLatLonAlt(point[0])
	resPoint = point + LatLonAlt
	fileRes.write(str(datetime.fromtimestamp(resPoint[0]).strftime('%d-%m-%YT%H:%M:%S')) + '\t'
	              + str(resPoint[2]) + '\t' + str(resPoint[3]) + '\t' + str(resPoint[4]) + '\t'
	              + str(resPoint[1][0]) + '\t' + str(resPoint[1][1]) + '\t' + str(resPoint[1][2]) + '\t'
	              + str(resPoint[1][3]) + '\t' + str(resPoint[1][4]) + '\t' + str(resPoint[1][5]) + '\t'
	              + str(resPoint[1][6]) + '\t' + str(resPoint[1][7]) + '\t' + str(resPoint[1][8]) + '\t'
				  + str(resPoint[1][9]) + '\n')
fileRes.close()
