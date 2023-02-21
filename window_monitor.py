# encoding=utf-8
import clr
import os,sys,re,json,time
import psutil
import win32gui
import win32process
# from subprocess import PIPE, Popen
# python调用命令行：https://zhuanlan.zhihu.com/p/329957363

exe_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(exe_dir) # 切换到文件所在目录
# python调用cs: https://zhuanlan.zhihu.com/p/145617607
clr.AddReference('VirtualDesktop')
#clr.FindAssembly("ClassLibrary1.dll") ## 加载c#dll文件
import VirtualDesktop
from VirtualDesktop import Desktop


now_hwnd_all = []
# except_list = ['Progman',"Windows.UI.Core.CoreWindow", "ApplicationFrameWindow"]
all_history = []
max_history_length = 500
seconds_per_loop = 10

program_history_json = "_program_history.json"
program_history_backup_json = "_program_history_backup.json"
config_json = "_config.json"
log_txt = "_log.txt"
last_hwnd_all = None

def log(message):
    with open(log_txt, "a", encoding="utf8") as f:
        out_info = "[ "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "] " + message+"\n"
        print(out_info)
        f.write(out_info)

log(exe_dir)

# 被调用的工具函数
def _get_all_hwnd_func(hwnd,mouse):
    global now_hwnd_all
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        _title = win32gui.GetWindowText(hwnd)
        # _class = win32gui.GetClassName(hwnd)
        if _title!="":
            # # proc = Popen('VirtualDesktop.exe "gdfwh:'+_title+'"',stdin=None,stdout=PIPE,stderr=PIPE,shell=True)
            # proc2 = Popen('VirtualDesktop.exe "gdfwh:'+str(hwnd)+'"',stdin=None,stdout=PIPE,stderr=PIPE,shell=True)
            # infoout2, infoerr2 = proc2.communicate()
            # infoout2=infoout2.decode("gbk")
            # infoerr2=infoerr2.decode("gbk")
            # # if infoerr != "":
            # if infoerr2 != "":
            #     dbg=1
            # else:
            #     # (desktop1, desktopname1) = re.search(r"is on desktop number (.*) \(desktop \'(.*)'\)", infoout).groups()
            #     (desktop2, desktopname2) = re.search(r"is on desktop number (.*) \(desktop \'(.*)'\)", infoout2).groups()
            #     thread, processId = win32process.GetWindowThreadProcessId(hwnd)
            #     exename = psutil.Process(processId).name()
            #     # hwnd_title.append([desktop2, desktopname2, hwnd, thread, processId, exename, _title])
            #     now_hwnd_all["arr"].append((desktop2, desktopname2, processId, hwnd, exename, _title))
            try:
                rc = VirtualDesktop.Desktop.FromDesktop(VirtualDesktop.Desktop.FromWindow(hwnd))
            except Exception:
                return
            desktop3, desktopname3 = str(rc), VirtualDesktop.Desktop.DesktopNameFromIndex(rc)
            thread, processId = win32process.GetWindowThreadProcessId(hwnd)
            exename = psutil.Process(processId).name()
            now_hwnd_all["arr"].append((desktop3, desktopname3, processId, hwnd, exename, _title))

def update_hwnd_arr():
    global now_hwnd_all
    _timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    now_hwnd_all = {"time": _timestamp,
                    "note": "窗口id, 窗口名, 进程id, 句柄id, exe名, 窗口标题",
                    "count": 0,
                    "arr": []}
    desktop_index = 0
    process_index = 2
    hwnd_index = 3
    exe_index = 4
    win32gui.EnumWindows(_get_all_hwnd_func, 0)
    now_hwnd_all["arr"].sort(key=lambda x: (x[desktop_index],x[exe_index],x[hwnd_index]))
    now_hwnd_all["count"] = len(now_hwnd_all["arr"])

def get_all_pid(): # 输出全部，但太多了，弃用
    # pids = psutil.pids()
    # for pid in pids:
    #     p = psutil.Process(pid)
    #     print("pid-%d,pname-%s" %(pid,p.name()))
    pass

# 可选择性使用
def show_all():
    update_hwnd_arr()
    print("index, desktopname, processId, hwnd, exename, _title")
    for i in now_hwnd_all["arr"]:
        print(i)

# 可选择性使用
def get_exe_wind(exe_name=None): # None的话就输出全部
    global now_hwnd_all
    update_hwnd_arr()
    new_wind = []
    exe_index = 4
    print("index, desktopname, processId, hwnd, exename, _title")
    for i in now_hwnd_all["arr"]:
        if exe_name is None or i[exe_index] == exe_name:
            print(i)
        new_wind.append(i)
    return new_wind

# get_all_pid() # 弃用
# get_exe_wind("explorer.exe")
# get_exe_wind()
# show_all()

def get_json(json_filename):
    # 检查json文件有没有
    if os.path.exists(json_filename):
        with open(json_filename, "r", encoding="utf8") as f:
            json_obj = json.load(f)
        return json_obj
    else:
        return []

def write_obj_to_json(obj, out_json_filename, indent=4, end=""):
    # 输出到文件
    with open(out_json_filename, "w", encoding="utf8") as f:
        _dumps = json.dumps(obj, indent=indent, ensure_ascii=False)
        _dumps = _dumps.replace("\n                "," ")
        _dumps = _dumps.replace("\n            ]"," ]")
        f.write(_dumps)
        f.write(end)
    

def get_last_hwnd_all_from_json():
    global all_history
    all_history = get_json(program_history_json)
    if len(all_history) > 0:
        return all_history[0]
    else:
        return None

def save_last_hwnd_all_to_history(a_last):
    all_history.insert(0, a_last)
    if len(all_history) > max_history_length: # 清除第一次，避免长度超过 max_history_length
        all_history.pop()
    if len(all_history) > max_history_length: # 清除第二次，确认避免长度超过 max_history_length
        all_history.pop()
        all_history.pop()
    write_obj_to_json(all_history, program_history_json)

# 保留10000条记录，每3秒记录一次，共约8.3小时
if __name__ == "__main__":
# def program_main():
    cfg = get_json(config_json)
    max_history_length = cfg["max_history_length"]
    seconds_per_loop = cfg["seconds_per_loop"]
    log(f"最长历史纪录 {max_history_length} ，正在每 {seconds_per_loop} 秒一次监视所有窗口状态...")
    if last_hwnd_all is None: # 刚运行程序
        last_hwnd_all = get_last_hwnd_all_from_json()
    if last_hwnd_all is None: # 没有历史json，就获取一个当前的值
        update_hwnd_arr()
        last_hwnd_all = now_hwnd_all
        save_last_hwnd_all_to_history(last_hwnd_all)
    while True:
        # 再次获取窗口，然后和last比对，如果不同则
        # log("updating...")
        update_hwnd_arr()
        if last_hwnd_all["arr"] != now_hwnd_all["arr"]:
            last_hwnd_all = now_hwnd_all
            log("saving...")
            save_last_hwnd_all_to_history(last_hwnd_all)
        dbg=1
        # log("sleeping...")
        time.sleep(seconds_per_loop/2)
        write_obj_to_json(all_history, program_history_backup_json)
        time.sleep(seconds_per_loop/2)
a=1