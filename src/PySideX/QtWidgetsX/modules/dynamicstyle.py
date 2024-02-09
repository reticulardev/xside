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
        """..."""
        self.__toplevel = toplevel

        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment(),
            self.__toplevel.follow_platform())

        self.__border_radius = self.__gui_env.settings(
            ).window_border_radius()
        self.__background_color = self.__gui_env.settings(
            ).window_background_color()
        self.__is_dark = color.is_dark(
            color.qcolor_to_rgba(self.__background_color))
        self.__border_color = self.__gui_env.settings(
            ).window_border_color()
        self.__selection_color = self.__gui_env.settings(
            ).contextmenubutton_bg_hover_color()
        self.__selection_alpha = self.__gui_env.settings(
            ).contextmenubutton_bg_hover_alpha()
        self.__ctxmenubutton_bd_color = self.__gui_env.settings(
            ).contextmenu_border_color()
        self.__ctxmenu_bd_radius = self.__gui_env.settings(
            ).contextmenu_border_radius()
        self.__ctxmenubutton_padding = self.__gui_env.settings(
            ).contextmenubutton_padding()
        self.__ctxmenubutton_bd_radius = (
            self.__ctxmenu_bd_radius - 4 if self.__ctxmenu_bd_radius > 4 else
            self.__ctxmenu_bd_radius)

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
            f'{self.__gui_env.settings().contextmenu_bg_alpha()});'
            'border: 1px solid rgba('
            f'{self.__ctxmenubutton_bd_color.red()},'
            f'{self.__ctxmenubutton_bd_color.green()},'
            f'{self.__ctxmenubutton_bd_color.blue()},'
            f'{self.__ctxmenubutton_bd_color.alpha_f()});'
            f'border-radius: {self.__ctxmenu_bd_radius}px;'
            '}'
            'QQuickContextMenuButton {'
            'background: transparent;'
            'padding:'
            f' {self.__ctxmenubutton_padding[0]}px'
            f' {self.__ctxmenubutton_padding[1]}px'
            f' {self.__ctxmenubutton_padding[2]}px'
            f' {self.__ctxmenubutton_padding[3]}px;'
            'border: 1px solid rgba(0, 0, 0, 0.0);'
            f'border-radius: {self.__ctxmenubutton_bd_radius}px;'
            '}'
            'QQuickContextMenuButton:hover {'
            'background-color: rgba('
            f'{self.__selection_color.red()},'
            f'{self.__selection_color.green()},'
            f'{self.__selection_color.blue()},'
            f'{self.__selection_alpha});'
            'border: 1px solid rgba('
            f'{self.__selection_color.red()},'
            f'{self.__selection_color.green()},'
            f'{self.__selection_color.blue()}, 0.9);'
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
