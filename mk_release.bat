@echo off

::�����ļ���
set newdir=releases\window_monitor_NEW
mkdir %newdir%

::�����ļ���cp��ʹ�õ�linux����
cp _config.json               %newdir%
cp restart_window_monitor.bat %newdir%
cp restore_windows.bat        %newdir%
cp restore_windows.py         %newdir%
cp show_json_more.bat         %newdir%
cp -r  VirtualDesktopDLL      %newdir%
cp window_monitor_nogui.exe   %newdir%
cp README.md                  %newdir%
cp requirements.txt           %newdir%
cp window_monitor.py          %newdir%

echo finished.
echo ���Ƶ��� %newdir% �ļ�����
pause

