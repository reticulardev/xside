#!/usr/bin/env python3
import logging
import os
import pathlib
import sys

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopsettings.settingsxfce as settingsxfce
import xside.modules.cli as cli


class EnvSettingsMate(settingsxfce.EnvSettingsXFCE):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def control_button_style(*args, **kwargs) -> str:
        logging.info(args)
        logging.info(kwargs)

        """..."""
        return (
            'ControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 3px 4px 3px 4px;'
            '  padding: 1px 0px 0px 1px;'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')
