@echo off
set y=%date:~0,4%
set m=%date:~5,2%
set d=%date:~8,2%
set h=%time:~0,2%
set mi=%time:~3,2%
set s=%time:~6,2%
set filename=0
set /p filenamem=请将主Python脚本拖放至此处：
if %filenamem% == 0 exit
set folder=%filenamem%_test_%y%_%m%_%d%_%h%_%mi%_%s%
mkdir %folder%
echo import time>>%folder%\%filenamem%
echo.>>%folder%\%filenamem%
type %filenamem%>>%folder%\%filenamem%
echo.>>%folder%\%filenamem%
echo print()>>%folder%\%filenamem%
echo print(time.process_time())>>%folder%\%filenamem%
echo subprocess.call("pause",shell=True)>>%folder%\%filenamem%
:cycle
set filename=0
set /p filename=请将Python脚本拖放至此处，它们不会被增加暂停代码：
if %filename% == 0 goto cycle
echo import time>>%folder%\%filename%
echo.>>%folder%\%filename%
type %filename%>>%folder%\%filename%
echo.>>%folder%\%filename%
echo print()>>%folder%\%filename%
echo print(time.process_time())>>%folder%\%filename%
goto cycle