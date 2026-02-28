# -*- coding: utf-8 -*-
"""
Core cleaning logic. Mirrors the 8 steps in cleanup_c_drive_en.ps1
but implemented natively in Python for better GUI integration.

Each cleaner function accepts a callback:
    callback(status, description, freed_bytes)
where status is one of: 'ok', 'skip', 'warn', 'info', 'bg'
"""

import os
import shutil
import subprocess
import winreg
from datetime import datetime, timedelta
from typing import Callable, List, NamedTuple, Optional

from utils import get_folder_size, expand_env


# ─────────────────────────────────────────────
#  Data structures
# ─────────────────────────────────────────────

class CleanItem(NamedTuple):
    """Metadata for a single cleanup item shown in the UI."""
    key: str            # matches i18n key suffix, e.g. "user_temp"
    icon: str           # emoji icon
    default_on: bool    # checked by default?


# Ordered list matching the 8 PS1 steps
CLEAN_ITEMS: List[CleanItem] = [
    CleanItem("user_temp",    "🗂", True),
    CleanItem("sys_temp",     "🖥", True),
    CleanItem("win_update",   "🔄", True),
    CleanItem("browser",      "🌐", True),
    CleanItem("sys_logs",     "📋", True),
    CleanItem("recycle",      "🗑", True),
    CleanItem("other",        "📦", True),
    CleanItem("disk_cleanup", "⚙", False),
]

CallbackFn = Callable[[str, str, int], None]   # (status, description, freed_bytes)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def _delete_contents(path: str, days_old: int = 0, dry_run: bool = False) -> int:
    """
    Delete files/folders inside *path*.
    If days_old > 0, only delete items older than that many days.
    Returns bytes freed (approximate; uses size before deletion).
    """
    if not os.path.exists(path):
        return 0

    freed = 0
    cutoff = datetime.now() - timedelta(days=days_old) if days_old > 0 else None

    try:
        scandir_iter = os.scandir(path)
    except (PermissionError, OSError):
        return 0

    try:
        for entry in scandir_iter:
            try:
                if cutoff:
                    mtime = datetime.fromtimestamp(entry.stat(follow_symlinks=False).st_mtime)
                    if mtime >= cutoff:
                        continue

                if entry.is_dir(follow_symlinks=False):
                    size = get_folder_size(entry.path)
                    if not dry_run:
                        shutil.rmtree(entry.path, ignore_errors=True)
                    freed += size
                else:
                    size = entry.stat(follow_symlinks=False).st_size
                    if not dry_run:
                        os.remove(entry.path)
                    freed += size
            except (PermissionError, OSError):
                pass
    finally:
        scandir_iter.close()

    return freed


def _process_path(path: str, label: str, cb: CallbackFn,
                  days_old: int = 0, dry_run: bool = False) -> int:
    """Run _delete_contents on a single path and fire the callback."""
    path = expand_env(path)
    if not os.path.exists(path):
        cb("skip", label, 0)
        return 0

    freed = _delete_contents(path, days_old=days_old, dry_run=dry_run)
    if freed > 0:
        cb("ok", label, freed)
    else:
        cb("skip", label, 0)
    return freed


# ─────────────────────────────────────────────
#  Step 1 – User Temp Files
# ─────────────────────────────────────────────

def clean_user_temp(cb: CallbackFn, dry_run: bool = False) -> int:
    total = 0
    total += _process_path("%TEMP%",                          "TEMP",       cb, dry_run=dry_run)
    total += _process_path("%LOCALAPPDATA%\\Temp",            "LocalAppData\\Temp", cb, dry_run=dry_run)
    return total


# ─────────────────────────────────────────────
#  Step 2 – System Temp Files
# ─────────────────────────────────────────────

def clean_sys_temp(cb: CallbackFn, dry_run: bool = False) -> int:
    total = 0
    total += _process_path("C:\\Windows\\Temp",      "Windows\\Temp",    cb, dry_run=dry_run)
    total += _process_path("C:\\Windows\\Prefetch",  "Windows\\Prefetch", cb, days_old=30, dry_run=dry_run)
    return total


# ─────────────────────────────────────────────
#  Step 3 – Windows Update Cache
# ─────────────────────────────────────────────

def clean_win_update(cb: CallbackFn, dry_run: bool = False) -> int:
    if not dry_run:
        # Stop Windows Update service before cleaning
        subprocess.run(["sc", "stop", "wuauserv"], capture_output=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)

    total = _process_path(
        "C:\\Windows\\SoftwareDistribution\\Download",
        "Windows Update Cache", cb, dry_run=dry_run
    )

    if not dry_run:
        subprocess.run(["sc", "start", "wuauserv"], capture_output=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)

    return total


# ─────────────────────────────────────────────
#  Step 4 – Browser Cache
# ─────────────────────────────────────────────

def clean_browser(cb: CallbackFn, dry_run: bool = False) -> int:
    total = 0
    local = expand_env("%LOCALAPPDATA%")

    chrome_paths = [
        os.path.join(local, "Google", "Chrome", "User Data", "Default", "Cache"),
        os.path.join(local, "Google", "Chrome", "User Data", "Default", "Code Cache"),
        os.path.join(local, "Google", "Chrome", "User Data", "Default", "GPUCache"),
    ]
    edge_paths = [
        os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Cache"),
        os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Code Cache"),
    ]
    firefox_profiles = os.path.join(local, "Mozilla", "Firefox", "Profiles")

    for p in chrome_paths:
        total += _process_path(p, "Chrome Cache", cb, dry_run=dry_run)
    for p in edge_paths:
        total += _process_path(p, "Edge Cache", cb, dry_run=dry_run)

    if os.path.exists(firefox_profiles):
        for profile in os.scandir(firefox_profiles):
            if profile.is_dir():
                cache2 = os.path.join(profile.path, "cache2")
                total += _process_path(cache2, "Firefox Cache", cb, dry_run=dry_run)

    return total


