@echo off

::�����ļ���
set newdir=releases\window_monitor_NEW
mkdir %newdir%

::�����ļ�
cp _config.json               %newdir%
cp restart_window_monitor.bat %newdir%
cp restore_windows.bat        %newdir%
cp restore_windows.py         %newdir%
cp show_json_more.bat         %newdir%
cp VirtualDesktop.dll         %newdir%
cp window_monitor_nogui.exe   %newdir%

echo finished.
echo ���Ƶ��� %newdir% �ļ�����
pause

