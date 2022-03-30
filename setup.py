from cx_Freeze import setup, Executable
import sys
build_exe_option = {"packages":["os","sched","time","datetime","mysql.connector","shutil","json","numpy"]}

# ada
base = None
if sys.platform == "win32":
    base = "Win32GUI"



setup(
    name="pri_reader",
    version='0.0.1',
    description ='Tradutor de arquivos pri',
    options = {"build_exe":build_exe_option},
    executables = [Executable("pri_reader.py",base=base)]
)
