

fileCoord = open('book.txt')
lines = fileCoord.readlines()
tableLonLat = []
print(lines)

inf = {}
for line in lines:
    l = line.split('\t')
    if line.find('lat') != (-1):

        for el in range(len(l)):
            if l[el].find('lat') != (-1):
                inf['lat'] = el
            if l[el].find('lon') != (-1):
                inf['lon'] = el
            if l[el].find('ns1:ele') != (-1):
                inf['ns1:ele'] = el
            if l[el].find('ns1:time2') != (-1):
                inf['ns1:time2'] = el
    else:

        tableLonLat.append((float(l[inf.get('lat')]), float(l[inf.get('lon')]),
                            float(l[inf.get('ns1:ele')]), l[inf.get('ns1:time2')]))

LonInterpolFunc = []
LatInterpolFunc = []

for i in range(len(tableLonLat)):
    if i == 0:
        continue
    else:
        LonK = (tableLonLat[i-1][0] - tableLonLat[i][0])/(tableLonLat[i-1][2] - tableLonLat[i][2])
        LonB = tableLonLat[i-1][0] - \
               ((tableLonLat[i-1][0] - tableLonLat[i][0])/(tableLonLat[i-1][2] - tableLonLat[i][2])) * tableLonLat[i-1][2]
        LonInterpolFunc.append((LonK, LonB))
        LatK = (tableLonLat[i-1][1] - tableLonLat[i][1])/(tableLonLat[i-1][2] - tableLonLat[i][2])
        LatB = tableLonLat[i-1][1] - \
               ((tableLonLat[i-1][1] - tableLonLat[i][1])/(tableLonLat[i-1][2] - tableLonLat[i][2])) * tableLonLat[i-1][2]
        LatInterpolFunc.append((LatK, LatB))

print(tableLonLat)
print(LonInterpolFunc)
print(LatInterpolFunc)

file2 = open('09161516.txt')
times = file2.readlines()
t = []
for time in times:
    t.append(int(time))

print(t)

i = 0
resultLon = []
resultLat = []
result = []
counter = 0
fileRes = open('09021820a_coord_interpolated.txt', 'w')
while counter < len(t):
    if t[counter] <= tableLonLat[i+1][2]:
        resLon = LonInterpolFunc[i][0]*t[counter]+LonInterpolFunc[i][1]
        resLat = LatInterpolFunc[i][0]*t[counter] + LatInterpolFunc[i][1]
        resultLon.append(resLon)
        resultLat.append(resLat)
        result = (str(resLon) + '\t' + str(resLat) + '\t' + str(t[counter]) + '\n')
        fileRes.write(result)
        counter += 1
    else:
        i += 1
        continue




fileRes.close()
