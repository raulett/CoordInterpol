import os
import subprocess
import re

def compile_files():
    extention_pattern = re.compile('.*\.ui$')

    current_path = os.path.dirname(os.path.abspath(__file__)).split('\\')
    root_path = '\\'.join(current_path[0: len(current_path)-1])+"\\"
    ui_path = root_path+'UI\\'
    print(ui_path)




    def get_ui_files(dir_name):
        ui_files = []
        for root, dirs, files in os.walk(dir_name):
            ui_files += [os.path.join(root, name) for name in files if re.search(extention_pattern, name)]
        print(ui_files)
        return ui_files

    ui_files = get_ui_files(ui_path)

    # subprocess.call(['pyrcc5.exe', "-o", root_path+'resources.py', root_path+'resources.qrc'])
    # print('*.qrc compiled')

    for ui_file in ui_files:
        ui_filename_without_ex = os.path.basename(ui_file).split('.')[:-1][0]
        path_for_output = os.path.dirname(ui_file)
        output_filename = path_for_output + '\\' + ui_filename_without_ex + '_ui.py'
        subprocess.call(['pyuic5.exe', "-o", output_filename, ui_file])
        print('{} UI file compiled to {} py file.'.format(ui_file, output_filename))



compile_files()