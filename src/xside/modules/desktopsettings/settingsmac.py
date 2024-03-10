#!/usr/bin/env python3
from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopsettings.settingsbase as settingsbase
import xside.modules.cli as cli


class EnvSettingsMac(settingsbase.EnvSettings):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

