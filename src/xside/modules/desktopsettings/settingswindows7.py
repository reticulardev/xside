#!/usr/bin/env python3
from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopsettings.settingswindows11 as settingswindows11


class EnvSettingsWindows7(settingswindows11.EnvSettingsWindows11):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
