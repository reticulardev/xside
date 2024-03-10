#!/usr/bin/env python3
import logging
import os
import pathlib
import re
import sys

from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case

import xside.modules.color as color
import xside.modules.env as env


class StyleParser(object):
    """..."""
    def __init__(self, style_sheet: str) -> None:
        """..."""
        self.__stylesheet_arg = style_sheet
        self.__scopes = self.__split_widgets_scops()
        self.__stylesheet = None

    def scopes(self) -> dict:
        """..."""
        return self.__scopes

    def set_style_sheet(self, style_sheet: str) -> None:
        """..."""
        self.__stylesheet_arg = style_sheet
        self.__scopes = self.__split_widgets_scops()
        self.__stylesheet = None

    def style_sheet(self, update: bool = False) -> str:
        """..."""
        if not self.__stylesheet or update:
            self.__stylesheet = ''
            for scope_key, scope_value in self.__scopes.items():
                self.__stylesheet += scope_key + ' {' + scope_value + '} '
        return self.__stylesheet

    def widget_scope(
            self, widget_class_name: str, propertie: str = None) -> str:
        """..."""
        for scope_key, scope_value in self.__scopes.items():
            if not propertie:
                if widget_class_name == scope_key:
                    return scope_value
            else:
                if widget_class_name in scope_key and propertie in scope_key:
                    return scope_value
        return ''

    def __split_widgets_scops(self) -> dict:
        # ...
        cleanstyle = re.sub(r'(/\*.+\*/)|(^#.+$)', r'', self.__stylesheet_arg)

        scopes = {}
        all_scopes = cleanstyle.replace('\n', '').replace('  ', ' ').split('}')
        for scope in all_scopes:
            if '{' in scope:
                scope_keys, scope_value = scope.split('{')

                for scope_key in scope_keys.split(','):
                    scope_key = self.__clean_key(scope_key)
                    if scope_key and scope_key in scopes:
                        scope_value = self.__join_duplicate_values(
                            scope_value, scopes[scope_key])

                    scopes[scope_key] = self.__clean_value(scope_value)
        return scopes

    def __join_duplicate_values(self, new_value: str, old: str) -> str:
        # ...
        new_values = [self.__clean_value(x) for x in new_value.split(';') if x]
        old_values = [self.__clean_value(x) for x in old.split(';') if x]
        new_keys = [self.__clean_key(self.__clean_value(x).split(':')[0])
                    for x in new_value.split(';') if x]

        for old_value in old_values:
            old_key = self.__clean_key(old_value.split(':')[0])
            if old_key not in new_keys:
                new_values.insert(0, old_value)

        return ' '.join(new_values)

    @staticmethod
    def __clean_value(value: str) -> str:
        # ...
        return value.strip().strip(';').strip().replace(',', ', ').replace(
            ' ;', ';').replace(';', '; ').replace('  ', ' ').strip().replace(
            ';;', ';') + ';'

    @staticmethod
    def __clean_key(value: str) -> str:
        # ...
        return value.lstrip('#').replace(' ', '').strip()

    def __str__(self) -> str:
        return 'StyleParser'

    def __repr__(self) -> str:
        return 'StyleParser(object)'


class Style(object):
    """..."""
    def __init__(self, toplevel: QtWidgets.QMainWindow) -> None:
        """..."""
        self.__toplevel = toplevel

        self.__env = env.Env(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment(),
            self.__toplevel.follow_platform())

    def build_style(self) -> str:
        return self.__env.settings('style').style_sheet()

    @staticmethod
    def fullscreen_adapted_style(style: str) -> str:
        # ...
        styleparser = StyleParser(style)
        return style + (
            'MainWindow {'
            f'{styleparser.widget_scope("MainWindow")}'
            'border-radius: 0px;'
            'border: 0px;}')

