#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build a standalone executable using cx_freeze"""

import os  # Add this missing import
import sys  # This is used and should also be included
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need to be explicitly included.
build_exe_options = {
    "packages": [
        "netmiko",
        "openpyxl",
        "argparse",
        "tqdm",
        "paramiko",
        "encodings.idna",
        "concurrent.futures",
        "tempfile",
        "uuid",
        "typing",
        "time",
        "datetime",
        "os",
        "sys",
        "re",
        "threading"
    ],
    "excludes": []
}

setup(
    name="myapp",
    version="0.2",
    description="Network device batch management tool using netmiko",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="myapp_scripts.py",
            targetName="myapp",  # Output executable name
            base=None if os.name != "nt" else "Win32GUI",  # Console app for non-Windows
        )
    ],
    platforms=["win32", "win64", "macosx", "linuxx86_64"],
)
