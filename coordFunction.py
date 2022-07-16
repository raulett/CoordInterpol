# Получает на вход массив кортежей вида (lon, lat, alt, nixTimstamp), отсортированный по времени. Возвращает объект.
# Объект предоставляет функцию положения от времени.

class CoordFunction:
    LonInterpolFunc = []
    LatInterpolFunc = []
    AltInterpolFunc = []
    timeSt = []

    firstRecord = 999999999999999
    lastRecord = -999999999999999

    #Функция создает объект CoordFunction, Получает на вход массив кортежей вида (lon, lat, alt, nixTimstamp),
    # отсортированный по времени.
    def __init__(self, tableLonLatAlt):
        print("coordinate interpolation started")
        for i in range(len(tableLonLatAlt)):
            print("Record {} from {} interpolated. ".format(i, len(tableLonLatAlt)))
            if tableLonLatAlt[i][3] < self.firstRecord: self.firstRecord = tableLonLatAlt[i][3]
            if tableLonLatAlt[i][3] > self.lastRecord: self.lastRecord = tableLonLatAlt[i][3]
            if i == 0:
                continue
            else:
                if (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] == 0):
                    LonK = (tableLonLatAlt[i - 1][0] - tableLonLatAlt[i][0]) / (
                    tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] + 0.0000000001)
                else:
                    LonK = (tableLonLatAlt[i - 1][0] - tableLonLatAlt[i][0]) / (
                            tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])
                if (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] == 0):
                    LonB = tableLonLatAlt[i - 1][0] - ((tableLonLatAlt[i - 1][0] - tableLonLatAlt[i][0]) / (
                    tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] + 0.0000000001)) * tableLonLatAlt[i - 1][3]
                else:
                    LonB = tableLonLatAlt[i - 1][0] - ((tableLonLatAlt[i - 1][0] - tableLonLatAlt[i][0]) / (
                    tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])) * tableLonLatAlt[i - 1][3]
                self.LonInterpolFunc.append((LonK, LonB))
                if (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] == 0):
                    LatK = (tableLonLatAlt[i - 1][1] - tableLonLatAlt[i][1]) / (
                    tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] + 0.0000000001)
                else:
                    LatK = (tableLonLatAlt[i - 1][1] - tableLonLatAlt[i][1]) / (
                    tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])
                if (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] == 0):
                    LatB = tableLonLatAlt[i - 1][1] - \
                       ((tableLonLatAlt[i - 1][1] - tableLonLatAlt[i][1]) / (
                       tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] + 0.0000000001 )) * tableLonLatAlt[i - 1][3]
                else:
                    LatB = tableLonLatAlt[i - 1][1] - \
                       ((tableLonLatAlt[i - 1][1] - tableLonLatAlt[i][1]) / (
                       tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])) * tableLonLatAlt[i - 1][3]


                self.LatInterpolFunc.append((LatK, LatB))
                if (tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] == 0):
                    AltK = (tableLonLatAlt[i - 1][2] - tableLonLatAlt[i][2]) / (
                    tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] + 0.0000000001)
                    AltB = tableLonLatAlt[i - 1][2] - ((tableLonLatAlt[i - 1][2] - tableLonLatAlt[i][2]) / (
                    tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3] + 0.0000000001)) * tableLonLatAlt[i - 1][3]
                else:
                    AltK = (tableLonLatAlt[i - 1][2] - tableLonLatAlt[i][2]) / (
                            tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])
                    AltB = tableLonLatAlt[i - 1][2] - ((tableLonLatAlt[i - 1][2] - tableLonLatAlt[i][2]) / (
                            tableLonLatAlt[i - 1][3] - tableLonLatAlt[i][3])) * tableLonLatAlt[i - 1][3]
                self.AltInterpolFunc.append((AltK, AltB))
                self.timeSt.append(tableLonLatAlt[i][3])
        print("first rec: " + str(self.firstRecord) + ", last rec: " + str(self.lastRecord))
    # Функция получает время и возвращает положение LAT, LON, ALT. Пока реализовано перебором, надо будет переписать
    # половинным делением.
    def getLonLatAlt(self, timestamp):
        if timestamp < self.firstRecord or timestamp > self.lastRecord:
            print("data`s time record {0} is out of coordinate range.".format(timestamp))
            return (0, 0, 0)
        else:
            i = 0
            while timestamp >= self.firstRecord or timestamp <= self.lastRecord:
                if timestamp <= self.timeSt[i]:
                    resLon = self.LonInterpolFunc[i][0] * float(timestamp) + self.LonInterpolFunc[i][1]
                    resLat = self.LatInterpolFunc[i][0] * float(timestamp) + self.LatInterpolFunc[i][1]
                    resAlt = self.AltInterpolFunc[i][0] * float(timestamp) + self.AltInterpolFunc[i][1]
                    return (resLon, resLat, resAlt)
                else:
                    i += 1
                    continue
            return (0, 0, 0)

