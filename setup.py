__author__ = 'jparaske'
import sys
from cx_Freeze import setup, Executable

setup(
    name = "MBB40H",
    version = "1.0",
    description = "SABA total training time counter",
    executables = [Executable("mbb40.py", 
    shortcutName="MBB40H",
    shortcutDir="DesktopFolder",
    icon="chronometer.ico")])