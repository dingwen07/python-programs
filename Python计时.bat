@echo off
:cycle
set filename=0
set /p filename=�뽫Python�ű��Ϸ����˴���
if %filename% == 0 exit
echo import time>>part1.txt
echo.>>part1.txt
copy %filename% part2.txt
copy /b part1.txt + /b part2.txt /b %filename%
del part1.txt
del part2.txt
echo.>>%filename%
echo print()>>%filename%
echo print(time.process_time())>>%filename%
pause
goto cycle