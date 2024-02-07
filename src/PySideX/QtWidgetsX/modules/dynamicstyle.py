#!/usr/bin/env python3
import os
import sys

from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case

import PySideX.QtWidgetsX.modules.color as color
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv

SRC_DIR = os.path.dirname(os.path.abspath(__file__))


class DynamicStyle(object):
    """..."""
    def __init__(self, toplevel: QtWidgets.QMainWindow) -> None:
        """...self.__gui_env.settings().control_button_style("""
        # Param
        self.__toplevel = toplevel

        # Settings
        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment(),
            self.__toplevel.follow_platform())

        # Properties
        self.__border_radius = self.__gui_env.settings().window_border_radius()
        self.__border_color = self.__toplevel.color_by_state_name(
            'window-border')
        self.__background_color = self.__toplevel.color_by_state_name(
            'window-background')
        self.__is_dark = color.is_dark((
            self.__background_color.red(),
            self.__background_color.green(),
            self.__background_color.blue()))
        self.__selection_color = self.__gui_env.settings().color_of_selection(
            self.__is_dark)
        self.__selection_alpha = self.__gui_env.settings(
            ).contextmenu_selection_alpha_color_value()

    def build_style(self) -> str:
        """..."""
        if self.__toplevel.is_server_side_decorated():
            window_style = (
                '#QApplicationWindow {'
                'background-color: rgba('
                f'{self.__background_color.red()},'
                f'{self.__background_color.green()},'
                f'{self.__background_color.blue()},'
                f'{self.__background_color.alpha_f()});'
                '}')
        else:
            window_style = (
                '#QApplicationWindow {'
                'background-color: rgba('
                f'{self.__background_color.red()},'
                f'{self.__background_color.green()},'
                f'{self.__background_color.blue()},'
                f'{self.__background_color.alpha_f()});'
                'border: 1px solid rgba('
                f'{self.__border_color.red()},'
                f'{self.__border_color.green()},'
                f'{self.__border_color.blue()},'
                f'{self.__border_color.alpha_f()});'
                f'border-top-left-radius: {self.__border_radius[0]};'
                f'border-top-right-radius: {self.__border_radius[1]};'
                f'border-bottom-right-radius: {self.__border_radius[2]};'
                f'border-bottom-left-radius: {self.__border_radius[3]};'
                '}')

        context_menu_style = (
            '#QQuickContextMenu {'
            'background-color: rgba('
            f'{self.__background_color.red()},'
            f'{self.__background_color.green()},'
            f'{self.__background_color.blue()},'
            f'{self.__gui_env.settings().contextmenu_alpha_color_value()});'
            'border: 1px solid rgba('
            f'{self.__border_color.red()},'
            f'{self.__border_color.green()},'
            f'{self.__border_color.blue()},'
            f'{self.__border_color.alpha_f()});'
            f'border-radius: {self.__border_radius[0]}px;'
            '}'
            'QQuickContextMenuButton {'
            'background: transparent;'
            'padding: 2px;'
            'border: 1px solid rgba(0, 0, 0, 0.0);'
            'border-radius: 3px;'
            '}'
            'QQuickContextMenuButton:hover {'
            'background-color: rgba('
            f'{self.__selection_color.red()}, '
            f'{self.__selection_color.green()}, '
            f'{self.__selection_color.blue()},'
            f'{self.__selection_alpha});'
            'padding: 2px;'
            'border: 1px solid rgba('
            f'{self.__selection_color.red()}, '
            f'{self.__selection_color.green()}, '
            f'{self.__selection_color.blue()}, 0.9);'
            'border-radius: 3px;'
            '}')

        style_path = os.path.join(SRC_DIR, 'static', 'style.qss')
        with open(style_path, 'r') as style_qss_file:
            file_style = style_qss_file.read()

        return window_style + context_menu_style + file_style

    @staticmethod
    def fullscreen_adapted_style(style: str) -> str:
        # ...
        central_widget = [
            x for x in style.split('}') if
            x.strip().startswith(f'#QApplicationWindow')][-1]

        return style.replace(
            central_widget, central_widget + 'border-radius: 0px; border: 0px')
