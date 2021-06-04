#getRadData_unixtimeOnly Привязывает данные радометрии ATOM к координатам GPX. Дает выбрать CSV Файлы радиометра и возвращает упорядоченный список кортежей (Время, доза)
from datetime import *
from tkinter import *
from tkinter import filedialog


def getRadData():

    filesRad = filedialog.askopenfilenames(title = ("Choose radiation files"), filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
    val_points = []
    for file in filesRad:
        fileRad = open(file, 'r')
        lines = fileRad.readlines()
        for line in lines:
            value = line.replace('\n', '').split('\t')
            val_points.append(((datetime.strptime(value[1], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)).timestamp(), value[0]))
        fileRad.close()
    val_points = dict((x,y) for x, y in val_points)
    vals = []
    for key in val_points.keys():
        vals.append((key, val_points[key]))
    def getKey(item):
        return item[0]
    val_points = sorted(vals, key=getKey)
    return val_points

def getRadData_unixtimeDoseOnly():
    filesRad = filedialog.askopenfilenames(title=("Choose radiation files"),
                                           filetypes=(("Template files", "*.csv"), ("All files", "*.*")))
    val_points = []
    for file in filesRad:
        fileRad = open(file, 'r')
        lines = fileRad.readlines()
        for line in lines:
            value = line.replace('\n', '').split(';')
            try:
                val_points.append((int(value[0])-32, float(value[1])))
            except ValueError:
                continue
        fileRad.close()
    def getKey(item):
        return item[0]
    val_points = sorted(val_points, key=getKey)
    return val_points

#заполняет Пустыми значениями
def fillDataHoles(val_points):
    filledPoints = []
    prevTime = 0
    for point in val_points:
        if prevTime == 0:
            prevTime = point[0]
            filledPoints.append(point)
            continue
        timedelta = point[0] - prevTime
        if (timedelta > 2) and (timedelta <= 900):
            for i in range(1,timedelta//2):
                filledPoints.append(((prevTime + i*2), 0.0))
        filledPoints.append(point)
        prevTime = point[0]
    return filledPoints