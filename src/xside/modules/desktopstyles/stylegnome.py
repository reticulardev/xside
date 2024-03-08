#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopstyles.stylebase as stylebase
import xside.modules.cli as cli


class EnvStyleGnome(stylebase.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def border_radius() -> tuple:
        """..."""
        return 4, 4, 0, 0

    @staticmethod
    def contextmenu_bg_alpha() -> float:
        """..."""
        return 1.0

    @staticmethod
    def contextmenu_padding() -> tuple:
        """..."""
        return 6, 6, 6, 6

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 8, 6, 8, 6

    @staticmethod
    def contextmenubutton_bg_hover_alpha() -> float:
        """..."""
        return 1.0

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(QtGui.QPalette.AlternateBase)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.contextmenubutton_background_hover_color()

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 6, 12, 6, 12

    @staticmethod
    def contextmenugroup_padding() -> tuple:
        """..."""
        return 6, 12, 6, 14

    @staticmethod
    def controlbutton_order() -> tuple:
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

    @staticmethod
    def controlbutton_style(*args, **kwargs) -> str:
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

    def icon_theme_name(self) -> str | None:
        """..."""
        icon_theme = self.cli.output_by_args(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'icon-theme'])
        return icon_theme if icon_theme else None

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 10, 10, 10, 10

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 5, 7, 5, 7
