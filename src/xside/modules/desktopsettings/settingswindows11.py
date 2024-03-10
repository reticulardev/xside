#!/usr/bin/env python3
import logging
import os
import pathlib

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopsettings.settingsbase as settingsbase


class EnvSettingsWindows11(settingsbase.EnvSettings):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    @staticmethod
    def control_button_style(
            window_is_dark: bool,
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
            button_name = 'window-close'

        if button_state == 'hover':
            button_name += '-hover'
        if button_state == 'inactive':
            button_name += '-inactive'

        if window_is_dark:
            button_name += '-symbolic'

        url_icon = os.path.join(
            pathlib.Path(__file__).resolve().parent, 'static',
            'windows-11-control-buttons', button_name + '.svg')

        return (
            'ControlButton {'
            f'background: url("{url_icon}") center no-repeat;'
            f'width: 42px;'
            'height: 26px;'
            'border-radius: 0px;'
            'border: 0px;'
            'margin: 0px;'
            'padding: 0px;'
            '}')

    @staticmethod
    def control_buttons_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (3,), (0, 1, 2)
