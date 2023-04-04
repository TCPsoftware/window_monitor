@echo off

set /p var=请输入_program_history.json里写的时间戳:

cmd /c python "%~dp0restore_windows.py" %var%

pause