
@echo off

set "script_dir=%~dp0"
set "program_name=window_monitor_nogui.exe"

:loop
echo �������Ƿ�����
tasklist | find /i "window_monitor_nogui.exe"

IF %ERRORLEVEL% NEQ 0 (
    echo *** ����δ������ �� ***
) ELSE (
    echo *** ������������ �� ***
)

echo.
echo "  1. �˳�ѭ���������� q d��"
echo "  2. ���� window_monitor_nogui.exe ����"
echo "  3. ���� window_monitor_nogui.exe ����"
echo "  4. �鿴 _program_history.json �ļ�ǰʮ������"
echo.

REM ����choice��ǿ���û������µ�ѡ��
set "choice=0"
set /p choice=������ָ��: 
echo ���������Ϊ��%choice%��
IF "%choice%"=="1" (
    goto end
) ELSE IF "%choice%"=="d" (
    goto end
) ELSE IF "%choice%"=="q" (
    goto end
) ELSE IF "%choice%"=="2" (
    taskkill /f /im "%program_name%"
) ELSE IF "%choice%"=="3" (
    start "" "%script_dir%%program_name%"
) ELSE IF "%choice%"=="4" (
    start cmd /c "show_json_more.bat"
) ELSE (
    echo ��Ч��ָ�����������
)

goto loop

:end
exit /b
