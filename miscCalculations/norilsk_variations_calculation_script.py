from tkinter import filedialog
from common.SplinesArray import *
from datetime import *
import math
import statistics


outer_variation_files = filedialog.askopenfilenames(title="Choose outer variation files",
                                                  filetypes=(("Template files", "*.txt"), ("All files", "*.*")))

value_points_full_vector = []
value_points_z_only = []
outer_variations_function_full_vector = SplinesArray()
outer_variations_function_z_only = SplinesArray()

for filename in outer_variation_files:
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        value = line.replace('\n', '').split(' ')
        year = int(value[0])
        month = int(value[1])
        day = int(value[2])
        hour = int(value[3])
        minute = int(value[4])
        sec = int(value[5])
        date_time = datetime(year,month, day, hour, minute, sec)
        x = float(value[6])
        y = float(value[7])
        z = float(value[8])
        full_vector = math.sqrt(x**2 + y**2 + z**2)
        value_points_full_vector.append((date_time.timestamp(), full_vector))
        value_points_z_only.append((date_time.timestamp(), z))
    file.close()
    outer_variations_function_full_vector.add_spline(value_points_full_vector)
    outer_variations_function_z_only.add_spline(value_points_z_only)
    value_points_full_vector = []
    value_points_z_only = []

var_filenames = filedialog.askopenfilenames(title="Choose our variation files",
                                                  filetypes=(("Template files", "*.txt"), ("All files", "*.*")))

value_points = []

for var_filename in var_filenames:
    file = open(var_filename, 'r')
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

        try:
            full_vector_value = outer_variations_function_full_vector.get_value(date_time)
            z_only_value = outer_variations_function_z_only.get_value(date_time)
        except:
            print("Variations not found for magnetic record: {}".format(datetime.fromtimestamp(date_time)))
            continue
        full_vector_difference = variation_t - full_vector_value
        z_only_difference = variation_t - z_only_value
        value_points.append((variation_t, full_vector_value, z_only_value, full_vector_difference, z_only_difference, date_time))

result_file = filedialog.asksaveasfile('w')


full_vector_difference_math_expectation = statistics.mean(list(map(lambda x: x[3], value_points)))
full_vector_difference_std_deviation = statistics.stdev(list(map(lambda x: x[3], value_points)))
z_only_difference_math_expectation = statistics.mean(list(map(lambda x: x[4], value_points)))
z_only_difference_std_deviation = statistics.stdev(list(map(lambda x: x[4], value_points)))

result_file.write(";;Math expectation of full vector variation difference: {}\n".format(full_vector_difference_math_expectation))
result_file.write(";;Std deviation of full vector variation difference: {}\n".format(full_vector_difference_std_deviation))
result_file.write(";;Math expectation of z only variation difference: {}\n".format(z_only_difference_math_expectation))
result_file.write(";;Std deviation of z only variation difference: {}\n".format(z_only_difference_std_deviation))
result_file.write('\n')
result_file.write('datetime' + '\t' + 'pos_var' + '\t' + 'full_vector_var' + '\t' + 'z_only_var' + '\t' +
                        'full_vector_diff' + '\t' + 'z_only_diff' + '\n')
for value in value_points:
    result_file.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(datetime.fromtimestamp(value[5]).strftime("%d-%m-%YT%H:%M:%S,%f"), value[0], value[1], value[2], value[3], value[4]))
result_file.close()





