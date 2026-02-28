# -*- coding: utf-8 -*-
"""
Utility functions: disk info, admin check, size formatting.
"""

import ctypes
import os
import sys
import psutil


def is_admin() -> bool:
    """Check if the current process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """Re-launch the current process with administrator privileges."""
    if is_admin():
        return
    try:
        script = sys.argv[0]
        params = " ".join(sys.argv[1:])
        
        executable = sys.executable
        if executable.lower().endswith("python.exe"):
            executable = executable[:-10] + "pythonw.exe"
            
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", executable, f'"{script}" {params}', None, 1
        )
    except Exception:
        pass
    sys.exit(0)


def get_disk_info(drive: str = "C:\\") -> dict:
    """
    Returns disk usage info for the given drive.
    Returns a dict with keys: total, used, free (all in bytes), percent.
    """
    try:
        usage = psutil.disk_usage(drive)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
        }
    except Exception:
        return {"total": 0, "used": 0, "free": 0, "percent": 0}


def format_size(size_bytes: float, decimals: int = 2) -> str:
    """
    Converts bytes to a human-readable string.
    E.g. 1536 -> '1.50 KB', 1073741824 -> '1.00 GB'
    """
    if size_bytes <= 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    val = float(size_bytes)
    while val >= 1024 and i < len(units) - 1:
        val /= 1024.0
        i += 1
    return f"{val:.{decimals}f} {units[i]}"


def get_folder_size(path: str) -> int:
    """
    Recursively calculates the total size (bytes) of a folder.
    Silently skips permission errors and missing files.
    """
    if not os.path.exists(path):
        return 0
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path, onerror=None):
            for f in filenames:
                try:
                    fp = os.path.join(dirpath, f)
                    total += os.path.getsize(fp)
                except (OSError, PermissionError):
                    pass
    except Exception:
        pass
    return total


def expand_env(path: str) -> str:
    """Expand environment variables in a path string."""
    return os.path.expandvars(path)


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and PyInstaller bundle.
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
