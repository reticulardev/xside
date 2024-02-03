#!/usr/bin/env python3
import math
import os
import platform
import sys

from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.platform import envsettings

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class StyleBuilder(object):
    """..."""
    def __init__(self, main_window: QtWidgets.QMainWindow) -> None:
        """..."""
        self.__main_window = main_window
        self.__src = os.path.dirname(os.path.abspath(__file__))
        self.__bd_radius = self.__main_window.platform_settings(
            ).gui_env.window_border_radius()

        self.__bg_color = self.__main_window.palette().color(
            QtGui.QPalette.Window)
        
        self.__bg_accent_color = QtGui.QColor(
            QtGui.QPalette().color(
                QtGui.QPalette.Active, QtGui.QPalette.Highlight))
        
        self.__bd_color = self.__main_window.palette().color(
            QtGui.QPalette.Window.Mid)
        # https://doc.qt.io/qtforpython-6/PySide6/QtGui/
        # QPalette.html#PySide6.QtGui.PySide6.QtGui.QPalette.ColorGroup

    def build_style(self) -> str:
        """..."""
        if self.__main_window.is_server_side_decorated():
            main_window_style = (
                '#QApplicationWindow {'
                'background-color: rgba('
                f'{self.__bg_color.red()}, {self.__bg_color.green()}, '
                f'{self.__bg_color.blue()}, {self.__bg_color.alpha_f()});'
                '}')
        else:
            main_window_style = (
                '#QApplicationWindow {'
                'background-color: rgba('
                f'{self.__bg_color.red()}, {self.__bg_color.green()}, '
                f'{self.__bg_color.blue()}, {self.__bg_color.alpha_f()});'
                'border: 1px solid rgba('
                f'{self.__bd_color.red()}, {self.__bd_color.green()}, '
                f'{self.__bd_color.blue()}, {self.__bd_color.alpha_f()});'
                f'border-top-left-radius: {self.__bd_radius[0]};'
                f'border-top-right-radius: {self.__bd_radius[1]};'
                f'border-bottom-right-radius: {self.__bd_radius[2]};'
                f'border-bottom-left-radius: {self.__bd_radius[3]};'
                '}')

        main_window_style += (
            '#QQuickContextMenu {'
            'background-color: rgba('
            f'{self.__bg_color.red()}, {self.__bg_color.green()}, '
            f'{self.__bg_color.blue()}, 0.9);'
            'border: 1px solid rgba('
            f'{self.__bd_color.red()}, {self.__bd_color.green()}, '
            f'{self.__bd_color.blue()}, {self.__bd_color.alpha_f()});'
            f'border-radius: {self.__bd_radius[0]}px;'
            '}'
            'QQuickContextMenuButton {'
            'background: transparent;'
            'padding: 2px;'
            'border: 1px solid rgba(0, 0, 0, 0.0);'
            'border-radius: 3px;'
            '}'
            'QQuickContextMenuButton:hover {'
            'background-color: rgba('
            f'{self.__bg_accent_color.red()}, '
            f'{self.__bg_accent_color.green()}, '
            f'{self.__bg_accent_color.blue()}, 0.2);'
            'padding: 2px;'
            'border: 1px solid rgba('
            f'{self.__bg_accent_color.red()}, '
            f'{self.__bg_accent_color.green()}, '
            f'{self.__bg_accent_color.blue()}, 0.9);'
            'border-radius: 3px;'
            '}')

        style_path = os.path.join(self.__src, 'static', 'style.qss')
        with open(style_path, 'r') as style_qss_file:
            style = style_qss_file.read()

        return main_window_style + style

    @staticmethod
    def adapt_to_fullscreen(style: str) -> str:
        # ...
        central_widget = [
            x for x in style.split('}') if
            x.strip().startswith(f'#QApplicationWindow')][-1]

        return style.replace(
            central_widget, central_widget + 'border-radius: 0px; border: 0px')
