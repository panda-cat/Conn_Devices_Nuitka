#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build a standalone executable using cx_freeze"""

from cx_Freeze import setup, Executable

setup(
    name = "myapp",
    version = "0.1",
    description = "Connect to network devices and execute commands using netmiko",
    executables = [Executable("myapp_scripts.py")],
    platforms=["win32", "win64", "macosx", "linuxx86_64"],
    packages=['netmiko', 'openpyxl', 'argparse', 'os', 'datetime', 'sys', 're', 'uuid', 'tqdm', 'paramiko==3.5.0'],
)
