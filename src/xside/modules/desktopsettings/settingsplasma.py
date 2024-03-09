#!/usr/bin/env python3
import os
import pathlib
import sys

from PySide6 import QtGui
from __feature__ import snake_case

from xside.modules.parser import DesktopFile
import xside.modules.desktopsettings.settingsbase as settingsbase


class EnvSettingsPlasma(settingsbase.EnvSettings):
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

    def is_using_global_menu(self) -> bool:
        """..."""
        group, key = '[Windows]', 'BorderlessMaximizedWindows'
        if group in self.__kwinrc and key in self.__kwinrc[group]:
            return True if self.__kwinrc[group][key] == 'true' else False

    def control_button_style(
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
            pathlib.Path(__file__).resolve().parent, 'static',
            'kde-breeze-control-buttons', button_name + '.svg')
        return (
            # f'background: url({url_icon}) top center no-repeat;'
            'ControlButton {'
            '  border: 0px;'
            '  margin: 0px;'
            '  padding: 0px;'
            f' background: url({url_icon}) center no-repeat;'
            '}')

    def control_buttons_order(self) -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
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

    def icon_theme_name(self) -> str | None:
        """..."""
        group, key = '[Icons]', 'Theme'
        if group in self.__kde_globals and key in self.__kde_globals[group]:
            return self.__kde_globals[group][key]
        return None
