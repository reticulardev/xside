#!/usr/bin/env python3
import os
import sys

import PySideX.QtWidgetsX.modules.color as color
import PySideX.QtWidgetsX.modules.styles.stylegnome as stylegnome

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class EnvStyleCinnamon(stylegnome.EnvStyleGnome):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)

    def controlbutton_style(self, button_name: str, *args, **kwargs) -> str:
        """..."""
        logging.info(args)
        logging.info(kwargs)

        if button_name == 'close':
            url_icon = os.path.join(
                SRC_DIR, 'static', 'cinnamon-control-buttons',
                'window-close.svg')

            accent = self.window_accent_color()
            accent_light = color.lighten_rgba(accent.to_tuple(), 20)
            return (
                'ControlButton {'
                '  border: 0px;'
                '  border-radius: 10px;'
                f' background: url({url_icon}) center no-repeat;'
                '  background-color: rgba('
                f' {accent.red()},'
                f' {accent.green()},'
                f' {accent.blue()},'
                f' {accent.alpha_f()});'
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