# ─────────────────────────────────────────────
#  Step 5 – System Logs
# ─────────────────────────────────────────────

def clean_sys_logs(cb: CallbackFn, dry_run: bool = False) -> int:
    total = 0
    total += _process_path("C:\\Windows\\Logs\\CBS",  "CBS Logs",  cb, days_old=30, dry_run=dry_run)
    total += _process_path("C:\\Windows\\Logs\\DISM", "DISM Logs", cb, days_old=30, dry_run=dry_run)
    total += _process_path("C:\\inetpub\\logs",       "IIS Logs",  cb, days_old=30, dry_run=dry_run)

    if not dry_run:
        try:
            subprocess.run(["wevtutil", "cl", "Application"], capture_output=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["wevtutil", "cl", "System"],      capture_output=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            cb("ok", "Windows Event Logs", 0)
        except Exception:
            cb("warn", "Windows Event Logs", 0)

    return total


# ─────────────────────────────────────────────
#  Step 6 – Recycle Bin
# ─────────────────────────────────────────────

def clean_recycle(cb: CallbackFn, dry_run: bool = False) -> int:
    if dry_run:
        # Estimate recycle bin size
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "(New-Object -ComObject Shell.Application).Namespace(10).Items() | "
                 "Measure-Object -Property Size -Sum | Select-Object -ExpandProperty Sum"],
                capture_output=True, text=True, timeout=15,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            size = int(result.stdout.strip() or "0")
            cb("ok", "Recycle Bin", size)
            return size
        except Exception:
            cb("skip", "Recycle Bin", 0)
            return 0
    else:
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
                capture_output=True, timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            cb("ok", "Recycle Bin", 0)
        except Exception:
            cb("warn", "Recycle Bin", 0)
        return 0


# ─────────────────────────────────────────────
#  Step 7 – Other Caches
# ─────────────────────────────────────────────

def clean_other(cb: CallbackFn, dry_run: bool = False) -> int:
    total = 0
    local = expand_env("%LOCALAPPDATA%")
    prog_data = expand_env("%PROGRAMDATA%")

    paths = [
        ("C:\\Windows\\Installer\\$PatchCache$",                  "Installer Patch Cache", 0),
        (os.path.join(prog_data, "Microsoft", "Windows", "WER"), "System Error Reports",  7),
        (os.path.join(local,    "Microsoft", "Windows", "WER"),  "User Error Reports",    7),
        (os.path.join(local,    "D3DSCache"),                     "DirectX Shader Cache",  0),
        (os.path.join(local,    "npm-cache"),                     "NPM Cache",             30),
        (os.path.join(local,    "pip", "cache"),                  "pip Cache",             30),
    ]

    for path, label, days in paths:
        total += _process_path(path, label, cb, days_old=days, dry_run=dry_run)

    return total


# ─────────────────────────────────────────────
#  Step 8 – System Disk Cleanup (cleanmgr)
# ─────────────────────────────────────────────

def clean_disk_cleanup(cb: CallbackFn, dry_run: bool = False) -> int:
    if dry_run:
        cb("info", "System Disk Cleanup", 0)
        return 0

    try:
        # Pre-configure cleanup categories via registry
        reg_base = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches"
        categories = [
            "Active Setup Temp Folders", "Downloaded Program Files",
            "Internet Cache Files", "Old ChkDsk Files", "Recycle Bin",
            "Setup Log Files", "System error memory dump files",
            "System error minidump files", "Temporary Files",
            "Temporary Setup Files", "Thumbnail Cache", "Update Cleanup",
        ]
        for cat in categories:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{reg_base}\\{cat}",
                                     0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "StateFlags0001", 0, winreg.REG_DWORD, 2)
                winreg.CloseKey(key)
            except Exception:
                pass

        subprocess.Popen(["cleanmgr.exe", "/sagerun:1"], creationflags=subprocess.CREATE_NO_WINDOW)
        cb("bg", "System Disk Cleanup", 0)
    except Exception as e:
        cb("warn", f"System Disk Cleanup ({e})", 0)

    return 0


# ─────────────────────────────────────────────
#  Master dispatcher
# ─────────────────────────────────────────────

STEP_FUNCTIONS = {
    "user_temp":    clean_user_temp,
    "sys_temp":     clean_sys_temp,
    "win_update":   clean_win_update,
    "browser":      clean_browser,
    "sys_logs":     clean_sys_logs,
    "recycle":      clean_recycle,
    "other":        clean_other,
    "disk_cleanup": clean_disk_cleanup,
}


def run_selected(
    selected_keys: List[str],
    cb: CallbackFn,
    progress_cb: Optional[Callable[[int, int, str], None]] = None,
    dry_run: bool = False
) -> int:
    """
    Run cleanup (or scan) for the given list of item keys.
    progress_cb(current, total, key) is fired before each step.
    Returns total bytes freed.
    """
    total_freed = 0
    total = len(selected_keys)

    for i, key in enumerate(selected_keys):
        if progress_cb:
            progress_cb(i + 1, total, key)

        fn = STEP_FUNCTIONS.get(key)
        if fn:
            total_freed += fn(cb, dry_run=dry_run)

    return total_freed
