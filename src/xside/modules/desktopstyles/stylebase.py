#!/usr/bin/env python3
import logging

from PySide6 import QtGui
from __feature__ import snake_case

import xside.modules.color as color


class EnvStyle(object):
    """Base environment settings"""

    def __init__(self):
        """..."""
        self.palette = QtGui.QPalette()
        self.accent_color = self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)

        self.__style_sheet = {
            'ContextLabel':
                self.context_label(),
            'ContextMenu':
                self.contex_menu(),
            'ContextMenuButton':
                self.contex_menu_button(),
            'ContextMenuButton:hover':
                self.contex_menu_button_hover(),
            'ContextMenuButtonLabel:hover':
                self.context_menu_button_label_hover(),
            'ContextMenuGroup':
                self.context_menu_group(),
            'ContextMenuSeparator':
                self.contex_menu_separator(),
            'ControlButtons':
                self.control_buttons(),
            'HeaderBar':
                self.header_bar(),
            'MainWindow':
                self.main_window(),
            'WindowIcon':
                self.window_icon(),
        }

    def style_sheet(self) -> str:
        style_sheet = ''
        for widget_name, widget_styles in self.__style_sheet.items():
            scope = widget_name + ' {'
            for propertie_name, propertie_value in widget_styles.items():
                kv = f'{propertie_name}: {propertie_value}; '
                scope += kv

            style_sheet += scope.strip() + '} '
        return style_sheet.strip()

    def context_label(self) -> dict:
        """..."""
        r, g, b, a = self.palette.color(
            QtGui.QPalette.Disabled, QtGui.QPalette.WindowText).to_tuple()
        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
        }

    def contex_menu(self) -> dict:
        """..."""
        return {
            'background-color': self.main_window()['background-color'],
            'border': self.main_window()['border'],
            'border-radius': f'{self.main_window()["border-radius"]}',
            'margin': '0px 0px 0px 0px',
            'padding': '4px 4px 4px 4px',
            'spacing': '0px',
        }

    def contex_menu_button(self) -> dict:
        """..."""
        r = self.contex_menu()['border-radius'].split('px')[0]
        r = int(r) - 4 if int(r) > 6 else r
        return {
            'border-radius': f'{r}px',
            'padding': '4px 6px 4px 6px',
        }

    def contex_menu_button_hover(self) -> dict:
        """..."""
        r, g, b, a = self.accent_color.to_tuple()
        return {
            'background-color': f'rgba({r}, {g}, {b}, {a})',
        }

    def context_menu_button_label_hover(self) -> dict:
        """..."""
        r, g, b, a = self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.WindowText).to_tuple()
        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
        }

    @staticmethod
    def context_menu_group() -> dict:
        """..."""
        return {
            'padding': '0px 6px 0px 8px',
        }

    def contex_menu_separator(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        step_tone = 15 if color.is_dark(bg_color) else 30
        r, g, b, a = color.lighten_rgba(bg_color, step_tone)

        return {
            'color': f'rgba({r}, {g}, {b}, {a})',
            'margin': '0px 4px 0px 4px',
        }

    @staticmethod
    def control_buttons() -> dict:
        """..."""
        return {
            'margin': '2px 0px 2px 0px',
            'spacing': '6px',
        }

    @staticmethod
    def header_bar() -> dict:
        """..."""
        return {
            'margin': '4px 4px 4px 4px',
        }

    def main_window(self) -> dict:
        """..."""
        bg_color = self.palette.color(QtGui.QPalette.Window).to_tuple()
        bg_r, bg_g, bg_b, bg_a = bg_color

        step_tone = 15 if color.is_dark(bg_color) else 30
        bd_r, bd_g, bd_b, bd_a = color.lighten_rgba(bg_color, step_tone)

        return {
            'background-color': f'rgba({bg_r}, {bg_g}, {bg_b}, {bg_a})',
            'border': f'1px solid rgba({bd_r}, {bd_g}, {bd_b}, {bd_a})',
            'border-radius': '5px',
            'margin': '0px 0px 0px 0px',
        }

    @staticmethod
    def window_icon() -> dict:
        """..."""
        return {
            'margin': '1px 0px 1px 0px',
        }
