# -*- coding: utf-8 -*-
"""
Main entry point for the C Drive Cleaner application.
Handles admin relaunch and initializes the UI.
"""

import sys
from utils import is_admin, run_as_admin
from ui import CleanerApp


def main():
    # If not admin, you could choose to force relaunch.
    # But let's allow non-admin run with limited features for now,
    # or just show a warning in the UI (which we already do).
    # We are now forcing admin for better cleaner functionality.
    if not is_admin():
         run_as_admin()

    app = CleanerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
