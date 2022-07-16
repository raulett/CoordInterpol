import datetime
import sys

from UI.bindMagnFiles_ui import Ui_BindMagnFiles
from PyQt5 import QtWidgets
import os, string
from GetSpatialData import openGpxFiles
from getMagnDataV2 import getMagnData
from common.SplinesArray import ValueNotFoundException
from common.LinearSpline import ImpossibleException
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


class BindMagnFile_handle(Ui_BindMagnFiles, QtWidgets.QMainWindow):
    debug = 0
    def __init__(self):
        super(BindMagnFile_handle, self).__init__()
        self.setupUi(self)
        self.initGui()

    def initGui(self):
        self.gpx_filenames = []
        self.input_magn_filenames = []
        self.save_filename = ''
        self.work_dir = os.path.dirname(os.path.abspath(__file__))


        self.toolButton.clicked.connect(self.set_GPX_filenames)
        self.toolButton_2.clicked.connect(self.set_input_magn_filenames)
        self.toolButton_3.clicked.connect(self.set_result_file)
        self.pushButton_make.clicked.connect(self.genarate_magn_coord_file)
        self.pushButton_exit.clicked.connect(sys.exit)
        self.pushButton_draw.clicked.connect(self.show_graph)

    def set_GPX_filenames(self):
        self.gpx_filenames = QtWidgets.QFileDialog.getOpenFileNames(self, "Open GPX files", "","GPX files (*.gpx)")[0]
        if self.debug:
            print(self.gpx_filenames)
        # print(base_filenames)
        if len(self.gpx_filenames)>0:
            self.gpxlineEdit.setText('; '.join(map(lambda fn: os.path.basename(fn),self.gpx_filenames)))
            self.gpxlineEdit.setToolTip('; '.join(self.gpx_filenames))
            self.gpx_functions = openGpxFiles.openGpxFiles(self.gpx_filenames)
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("No gpx files was chosen")
            msgBox.exec()

    def set_input_magn_filenames(self):
        self.input_magn_filenames = QtWidgets.QFileDialog.getOpenFileNames(self, "Open POS magn files", "","TXT files (*.txt)")[0]
        if self.debug:
            print(self.input_magn_filenames)
        if len(self.input_magn_filenames)>0:
            self.magn_lineEdit.setText('; '.join(map(lambda fn: os.path.basename(fn),self.input_magn_filenames)))
            self.magn_lineEdit.setToolTip('; '.join(self.input_magn_filenames))
            if self.debug:
                print(type(self.comboBox.currentText()))
            try:
                self.magn_points = getMagnData(self.input_magn_filenames, str(self.comboBox.currentText()))
            except Exception as e:
                print(e)

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("No input magn files was chosen")
            msgBox.exec()

    def set_result_file(self):
        self.result_filename = QtWidgets.QFileDialog.getSaveFileName(self, "result magn file", "", "TXT tab separated files (*.txt)")[0]
        self.result_lineEdit.setText(os.path.basename(self.result_filename))
        self.result_lineEdit.setToolTip(self.result_filename)

    def show_graph(self):
        if len(self.magn_points)==0 or len(self.gpx_functions)==0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("No magn or gpx files chosen")
            return

        try:
            timelag = self.doubleSpinBox.value()
        except Exception as e:
            timelag = 0.0
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Errer getting timelag: {}".format(e))
            msgBox.exec()

        fig, ax = plt.subplots()
        fig.set_size_inches(14, 8)
        ax.xaxis.axis_date()
        x = [datetime.datetime.fromtimestamp(point[0] + timelag) for point in self.magn_points]
        dates = matplotlib.dates.date2num(x)
        y = np.array([int(point[1]) / 1000 for point in self.magn_points])
        # подбор масштаба осей
        hist_classes = self.spinBox.value()
        hist, bin_edges = np.histogram(y, bins=hist_classes)
        max_el_index = hist.argmax(axis=0)
        class_delta = bin_edges[max_el_index + 1] - bin_edges[max_el_index]
        low_lim = bin_edges[max_el_index] - class_delta / 10
        high_lim = bin_edges[max_el_index] + class_delta
        plt.ylim(low_lim, high_lim)

        colors = []
        for point in self.magn_points:
            try:
                lon = self.gpx_functions[0].get_value(point[0] + timelag)
                colors.append('r')
            except Exception as e:
                colors.append('b')
        colors = np.array(colors)
        ax.set_xlabel('datetime')
        ax.set_ylabel('Magnetic Field')
        plt.scatter(dates, y, color=colors, s=0.5)
        plt.show()


    def genarate_magn_coord_file(self):
        count = 0
        try:
            timelag = self.doubleSpinBox.value()
        except Exception as e:
            timelag = 0.0
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Errer getting timelag: {}".format(e))
            msgBox.exec()
        try:
            result_file = open(self.result_filename, 'w')
            result_file.write('FIELD' + '\t' + 'qmc'  + '\t' + 'st' + '\t' + 'TIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\n')
            for point in self.magn_points:
                try:
                    lon = self.gpx_functions[0].get_value(point[0]+timelag)
                    lat = self.gpx_functions[1].get_value(point[0]+timelag)
                    alt = self.gpx_functions[2].get_value(point[0]+timelag)
                    count += 1
                except ValueNotFoundException as e:
                    lon = 0
                    lat = 0
                    alt = 0
                except ImpossibleException as e:
                    lon = 0
                    lat = 0
                    alt = 0

                result_file.write(str(int(point[1])/1000) + '\t' +
                                  str(point[2]) + '\t' +
                                  str(point[3]) + '\t' +
                                  str(datetime.datetime.fromtimestamp(point[0]).strftime('%d-%m-%YT%H:%M:%S,%f')) + '\t' +
                                  str(lon) + '\t' + str(lat) + '\t' + str(alt) + '\n')
            result_file.close()

        except Exception as e:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("General exception")
            msgBox.setText("Error writing result file: {}".format(e))
            msgBox.exec()
            return

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("file generated, {} records with coord".format(count))
        msgBox.setWindowTitle("Generation successful")
        msgBox.exec()



