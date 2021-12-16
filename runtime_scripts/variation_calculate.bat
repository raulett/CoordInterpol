cd /d %~dp0
cd ..

set /p general_field="Input general field: "
%PYTHONPATH%python.exe %CD%\variations_calculate.py %general_field%