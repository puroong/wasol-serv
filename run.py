import wasol
import shutil
import os
import sys
import platform

def prepare_win():
    # add python37 to system path
    python_path = '\\'.join(sys.executable.split('\\')[:-1])
    os.environ['PATH'] = f"{os.environ['PATH']}{python_path};"

    # add cur path as pythonpath
    wasol_path = os.getcwd()
    os.environ['PYTHONPATH'] = f"{os.environ['PYTHONPATH']}{wasol_path};"

    # move python37\lib\site-packages\pywin32_system dlls to python37\lib\site-packages\win32
    dll_path = f"{python_path}\\Lib\\site-packages\\pywin32_system32"
    if not os.path.exists(dll_path):
        raise Exception("pywin32 is not installed")

    dll_basenames = os.listdir(dll_path)
    dll_fullpaths = [f"{dll_path}\\{dll_basename}" for dll_basename in dll_basenames] 
    win32_path = f"{python_path}\\Lib\\site-packages\\win32"
    for dll_fullpath, dll_basename in zip(dll_fullpaths, dll_basenames):
        if not os.path.exists(f"{win32_path}\\{dll_basename}"):
            shutil.copy(dll_fullpath, f"{win32_path}\\{dll_basename}")

if __name__ == "__main__":
    plat_sys = platform.system()
    if plat_sys == "Windows":
        prepare_win()
        wasol.daemon.win.WasolService.parse_command_line(sys.argv)