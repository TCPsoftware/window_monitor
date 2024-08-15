# window_monitor

监控所有窗口，并记录到json文件，当资源管理器崩溃或者系统重启，可以查看json恢复你的工作

## 编译和运行方法（手动版）

```cmd
pyinstaller打包：（不推荐）
pyinstaller.exe -F -c --noupx window_monitor.py 

nuitka打包：（推荐）
知乎 nuitka：https://zhuanlan.zhihu.com/p/165978688
nuitka --standalone --onefile --windows-disable-console window_monitor.py -o window_monitor_nogui.exe
上面命令行使用旧版本1.4.7。nuitka 2.4.5 要求使用新的参数名，因此命令行为：
nuitka --standalone --onefile --windows-console-mode=disable window_monitor.py -o window_monitor_nogui.exe


VirtualDesktop.dll编译：
C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /target:library /out:VirtualDesktop.dll VirtualDesktop.cs


python运行时先安装需要的库：
pip install -r .\requirements.txt

运行方式：
pythonw window_monitor.py（不推荐）
Start-Process -WindowStyle Hidden .\window_monitor.exe (文件名：run_with_new_process.ps1)（不推荐）
window_monitor_nogui.exe （推荐）

```

## 运行方法（简洁版）

- 从 releases 下载最新的 window_monitor_vXX.zip，解压
- 将文件夹放置在合适的位置
- 双击 window_monitor_nogui.exe 运行
- 运行后没有界面，同目录下会生成 `_log.txt` `_program_history.json` `_program_history_backup.json` 三个文件
- 如果要结束程序，可以打开任务管理器，详细信息，找到 window_monitor_nogui.exe，结束任务

## json配置文件

`_config.json` 为配置文件，运行前可能需要根据需求或环境来设置合适的值。

样例内容：

```json
{
    "max_history_length": 400,
    "seconds_per_loop": 20,
    "VirtualDesktop_DLL_name": "VirtualDesktop_v1.18"
}
```

参数说明：

- **max_history_length**：历史记录最大状态数量，超过将去除最旧的状态
- **seconds_per_loop**：间隔时间，每隔此时间监测一次窗口状态
- **VirtualDesktop_DLL_name**：对应VirtualDesktopDLL文件夹中的dll路径，与Windows版本有关，根据Windows版本选择对应的dll。注意不带目录路径和后缀名
  - `VirtualDesktop_v1.18`：适用于Windows 10
  - `VirtualDesktop11_v1.18`：适用于Windows 11
  - `VirtualDesktop11_24H2_v1.18`：适用于Windows 11 24H2
  - 如有其他版本Windows或DLL修改后仍然不能正常获取窗口，可以提交反馈。

## 运行效果

![running.png](images/running.png)

## 相关repo

MScholtes/VirtualDesktop:  [https://github.com/MScholtes/VirtualDesktop](https://github.com/MScholtes/VirtualDesktop)
