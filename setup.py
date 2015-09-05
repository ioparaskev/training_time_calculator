__author__ = 'jparaske'
from sys import platform, version_info
from cx_Freeze import setup, Executable

base = None
if platform == "win32":
    base = "Win32GUI"

if version_info < (3,):
    print('Python version 2.x is not supported')

setup(
    name = "MBB40H",
    version = "0.8",
    description = "SABA total training time counter",
    executables = [Executable("mbb40.py", 
    shortcutName="MBB40H",
    shortcutDir="DesktopFolder",
    icon="chronometer.ico", base=base)],
    install_requires=[
          'cx_Freeze',
      ])