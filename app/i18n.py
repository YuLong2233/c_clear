# -*- coding: utf-8 -*-
"""
Internationalization (i18n) module.
Supports Simplified Chinese (zh) and English (en).
"""

LANGUAGES = {
    "zh": {
        # Window
        "title": "C盘深度清理工具",
        "subtitle": "Windows C Drive Deep Cleaner v2.0",

        # Disk Info
        "disk_section": "磁盘状态",
        "disk_label": "C盘空间",
        "disk_free": "可用",
        "disk_used": "已用",
        "disk_total": "总计",

        # Cleanup Items
        "items_section": "清理项目",
        "item_user_temp": "用户临时文件",
        "item_sys_temp": "系统临时文件",
        "item_win_update": "Windows 更新缓存",
        "item_browser": "浏览器缓存",
        "item_sys_logs": "系统日志",
        "item_recycle": "回收站",
        "item_other": "其他缓存",
        "item_disk_cleanup": "系统磁盘清理",

        # Item descriptions
        "desc_user_temp": "%TEMP% 及本地临时目录",
        "desc_sys_temp": "Windows Temp + Prefetch",
        "desc_win_update": "SoftwareDistribution 下载目录",
        "desc_browser": "Chrome / Edge / Firefox 缓存",
        "desc_sys_logs": "CBS / DISM / IIS 日志（30天以上）",
        "desc_recycle": "清空所有驱动器回收站",
        "desc_other": "错误报告 / DirectX 着色器 / npm / pip",
        "desc_disk_cleanup": "调用系统 cleanmgr.exe",

        # Log Section
        "log_section": "运行日志",
        "log_waiting": "就绪，点击「扫描」或「开始清理」...",
        "log_scanning": "正在扫描...",
        "log_cleaning": "正在清理...",
        "log_done": "✅ 清理完成！",
        "log_scan_done": "✅ 扫描完成！",
        "log_freed_prefix": "释放",
        "log_already_clean": "已干净",
        "log_not_found": "路径不存在",
        "log_in_use": "部分文件占用中",
        "log_running_bg": "已在后台运行",

        # Status Bar
        "status_freed": "累计释放",
        "status_elapsed": "耗时",
        "status_before": "清理前",
        "status_after": "清理后",
        "status_ready": "就绪",
        "status_admin": "管理员模式",
        "status_no_admin": "⚠ 非管理员（部分功能受限）",

        # Buttons
        "btn_scan": "🔍  扫  描",
        "btn_clean": "🧹  开始清理",
        "btn_stop": "⏹  停  止",

        # Dialog
        "confirm_title": "确认清理",
        "confirm_msg": "将清理已选中的 {n} 个项目，是否继续？\n\n此操作不可撤销，请确认已选择正确的清理项目。",
        "confirm_yes": "确认清理",
        "confirm_no": "取消",
        "admin_title": "需要管理员权限",
        "admin_msg": "部分清理项目需要管理员权限。\n请以管理员身份重新运行此程序。",
        "error_title": "错误",

        # Progress
        "progress_step": "步骤 {current} / {total}",
        "cleaning_item": "正在清理：{item}",
        "scanning_item": "正在扫描：{item}",

        # Links
        "link_github": "🐱 GitHub",
        "link_more": "🌐 更多软件",
    },

    "en": {
        # Window
        "title": "C Drive Deep Cleaner",
        "subtitle": "Windows C Drive Deep Cleaner v2.0",

        # Disk Info
        "disk_section": "Disk Status",
        "disk_label": "C: Drive",
        "disk_free": "Free",
        "disk_used": "Used",
        "disk_total": "Total",

        # Cleanup Items
        "items_section": "Cleanup Items",
        "item_user_temp": "User Temp Files",
        "item_sys_temp": "System Temp Files",
        "item_win_update": "Windows Update Cache",
        "item_browser": "Browser Cache",
        "item_sys_logs": "System Logs",
        "item_recycle": "Recycle Bin",
        "item_other": "Other Caches",
        "item_disk_cleanup": "System Disk Cleanup",

        # Item descriptions
        "desc_user_temp": "%TEMP% and local temp dirs",
        "desc_sys_temp": "Windows Temp + Prefetch",
        "desc_win_update": "SoftwareDistribution download dir",
        "desc_browser": "Chrome / Edge / Firefox cache",
        "desc_sys_logs": "CBS / DISM / IIS logs (30+ days)",
        "desc_recycle": "Empty recycle bins on all drives",
        "desc_other": "Error reports / DirectX / npm / pip cache",
        "desc_disk_cleanup": "Run system cleanmgr.exe",

        # Log Section
        "log_section": "Activity Log",
        "log_waiting": "Ready. Click 'Scan' or 'Start Cleanup'...",
        "log_scanning": "Scanning...",
        "log_cleaning": "Cleaning...",
        "log_done": "✅ Cleanup complete!",
        "log_scan_done": "✅ Scan complete!",
        "log_freed_prefix": "Freed",
        "log_already_clean": "Already clean",
        "log_not_found": "Path not found",
        "log_in_use": "Some files in use",
        "log_running_bg": "Running in background",

        # Status Bar
        "status_freed": "Total Freed",
        "status_elapsed": "Elapsed",
        "status_before": "Before",
        "status_after": "After",
        "status_ready": "Ready",
        "status_admin": "Administrator",
        "status_no_admin": "⚠ Not Admin (limited)",

        # Buttons
        "btn_scan": "🔍  Scan",
        "btn_clean": "🧹  Start Cleanup",
        "btn_stop": "⏹  Stop",

        # Dialog
        "confirm_title": "Confirm Cleanup",
        "confirm_msg": "Will clean {n} selected item(s). Continue?\n\nThis action cannot be undone. Please verify your selection.",
        "confirm_yes": "Confirm",
        "confirm_no": "Cancel",
        "admin_title": "Administrator Required",
        "admin_msg": "Some cleanup tasks require administrator privileges.\nPlease re-run this program as Administrator.",
        "error_title": "Error",

        # Progress
        "progress_step": "Step {current} of {total}",
        "cleaning_item": "Cleaning: {item}",
        "scanning_item": "Scanning: {item}",

        # Links
        "link_github": "🐱 GitHub",
        "link_more": "🌐 More Apps",
    }
}

# Default language
DEFAULT_LANG = "zh"


class I18n:
    """Simple internationalization helper."""

    def __init__(self, lang: str = DEFAULT_LANG):
        self._lang = lang if lang in LANGUAGES else DEFAULT_LANG

    @property
    def lang(self) -> str:
        return self._lang

    def set_lang(self, lang: str):
        if lang in LANGUAGES:
            self._lang = lang

    def t(self, key: str, **kwargs) -> str:
        """Translate a key, with optional format arguments."""
        text = LANGUAGES[self._lang].get(key, f"[{key}]")
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    def toggle(self):
        """Toggle between zh and en."""
        self._lang = "en" if self._lang == "zh" else "zh"
