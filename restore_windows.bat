@echo off

set /p var=������_program_history.json��д��ʱ���:

cmd /c python "%~dp0restore_windows.py" %var%

pause