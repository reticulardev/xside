#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.color as color


class EnvSettings(object):
    """Base environment settings"""

    def __init__(self):
        """..."""
        self.palette = QtGui.QPalette()

    @staticmethod
    def is_using_global_menu():
        """..."""
        return False

    @staticmethod
    def control_button_style(*args, **kwargs) -> str:
        logging.info(args)
        logging.info(kwargs)
        """..."""
        return (
            'ControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  padding: 1px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(200, 200, 200, 0.2);'
            '}')

    @staticmethod
    def control_buttons_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (2, 1, 0), (3,)

    @staticmethod
    def icon_theme_name() -> str:
        """..."""
        return 'hicolor'

    def accent_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)
