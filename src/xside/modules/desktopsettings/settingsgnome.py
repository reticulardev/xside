#!/usr/bin/env python3
import logging
import os
import pathlib
import sys

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopsettings.settingsbase as settingsbase
import xside.modules.cli as cli


class EnvSettingsGnome(settingsbase.EnvSettings):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def control_button_style(*args, **kwargs) -> str:
        """..."""
        logging.info(args)
        logging.info(kwargs)
        return (
            'ControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 5px 4px 5px 4px;'
            '  padding: 2px 1px 1px 2px;'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')

    @staticmethod
    def control_buttons_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        button_layout = cli.output_by_args(
            ["gsettings", "get", "org.gnome.desktop.wm.preferences",
             "button-layout"]).split(':')

        if not button_layout:
            return (3,), (0, 1, 2)

        d = {'close': 2, 'maximize': 1, 'minimize': 0}
        left = []
        for x in button_layout[0].split(','):
            if x in d:
                left.append(d[x])
            else:
                left.append(3)

        right = []
        for x in button_layout[1].split(','):
            if x in d:
                right.append(d[x])
            else:
                right.append(3)

        return tuple(left), tuple(right)

    def icon_theme_name(self) -> str | None:
        """..."""
        icon_theme = self.cli.output_by_args(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'icon-theme'])
        return icon_theme if icon_theme else None
