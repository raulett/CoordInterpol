from tkinter import filedialog
from datetime import *
from common.SplinesArray import *
import sys

try:
    general_magnetic_field = int(sys.argv[1])
except IndexError:
    print('General field value argument not fount. Pass general field as first argument. for example: '
          'variations_calculate.py 60693')
    exit(1)
except ValueError:
    print('Can`t read general field value. Input an integer value. You input: {0}'.format(sys.argv[1]))


def variations_calculate():
    variation_files = filedialog.askopenfilenames(title="Choose variation files",
                                                  filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
    value_points = []
    variations_function = SplinesArray()

    for filename in variation_files:
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            value = line.replace('\n', '').split(' ')
            if (len(value)) != 5:
                continue
            try:
                date_time = datetime.strptime(value[3] + 'T' + value[4], "%m-%d-%yT%H:%M:%S,%f").timestamp()
            except ValueError:
                print('Variations datetime parse error')
                continue
            try:
                variation_t = int(value[0]) / 1000
            except ValueError:
                print('Error parce integer digit: {}'.format(value[0]))
                continue
            value_points.append((date_time, variation_t))
        file.close()
        variations_function.add_spline(value_points)
        value_points = []

    magnetic_files = filedialog.askopenfilenames(title="Choose magnetic files",
                                                  filetypes=(("Template files", "*.txt"), ("All files", "*.*")))
    variated_magnetic_points = []
    for magnetic_file_name in magnetic_files:
        magnetic_file = open(magnetic_file_name, 'r')
        lines = magnetic_file.readlines()
        for line in lines:
            value = line.replace('\n', '').split('\t')
            try:
                t = float(value[0])
            except ValueError:
                print('Error parsing magnetic field value: {}'.format(value[0]))
                continue
            qmc = value[1]
            st = value[2]
            date_time = value[3]
            lon = value[4]
            lat = value[5]
            alt = value[6]
            unix_date_time = datetime.strptime(date_time, "%d-%m-%YT%H:%M:%S,%f").timestamp()
            try:
                variated_value = t + (general_magnetic_field - variations_function.get_value(unix_date_time))
            except ValueNotFoundException:
                print("Variations not found for magnetic record: {}".format(date_time))
                variated_value = 0
            variated_magnetic_points.append((variated_value, qmc, st, date_time, lon, lat, alt))
        magnetic_file.close()

    variated_file = filedialog.asksaveasfile('w')
    variated_file.write('T' + '\t' + 'qmc' + '\t' + 'st' + '\t' +
                        'TIME' + '\t' + 'LON' + '\t' + 'LAT' + '\t' + 'ALT' + '\n')
    for point in variated_magnetic_points:
        variated_file.write(str(point[0]) + '\t' + point[1] + '\t' + point[2] + '\t' +
                        point[3] + '\t' + point[4] + '\t' + point[5] + '\t' + point[6] + '\n')
    variated_file.close()

variations_calculate()