# def build_style_bkp(self) -> str:
#     """..."""
#     win_bg_color = self.__env.settings().window_background_color()
#     win_bd_radius = self.__env.settings().window_border_radius()
#     win_bd_color = self.__env.settings().window_border_color()
#     win_margin = self.__env.settings().window_margin()
#
#     att = hasattr(self.__toplevel, 'is_server_side_decorated')
#     if att and self.__toplevel.is_server_side_decorated():
#         style_sheet = (
#             'MainWindow {'
#             'background-color: rgba('
#             f'{win_bg_color.red()},'
#             f'{win_bg_color.green()},'
#             f'{win_bg_color.blue()},'
#             f'{win_bg_color.alpha_f()});'
#             '}')
#     else:
#         style_sheet = (
#             'MainWindow {'
#             'background-color: rgba('
#             f'{win_bg_color.red()},'
#             f'{win_bg_color.green()},'
#             f'{win_bg_color.blue()},'
#             f'{win_bg_color.alpha_f()});'
#             f'border: {self.__env.settings().window_border()}px solid'
#             ' rgba('
#             f'{win_bd_color.red()},'
#             f'{win_bd_color.green()},'
#             f'{win_bd_color.blue()},'
#             f'{win_bd_color.alpha()});'
#             f'border-top-left-radius: {win_bd_radius[0]};'
#             f'border-top-right-radius: {win_bd_radius[1]};'
#             f'border-bottom-right-radius: {win_bd_radius[2]};'
#             f'border-bottom-left-radius: {win_bd_radius[3]};'
#             'margin: '
#             f' {win_margin[0]}px'
#             f' {win_margin[1]}px'
#             f' {win_margin[2]}px'
#             f' {win_margin[3]}px;'
#             '}')
#
#     cmenu_margin = self.__env.settings().contextmenu_margin()
#     cmenu_padding = self.__env.settings().contextmenu_padding()
#     cmenu_bg_color = self.__env.settings().contextmenu_background_color()
#     cmenu_bd_color = self.__env.settings().contextmenu_border_color()
#     cmenu_bd_radius = self.__env.settings().contextmenu_border_radius()
#     style_sheet += (
#         'ContextMenu {'
#         'margin:'
#         f' {cmenu_margin[0]}px'
#         f' {cmenu_margin[1]}px'
#         f' {cmenu_margin[2]}px'
#         f' {cmenu_margin[3]}px;'
#         'padding:'
#         f' {cmenu_padding[0]}px'
#         f' {cmenu_padding[1]}px'
#         f' {cmenu_padding[2]}px'
#         f' {cmenu_padding[3]}px;'
#         'background-color: rgba('
#         f' {cmenu_bg_color.red()},'
#         f' {cmenu_bg_color.green()},'
#         f' {cmenu_bg_color.blue()},'
#         f' {cmenu_bg_color.alpha()});'
#         'border: 1px solid rgba('
#         f' {cmenu_bd_color.red()},'
#         f' {cmenu_bd_color.green()},'
#         f' {cmenu_bd_color.blue()},'
#         f' {cmenu_bd_color.alpha_f()});'
#         f'border-radius: {cmenu_bd_radius}px;'
#         '}')
#
#     cmenusep_margin = self.__env.settings().contextmenu_separator_margin()
#     cmenusep_color = self.__env.settings().contextmenu_separator_color()
#     style_sheet += (
#         'ContextMenuSeparator {'
#         'margin:'
#         f' {cmenusep_margin[0]}px'
#         f' {cmenusep_margin[1]}px'
#         f' {cmenusep_margin[2]}px'
#         f' {cmenusep_margin[3]}px;'
#         '}'
#         'ContextMenuSeparatorLine {'
#         'color: rgba('
#         f' {cmenusep_color.red()},'
#         f' {cmenusep_color.green()},'
#         f' {cmenusep_color.blue()},'
#         f' {cmenusep_color.alpha()});'
#         '}')
#
#     cmenubtn_bdr = self.__env.settings().contextmenubutton_border_radius()
#     cmenubtn_pd = self.__env.settings().contextmenubutton_padding()
#     cmenubtn_bg_hover_color = self.__env.settings(
#         ).contextmenubutton_background_hover_color()
#     cmenubtn_bd_hover_color = self.__env.settings(
#         ).contextmenubutton_border_hover_color()
#     cmenubtn_lbl_hover_color = self.__env.settings(
#         ).contextmenubutton_label_hover_color()
#     style_sheet += (
#         'ContextMenuButton {'
#         'background: transparent;'
#         'padding:'
#         f' {cmenubtn_pd[0]}px'
#         f' {cmenubtn_pd[1]}px'
#         f' {cmenubtn_pd[2]}px'
#         f' {cmenubtn_pd[3]}px;'
#         'border: 1px solid rgba(0, 0, 0, 0.0);'
#         f'border-radius: {cmenubtn_bdr}px;'
#         '}'
#         'ContextMenuButton:hover {'
#         'color: rgba('
#         f' {cmenubtn_lbl_hover_color.red()},'
#         f' {cmenubtn_lbl_hover_color.green()},'
#         f' {cmenubtn_lbl_hover_color.blue()},'
#         f' {cmenubtn_lbl_hover_color.alpha()});'
#         'background-color: rgba('
#         f' {cmenubtn_bg_hover_color.red()},'
#         f' {cmenubtn_bg_hover_color.green()},'
#         f' {cmenubtn_bg_hover_color.blue()},'
#         f' {cmenubtn_bg_hover_color.alpha()});'
#         'border: 1px solid rgba('
#         f' {cmenubtn_bd_hover_color.red()},'
#         f' {cmenubtn_bd_hover_color.green()},'
#         f' {cmenubtn_bd_hover_color.blue()},'
#         f' {cmenubtn_bd_hover_color.alpha()});'
#         '}'
#         'ContextMenuButtonLabel:hover {'
#         'color: rgba('
#         f' {cmenubtn_lbl_hover_color.red()},'
#         f' {cmenubtn_lbl_hover_color.green()},'
#         f' {cmenubtn_lbl_hover_color.blue()},'
#         f' {cmenubtn_lbl_hover_color.alpha()});'
#         '}')
#
#     lbl_ctx_color = self.__env.settings().label_context_color()
#     style_sheet += (
#         'ContextLabel {'
#         'color: rgba('
#         f' {lbl_ctx_color.red()},'
#         f' {lbl_ctx_color.green()},'
#         f' {lbl_ctx_color.blue()},'
#         f' {lbl_ctx_color.alpha()});'
#         '}')
#
#     contextmenugroup_pd = self.__env.settings().contextmenugroup_padding()
#     style_sheet += (
#         'ContextMenuGroup {'
#         'padding:'
#         f' {contextmenugroup_pd[0]}px'
#         f' {contextmenugroup_pd[1]}px'
#         f' {contextmenugroup_pd[2]}px'
#         f' {contextmenugroup_pd[3]}px;'
#         '}')
#
#     controlbutton_margin = self.__env.settings().controlbuttons_margin()
#     style_sheet += (
#         'ControlButtons {'
#         f'margin:'
#         f' {controlbutton_margin[0]}px'
#         f' {controlbutton_margin[1]}px'
#         f' {controlbutton_margin[2]}px'
#         f' {controlbutton_margin[3]}px;'
#         '}')
#
#     headerbar_margin = self.__env.settings().headerbar_margin()
#     style_sheet += (
#         'HeaderBar {'
#         f'margin:'
#         f' {headerbar_margin[0]}px'
#         f' {headerbar_margin[1]}px'
#         f' {headerbar_margin[2]}px'
#         f' {headerbar_margin[3]}px;'
#         '}')
#
#     win_icon_margin = self.__env.settings().window_icon_margin()
#     style_sheet += (
#         'WindowIcon {'
#         f'margin:'
#         f' {win_icon_margin[0]}px'
#         f' {win_icon_margin[1]}px'
#         f' {win_icon_margin[2]}px'
#         f' {win_icon_margin[3]}px;'
#         '}')
#
#     with open(os.path.join(
#             pathlib.Path(__file__).resolve().parent,
#             'static', 'style.qss'), 'r') as style_qss_file:
#         file_style = style_qss_file.read()
#
#     return style_sheet + file_style
