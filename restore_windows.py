# encoding=utf-8

import os,sys,re,json,time
import psutil
import win32gui,win32con
import win32process
# from subprocess import PIPE, Popen
# python调用命令行：https://zhuanlan.zhihu.com/p/329957363
import winreg
from window_monitor import update_hwnd_arr, Desktop

exe_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(exe_dir) # 切换到文件所在目录

userhomepath = os.environ['USERPROFILE']
userdir = os.path.split(userhomepath)[-1]
special_dir_dict = {
    "音乐":"My Music",
    "视频":"My Video",
    "图片":"My Pictures",
    "下载":"{374DE290-123F-4565-9164-39C4925E467B}",
    "文档":"Personal",
    "桌面":"Desktop"
}
program_history_json = "_program_history.json"
program_history_backup_json = "_program_history_backup.json"

def get_true_path(_window_title):
    if os.path.splitdrive(_window_title)[0] == "":
        _window_title = get_special_path(_window_title)
    return _window_title

def get_special_path(title):# 获取桌面、下载等路径
    if title == userdir:
        return userhomepath
    if title in special_dir_dict:
        to_query = special_dir_dict[title]
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        got_value = winreg.QueryValueEx(key, to_query)[0]
        winreg.CloseKey(key)
        return got_value
    return None

def get_json(json_filename):
    # 检查json文件有没有
    if os.path.exists(json_filename):
        with open(json_filename, "r", encoding="utf8") as f:
            json_obj = json.load(f)
        return json_obj
    else:
        return []

def main():
    arg = sys.argv
    length = len(arg)
    if length == 2:
        timestamp = arg[-1]
        print("待查找时间戳:",timestamp)
        read_history1 = get_json(program_history_json)
        read_history2 = get_json(program_history_backup_json)
        if len(read_history1) >= len(read_history2):
            all_history = read_history1
        else:
            all_history = read_history2
        found = None
        for obj in all_history:
            if "timestamp" not in obj.keys():
                found = None
                break
            if obj["timestamp"] == int(timestamp):
                found = obj
                break
        if not found:
            print("    未找到 timestamp，请检查 _program_history*.json 后输入")
            return
        # found object
        explorer_arr = []
        for obj in found["arr"]:
            dbg=1
            if obj[4] == "explorer.exe":
                explorer_arr.append(obj)
        explorer_arr.reverse()
        started_arr = []
        started_titles = []
        error_list = []
        print("● 找到如下窗口：")
        for obj in explorer_arr:
            _desk_id,_desk_name,_window_title = obj[0],obj[1],get_true_path(obj[5])
            print('index{}\t"{}"\texplorer.exe "{}"'.format(_desk_id,_desk_name,_window_title))
            try:
                obj[5] = _window_title
                if _window_title not in started_titles:
                    os.startfile(_window_title)
                    started_titles.append(_window_title)
                else:
                    os.system('explorer.exe "{}"'.format(_window_title))
                started_arr.append(obj)
            except Exception:
                error_list.append(obj)
        if error_list:
            print("● 遇到了错误，没有打开的窗口有：")
            for obj in error_list:
                _desk_id,_desk_name,_window_title = obj[0],obj[1],obj[5]
                print('index{}\t"{}"\texplorer.exe "{}"'.format(_desk_id,_desk_name,_window_title))
        print("● 等待 10s，等待窗口全部打开...")
        time.sleep(10)
        dbg=1
        # 获取所有资源管理器的窗口
        hwnd_all = update_hwnd_arr(return_value=True)
        explorer_arr = []
        for obj in hwnd_all["arr"]:
            dbg=1
            if obj[4] == "explorer.exe":
                explorer_arr.append(obj)
        dbg=1
# # 引用
# from window_monitor import Desktop
# # 移动窗口
# rc = 1
# iParam = 132010 # obj[3] 窗口id
# VirtualDesktop.Desktop.FromIndex(rc).MoveWindow(iParam)
        for obj in started_arr:
            _desk_id, _window_title = int(obj[0]), get_true_path(obj[5])
            for index in range(len(explorer_arr)):
                _window_hwnd = explorer_arr[index][3]
                if get_true_path(explorer_arr[index][5]) == _window_title: # 匹配上了
                    time.sleep(0.2)
                    win32gui.ShowWindow(_window_hwnd, win32con.SW_SHOWNORMAL)
                    time.sleep(0.2)
                    Desktop.FromIndex(_desk_id).MoveWindow(_window_hwnd) # 移动窗口
                    explorer_arr.pop(index)
                    dbg=1
                    break
        not_moved_arr = explorer_arr
        if not_moved_arr:
            print("● 以下窗口多余，输入 n 并回车以忽略这些窗口，直接回车关闭这些窗口。")
            for obj in not_moved_arr:
                _desk_id,_desk_name,_window_title = obj[0],obj[1],obj[5]
                print('index{}\t"{}"\texplorer.exe "{}"'.format(_desk_id,_desk_name,_window_title))
            while True:
                choice=input("输入 n 并回车以忽略这些窗口，直接回车关闭这些窗口: ")
                if choice in ['n',""]:
                    break
                else:
                    print("输入错误.")
            if choice == 'n':
                for obj in not_moved_arr:
                    win32gui.PostMessage(obj[3], win32con.WM_CLOSE, 0, 0)
                    dbg=1
        dbg=1
        if error_list:
            print("===== 存在 窗口打开 错误，请自行检查，并向开发者汇报错误 =====")
            print("===== 存在 窗口打开 错误，请自行检查，并向开发者汇报错误 =====")
            print("===== 存在 窗口打开 错误，请自行检查，并向开发者汇报错误 =====")
        else:
            print(" √ 操作已完成，没毛病 √ ")
            print(" √ 操作已完成，没毛病 √ ")
            print(" √ 操作已完成，没毛病 √ ")
    else:
        print("    Usage: python {} [timestamp]".format(arg[0]))
    dbg=1

if __name__ == "__main__":
    main()
    print("")

