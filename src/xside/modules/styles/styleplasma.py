#!/usr/bin/env python3
import os
import sys

from PySide6 import QtGui
from __feature__ import snake_case

from xside.modules.parser import DesktopFile
import xside.modules.styles.style as style

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class EnvStylePlasma(style.EnvStyle):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

        filerc = os.path.join(os.environ['HOME'], '.config', 'kwinrc')
        self.__kwinrc = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})

        filerc = os.path.join(os.environ['HOME'], '.config', 'breezerc')
        self.__breezerc = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})

        filerc = os.path.join(os.environ['HOME'], '.config', 'kdeglobals')
        self.__kde_globals = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})

    def contextmenu_background_color(self) -> QtGui.QColor:
        """..."""
        cor = self.window_background_color()
        return QtGui.QColor(cor.red(), cor.green(), cor.blue(), 225)

    @staticmethod
    def contextmenu_border_radius() -> int:
        """..."""
        return 3

    @staticmethod
    def contextmenu_padding() -> tuple:
        """..."""
        return 3, 3, 3, 3

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 3, 3, 3, 3

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        cor = self.window_accent_color()
        return QtGui.QColor(cor.red(), cor.green(), cor.blue(), 100)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_accent_color()

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 2, 6, 2, 6

    @staticmethod
    def contextmenugroup_padding() -> tuple:
        """..."""
        return 2, 6, 2, 8

    def controlbutton_order(self) -> tuple:
        """..."""
        right_buttons = 'IAX'  # X = close, A = max, I = min
        left_buttons = 'M'  # M = icon, F = above all

        kdecoration = '[org.kde.kdecoration2]'
        buttons_on_left, buttons_on_right = 'ButtonsOnLeft', 'ButtonsOnRight'
        if kdecoration in self.__kwinrc:
            if buttons_on_left in self.__kwinrc[kdecoration]:
                left_buttons = self.__kwinrc[kdecoration][buttons_on_left]

            if buttons_on_right in self.__kwinrc[kdecoration]:
                right_buttons = self.__kwinrc[kdecoration][buttons_on_right]

        d = {'X': 2, 'A': 1, 'I': 0, 'M': 3}
        return tuple(
            d[x] for x in left_buttons
            if x == 'X' or x == 'A' or x == 'I' or x == 'M'), tuple(
            d[x] for x in right_buttons
            if x == 'X' or x == 'A' or x == 'I' or x == 'M')

    def controlbutton_style(
            self, window_is_dark: bool,
            button_name: str,
            button_state: str) -> str:
        """..."""
        # window_is_dark: True or False
        # button_name: 'minimize', 'maximize', 'restore' or 'close'
        # button_state: 'normal', 'hover', 'inactive'

        if button_name == 'minimize':
            button_name = 'go-down'
        elif button_name == 'maximize':
            button_name = 'go-up'
        elif button_name == 'restore':
            button_name = 'window-restore'
        else:
            button_name = 'window-close-b'
            top, key = '[Common]', 'OutlineCloseButton'
            if (top in self.__breezerc and
                    key in self.__breezerc[top]):
                if self.__breezerc[top][key] == 'true':
                    button_name = 'window-close'

        if button_state == 'hover':
            if button_name == 'window-close-b':
                button_name = 'window-close'
            button_name += '-hover'
        if button_state == 'inactive':
            button_name += '-inactive'

        if window_is_dark:
            button_name += '-symbolic'

        url_icon = os.path.join(
            SRC_DIR, 'static',
            'kde-breeze-control-buttons', button_name + '.svg')
        return (
            # f'background: url({url_icon}) top center no-repeat;'
            'ControlButton {'
            '  border: 0px;'
            '  margin: 0px;'
            '  padding: 0px;'
            f' background: url({url_icon}) center no-repeat;'
            '}')

    def desktop_is_using_global_menu(self) -> bool:
        """..."""
        group, key = '[Windows]', 'BorderlessMaximizedWindows'
        if group in self.__kwinrc and key in self.__kwinrc[group]:
            return True if self.__kwinrc[group][key] == 'true' else False

    @staticmethod
    def headerbar_margin() -> tuple:
        """..."""
        return 3, 5, 0, 5

    def icon_theme_name(self) -> str | None:
        """..."""
        group, key = '[Icons]', 'Theme'
        if group in self.__kde_globals and key in self.__kde_globals[group]:
            return self.__kde_globals[group][key]
        return None

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 4, 4, 0, 0

    @staticmethod
    def windowcontrolbutton_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0
