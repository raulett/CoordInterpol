

fileCoord = open('coord.txt')
lines = fileCoord.readlines()
tableLonLat = []
print(lines)

inf = {}

prevLat = 0
prevLon = 0
for line in lines:
    l = line.split('\t')
    tableLonLat.append((float(l[0]), float(l[1]), float(l[2])))


LonInterpolFunc = []
LatInterpolFunc = []
print(tableLonLat)

for i in range(len(tableLonLat)):
    print(i)
    if i == 0:
        continue
    else:
        LonK = (tableLonLat[i-1][0] - tableLonLat[i][0])/(tableLonLat[i-1][2] - tableLonLat[i][2])
        LonB = tableLonLat[i-1][0] - ((tableLonLat[i-1][0] - tableLonLat[i][0])/(tableLonLat[i-1][2] - tableLonLat[i][2])) * tableLonLat[i-1][2]
        LonInterpolFunc.append((LonK, LonB))
        LatK = (tableLonLat[i-1][1] - tableLonLat[i][1])/(tableLonLat[i-1][2] - tableLonLat[i][2])
        LatB = tableLonLat[i-1][1] - \
               ((tableLonLat[i-1][1] - tableLonLat[i][1])/(tableLonLat[i-1][2] - tableLonLat[i][2])) * tableLonLat[i-1][2]
        LatInterpolFunc.append((LatK, LatB))

print(tableLonLat)
print(LonInterpolFunc)
print(LatInterpolFunc)

file2 = open('result_m.txt')
times = file2.readlines()
t = []
for time in times:
    t.append(float(time))

print(t)

i = 0
resultLon = []
resultLat = []
result = []
counter = 0
fileRes = open('10092017_interpolated_result.txt', 'w')
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
