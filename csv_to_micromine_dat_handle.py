from tkinter import filedialog
import os


input_file = filedialog.askopenfilename(title="Choose variation files", filetypes=(("input CSV", "*.csv"), ("All files", "*.*")))

# output_file = filedialog.asksaveasfile('w')

# print(input_file)
import os
path_to_file = os.path.dirname(os.path.abspath(input_file))
name, extention = os.path.basename(os.path.abspath(input_file)).split('.')
# print(path_to_file)
# print(name)

first_line = 40

output_filename = (path_to_file + '//' + name + '.' + 'dat').replace('\\', '//')
# print(output_filename)
# print(len(name))
out_file = open(output_filename, 'w')
out_file.write(name + (first_line - len(name)) * ' '  + '\n')
out_file.write('3   VARIABLES' + '\n')
out_file.write('x         N 20  5' + '\n')
out_file.write('y         N 20  5' + '\n')
out_file.write('y         N 20  5' + '\n')

in_file = open(input_file, 'r')


lines = in_file.readlines()
for line in lines:
    cols = line.split(';')
    try:
        x_var = format(float(cols[0]), '.2f')
        y_var = format(float(cols[1]), '.2f')
        z_var = format(float(cols[2]), '.2f')
    except:
        continue

    out_file.write(x_var + (20 - len(x_var)) * ' ')
    out_file.write(y_var + (20 - len(y_var)) * ' ')
    out_file.write(z_var + (20 - len(z_var)) * ' ')
    out_file.write('\n')

in_file.close()
out_file.close()


