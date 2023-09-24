
@echo off

set "script_dir=%~dp0"
set "program_name=window_monitor_nogui.exe"

:loop
echo 检查进程是否运行
tasklist | find /i "window_monitor_nogui.exe"

IF %ERRORLEVEL% NEQ 0 (
    echo *** 程序未在运行 × ***
) ELSE (
    echo *** 程序正在运行 √ ***
)

echo.
echo "  1. 退出循环（或输入 q d）"
echo "  2. 结束 window_monitor_nogui.exe 程序"
echo "  3. 启动 window_monitor_nogui.exe 程序"
echo "  4. 查看 _program_history.json 文件前十行内容"
echo.

REM 重置choice，强制用户输入新的选择
set "choice=0"
set /p choice=请输入指令: 
echo 输入的内容为【%choice%】
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
    echo 无效的指令，请重新输入
)

goto loop

:end
exit /b
