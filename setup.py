#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from cx_Freeze import setup, Executable

# 检查是否为 Windows 平台
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# 包含的依赖项
build_exe_options = {
    "packages": [
        "netmiko",
        "openpyxl",
        "argparse",
        "os",
        "datetime",
        "sys",
        "re",
        "uuid",
        "tempfile",
        "time",
        "typing",
        "concurrent.futures",
        "threading",
        "encodings.idna",
        "tqdm",
    ],
    "excludes": []
}

# 设置 cx_Freeze
setup(
    name="NetworkDeviceManager",
    version="5.0",
    description="网络设备批量管理工具",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="myapp_scripts.py",
            target_name="NetworkDeviceManager.exe",
            base=base
        )
    ],
)
