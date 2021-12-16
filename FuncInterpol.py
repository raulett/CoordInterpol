from tkinter import filedialog

from GetSpatialData import openGpxFiles
import radTimeTransform
import datetime

# <<<<<<< HEAD
tableLonLatAlt = openGpxFiles.openGpxFiles()
# # =======
# # table lon lat alt. tuple((point.longitude, point.latitude, point.elevation, (point.time + timedelta(hours=0, seconds=0)).timestamp())))
# tableLonLatAlt = transformCoord.openGpxFiles()
# >>>>>>> develop

# prevLat = 0
# prevLon = 0
# prevAlt = 0


LonInterpolFunc = []
LatInterpolFunc = []
AltInterpolFunc = []
# print(tableLonLatAlt)

for i in range(len(tableLonLatAlt)):
    # print(i)
    if i == 0:
        continue
    else:
        LonK = (tableLonLatAlt[i - 1][0] - tableLonLatAlt[i][0]) / (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])
        LonB = tableLonLatAlt[i - 1][0] - ((tableLonLatAlt[i - 1][0] - tableLonLatAlt[i][0]) / (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])) * tableLonLatAlt[i - 1][3]
        LonInterpolFunc.append((LonK, LonB))
        LatK = (tableLonLatAlt[i - 1][1] - tableLonLatAlt[i][1]) / (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])
        LatB = tableLonLatAlt[i - 1][1] - \
               ((tableLonLatAlt[i - 1][1] - tableLonLatAlt[i][1]) / (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])) * tableLonLatAlt[i - 1][3]
        LatInterpolFunc.append((LatK, LatB))
        AltK = (tableLonLatAlt[i - 1][2] - tableLonLatAlt[i][2]) / (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])
        AltB = tableLonLatAlt[i - 1][2] - ((tableLonLatAlt[i - 1][2] - tableLonLatAlt[i][2]) / (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])) * tableLonLatAlt[i - 1][3]
        AltInterpolFunc.append((AltK, AltB))


# print(tableLonLatAlt)
# print(LonInterpolFunc)
# print(LatInterpolFunc)
# print(AltInterpolFunc)

times = radTimeTransform.getRadData_unixtimeDoseOnly()

i = 0
resultLon = []
resultLat = []
resultAlt = []
result = []
counter = 0
fileRes = filedialog.asksaveasfile('w')
fileRes.write('VAL' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\t' + 'TIME' + '\n')
while counter < len(times):
    if times[counter][0] <= tableLonLatAlt[i+1][3]:
        resLon = LonInterpolFunc[i][0] * float(times[counter][0]) + LonInterpolFunc[i][1]
        resLat = LatInterpolFunc[i][0] * float(times[counter][0]) + LatInterpolFunc[i][1]
        resAlt = AltInterpolFunc[i][0] * float(times[counter][0]) + AltInterpolFunc[i][1]
        result = (str(times[counter][1]) + '\t' + str(resLon) + '\t' + str(resLat) + '\t' + str(resAlt) + '\t' +
                  datetime.datetime.fromtimestamp(int(times[counter][0])).strftime('%Y-%m-%dT%H:%M:%S') + '\n')
        fileRes.write(result)
        counter += 1
    else:
        i += 1
        continue




fileRes.close()
