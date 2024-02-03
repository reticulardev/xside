#!/usr/bin/env python3
import math
import os
import platform
import sys

from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.platform import environment

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class Settings(object):
    """..."""
    def __init__(self, platform_integration: bool = True):
        """..."""
        self.__platform_integration = platform_integration

        # unknown linux bsd mac windows
        self.__operational_system = self.__get_operational_system()

        # unknown plasma gnome cinnamon xfce mac
        # windows-7 windows-10 windows-11
        self.__desktop_environment = self.__get_desktop_environment()

        self.__env_settings = self.__get_env_settings()

    @staticmethod
    def is_dark_widget(widget: QtWidgets) -> bool:
        """..."""
        color = widget.palette().color(QtGui.QPalette.Window)
        r, g, b = (color.red(), color.green(), color.blue())
        hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
        return False if hsp > 127.5 else True

    @staticmethod
    def is_dark_rgb_color(rgb: tuple) -> bool:
        """..."""
        r, g, b = rgb
        hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
        return False if hsp > 127.5 else True

    @staticmethod
    def is_dark_hexa_color(hexa: str) -> bool:
        """..."""
        r, g, b = tuple(int(hexa.lstrip('#')[x:x + 2], 16) for x in (0, 2, 4))
        hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
        return False if hsp > 127.5 else True

    @property
    def desktop_environment(self) -> str:
        """..."""
        return self.__desktop_environment

    @property
    def gui_env(self) -> environment.EnvSettings:
        """..."""
        return self.__env_settings

    @property
    def operational_system(self) -> str:
        """..."""
        return self.__operational_system

    @staticmethod
    def variant_icon_theme() -> tuple:
        # ...
        variant = 'dark'
        if 'dark' in QtGui.QIcon.theme_name().lower():
            variant = 'light'

        theme_name = QtGui.QIcon.theme_name()
        variant_theme_name = None
        variant_theme_path = None

        for path_dirs in QtGui.QIcon.theme_search_paths():
            if os.path.isdir(path_dirs):
                for dire in os.listdir(path_dirs):

                    if variant == 'dark':
                        if theme_name in dire and 'dark' in dire.lower():
                            variant_theme_name = dire
                            variant_theme_path = os.path.join(path_dirs, dire)
                    else:
                        name = theme_name.replace(
                            '-Dark', '').replace('-dark', '').replace(
                            '-DARK', '').replace('Dark', '').replace(
                            'dark', '').replace('DARK', '')
                        if 'dark' not in dire.lower() and name in dire:
                            variant_theme_name = dire
                            variant_theme_path = os.path.join(path_dirs, dire)

        return variant_theme_name, variant_theme_path

    def __get_desktop_environment(self) -> str:
        # ...
        if self.__platform_integration:
            if self.__operational_system == 'linux':
                if (os.environ['DESKTOP_SESSION'] == 'plasma' or
                        os.environ['XDG_SESSION_DESKTOP'] == 'KDE' or
                        os.environ['XDG_CURRENT_DESKTOP'] == 'KDE'):
                    return 'plasma'

                # TODO: Gnome, Cinnamon, XFCE
                return 'gnome'

            elif self.__operational_system == 'windows':
                if platform.release() == '10':
                    return 'windows-10'

                elif platform.release() == '11':
                    return 'windows-11'

                return 'windows-7'

            elif self.__operational_system == 'mac':
                return 'mac'

            elif self.__operational_system == 'bsd':
                return 'bsd'

        return 'unknown'

    def __get_env_settings(self) -> environment.EnvSettings | None:
        """..."""
        if self.__platform_integration:
            if self.__operational_system == 'linux':

                if self.__desktop_environment == 'plasma':
                    return environment.EnvSettingsPlasma()

                if self.__desktop_environment == 'cinnamon':
                    return environment.EnvSettingsCinnamon()

                if self.__desktop_environment == 'xfce':
                    return environment.EnvSettingsXFCE()

                return environment.EnvSettingsGnome()

            if self.__operational_system == 'mac':
                return environment.EnvSettingsMac()

            if self.__operational_system == 'windows':

                if self.__desktop_environment == 'windows-7':
                    return environment.EnvSettingsWindows7()

                if self.__desktop_environment == 'windows-10':
                    return environment.EnvSettingsWindows10()
                
                return environment.EnvSettingsWindows11()

        return environment.EnvSettings()

    @staticmethod
    def __get_operational_system() -> str:
        # 'unknown', 'linux', 'bsd', 'mac', 'windows'

        # Win config path: $HOME + AppData\Roaming\
        # Linux config path: $HOME + .config
        if os.name == 'posix':
            if platform.system() == 'Linux':
                return 'linux'

            elif platform.system() == 'Darwin':
                return 'mac'

        elif os.name == 'nt' and platform.system() == 'Windows':
            return 'windows'


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
