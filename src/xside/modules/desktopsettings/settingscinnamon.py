#!/usr/bin/env python3
import logging
import os
import pathlib
import sys

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.desktopsettings.settingsgnome as settingsgnome
import xside.modules.color as color


class EnvSettingsCinnamon(settingsgnome.EnvSettingsGnome):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    def control_button_style(
            self, is_dark: bool, button_name: str, *args, **kwargs) -> str:
        """..."""
        logging.info(is_dark)
        logging.info(args)
        logging.info(kwargs)

        if button_name == 'close':
            url_icon = os.path.join(
                pathlib.Path(__file__).resolve().parent,
                'static', 'cinnamon-control-buttons',
                'window-close.svg')

            accent_light = color.lighten_rgba(self.accent_color.to_tuple(), 20)
            return (
                'ControlButton {'
                '  border: 0px;'
                '  border-radius: 10px;'
                f' background: url({url_icon}) center no-repeat;'
                '  background-color: rgba('
                f' {self.accent_color.red()},'
                f' {self.accent_color.green()},'
                f' {self.accent_color.blue()},'
                f' {self.accent_color.alpha_f()});'
                '  margin: 5px 2px 5px 2px;'
                '  padding: 1px 0px 0px 1px;'
                '}'
                'ControlButton:hover {'
                '  background-color: rgba('
                f' {accent_light[0]},'
                f' {accent_light[1]},'
                f' {accent_light[2]},'
                f' {accent_light[3]});'
                '}')
        return (
            'ControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 5px 2px 5px 2px;'
            '  padding: 1px 0px 0px 1px;'
            '}'
            'ControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')
