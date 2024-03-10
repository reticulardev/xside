#!/usr/bin/env python3
import logging
import os
import pathlib
import sys

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopsettings.settingsbase as settingsbase
import xside.modules.cli as cli


class EnvSettingsXFCE(settingsbase.EnvSettings):
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
            '  border-radius: 3px;'
            '  margin: 0px;'
            '  padding: 1px;'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '}')

    @staticmethod
    def control_buttons_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (3,), (0, 1, 2)

