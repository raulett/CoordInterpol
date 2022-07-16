from tkinter import filedialog
import datetime

reference_table_num = 1
source_table_num = 0
ref_datetime_format = '%d-%m-%YT%H:%M:%S' #02-09-2021T03:04:01
source_datetime_format = '%d-%m-%YT%H:%M:%S' #02-09-2021T03:04:01

reference_filenames = filedialog.askopenfilenames(title="get reference file")
source_filenames = filedialog.askopenfilenames(title="get source files")
result_intersection_file = filedialog.asksaveasfile(title="result file", mode='w')

reference_dataset = dict()
for filename in reference_filenames:
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        try:
            reference_timestamp = datetime.datetime.strptime(line.split('\t')[reference_table_num], ref_datetime_format).timestamp()
        except ValueError:
            print("Datetime parse error: {}".format(line.split('\t')[reference_table_num]))
            continue
        reference_dataset[reference_timestamp] = 1
    file.close()

print("got {} reference record".format(len(reference_dataset)))

got_title_flag = 0

for filename in source_filenames:
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        try:
            source_timestamp = datetime.datetime.strptime(line.split('\t')[source_table_num], source_datetime_format).timestamp()
        except ValueError:
            if not got_title_flag:
                result_intersection_file.write(line)
                got_title_flag = 1
            print(ValueError)
            continue
        if reference_dataset.get(source_timestamp, 0):
            result_intersection_file.write(line)
    file.close()

result_intersection_file.close()

