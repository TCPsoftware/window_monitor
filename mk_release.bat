@echo off

::创建文件夹
set newdir=releases\window_monitor_NEW
mkdir %newdir%

::复制文件
cp _config.json               %newdir%
cp restart_window_monitor.bat %newdir%
cp restore_windows.bat        %newdir%
cp restore_windows.py         %newdir%
cp show_json_more.bat         %newdir%
cp VirtualDesktop.dll         %newdir%
cp window_monitor_nogui.exe   %newdir%

echo finished.
echo 复制到了 %newdir% 文件夹中
pause

