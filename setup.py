__author__ = 'ioparaskev'
from sys import platform, version_info
from cx_Freeze import setup, Executable

base = None
if platform == "win32":
    base = "Win32GUI"

if version_info < (3,):
    print('Python version 2.x is not supported')

setup(
    name="Training time calculator",
    version="1.1",
    description="Training time calculator",
    executables=[Executable("ttcalc_gui.py",
                            shortcutName="Training time calculator",
                            shortcutDir="DesktopFolder",
                            icon="chronometer.ico", base=base)],
    install_requires=['cx_Freeze'])
