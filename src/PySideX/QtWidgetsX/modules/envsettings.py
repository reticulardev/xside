#!/usr/bin/env python3
import os
import sys

from PySide6 import QtGui

from PySideX.QtWidgetsX.modules.parser import DesktopFile
import PySideX.QtWidgetsX.modules.cli as cli

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class EnvSettings(object):
    """Base environment settings"""

    def __init__(self):
        """..."""
        self.__disabled_text_color = QtGui.QPalette().color(
            QtGui.QPalette.Disabled, QtGui.QPalette.Text)

        self.__window_border_color = QtGui.QPalette().color(
            QtGui.QPalette.Window.Mid)

        self.__window_background_color = QtGui.QPalette().color(
            QtGui.QPalette.Window)

        self.__accent_color = QtGui.QPalette().color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)

    @staticmethod
    def context_menu_border_color(window_is_dark: bool) -> tuple:
        """RGBA tuple: (127, 127, 127, 0.8)"""
        if window_is_dark:
            return 127, 127, 127, 0.8
        return 127, 127, 127, 0.8

    @staticmethod
    def context_menu_padding() -> int:
        """..."""
        return 4

    @staticmethod
    def context_menu_separator_color_type() -> str:
        """window-border, disabled-text"""
        return 'window-border'

    @staticmethod
    def context_menu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 0, 4, 0, 4

    @staticmethod
    def context_menu_spacing() -> int:
        """..."""
        return 0

    @staticmethod
    def control_button_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (2, 1, 0), (3,)

    @staticmethod
    def control_button_style(*args, **kwargs) -> str:
        """..."""
        return (
            'QControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  padding: 1px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '}'
            'QControlButton:hover {'
            '  background-color: rgba(200, 200, 200, 0.2);'
            '}')

    @staticmethod
    def icon_theme_name() -> str:
        """..."""
        return 'hicolor'

    @staticmethod
    def rc_file_content(file_url: str) -> dict:
        """..."""
        if os.path.isfile(file_url):
            return DesktopFile(url=file_url).content
        return {}

    def use_global_menu(self) -> bool:
        """..."""
        return False

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 5, 5, 5, 5

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 0, 1, 0, 1


class EnvSettingsPlasma(EnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()

        self.__kwinrc = self.rc_file_content(
            os.path.join(os.environ['HOME'], '.config', 'kwinrc'))
        self.__breezerc = self.rc_file_content(
            os.path.join(os.environ['HOME'], '.config', 'breezerc'))
        self.__kde_globals = self.rc_file_content(
            os.path.join(os.environ['HOME'], '.config', 'kdeglobals'))

    @staticmethod
    def context_menu_border_color(window_is_dark: bool) -> tuple:
        """RGBA tuple: (127, 127, 127, 0.8)"""
        if window_is_dark:
            return 127, 127, 127, 0.8
        return 127, 127, 127, 0.8

    @staticmethod
    def context_menu_padding() -> int:
        """..."""
        return 4

    @staticmethod
    def context_menu_separator_color_type() -> str:
        """window-border, disabled-text"""
        return 'window-border'

    @staticmethod
    def context_menu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 8, 4, 8, 4

    @staticmethod
    def context_menu_spacing() -> int:
        """..."""
        return 0

    def control_button_order(self) -> tuple:
        """..."""
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
            SRC_DIR, 'static',
            'kde-breeze-control-buttons', button_name + '.svg')
        return (
            # f'background: url({url_icon}) top center no-repeat;'
            'QControlButton {'
            f'background: url({url_icon}) center no-repeat;'
            '}')

    def icon_theme_name(self) -> str | None:
        """..."""
        group, key = '[Icons]', 'Theme'
        if group in self.__kde_globals and key in self.__kde_globals[group]:
            return self.__kde_globals[group][key]
        return None

    def use_global_menu(self) -> bool:
        """..."""
        group, key = '[Windows]', 'BorderlessMaximizedWindows'
        if group in self.__kwinrc and key in self.__kwinrc[group]:
            return True if self.__kwinrc[group][key] == 'true' else False

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 4, 4, 0, 0

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 0, 1, 0, 1


class EnvSettingsGnome(EnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()

    @staticmethod
    def context_menu_border_color(window_is_dark: bool) -> tuple:
        """RGBA tuple: (127, 127, 127, 0.8)"""
        if window_is_dark:
            return 127, 127, 127, 0.8
        return 127, 127, 127, 0.8

    @staticmethod
    def context_menu_padding() -> int:
        """..."""
        return 6

    @staticmethod
    def context_menu_separator_color_type() -> str:
        """window-border, disabled-text"""
        return 'disabled-text'

    @staticmethod
    def context_menu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 8, 6, 8, 6

    @staticmethod
    def context_menu_spacing() -> int:
        """..."""
        return 0

    def control_button_order(self) -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        button_layout = cli.output_by_args(
            ["gsettings", "get", "org.gnome.desktop.wm.preferences",
             "button-layout"]).split(':')

        if not button_layout:
            return (3,), (0, 1, 2)

        d = {'close': 2, 'maximize': 1, 'minimize': 0}
        left = []
        for x in button_layout[0].split(','):
            if x in d:
                left.append(d[x])
            else:
                left.append(3)

        right = []
        for x in button_layout[1].split(','):
            if x in d:
                right.append(d[x])
            else:
                right.append(3)

        return tuple(left), tuple(right)

    @staticmethod
    def control_button_style(*args, **kwargs) -> str:
        """..."""
        return (
            'QControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  padding: 1px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 5px 4px 5px 4px;'
            '  padding: 2px 1px 1px 2px;'
            '}'
            'QControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')

    def use_global_menu(self) -> bool:
        """..."""
        # TODO: auto
        return False

    def icon_theme_name(self) -> str | None:
        """..."""
        icon_theme = self.cli.output_by_args(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'icon-theme'])
        return icon_theme if icon_theme else None

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 10, 10, 10, 10

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 5, 7, 5, 7


class EnvSettingsCinnamon(EnvSettingsGnome):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()


class EnvSettingsXFCE(EnvSettingsGnome):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()


class EnvSettingsMac(EnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()


class EnvSettingsWindows11(EnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()


class EnvSettingsWindows10(EnvSettingsWindows11):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()


class EnvSettingsWindows7(EnvSettingsWindows11):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()


class GuiEnv(object):
    """..."""
    def __init__(
            self,
            operational_system: str,
            desktop_environment: str,
            follow_platform: bool = True) -> None:
        """..."""
        self.__operational_system = operational_system
        self.__desktop_environment = desktop_environment
        self.__follow_platform = follow_platform
        self.__gui_env_settings = self.__get_gui_env_settings()

    def settings(self) -> EnvSettings:
        """..."""
        return self.__gui_env_settings

    def __get_gui_env_settings(self) -> EnvSettings:
        # ...
        if self.__follow_platform:
            if self.__operational_system == 'linux':

                if self.__desktop_environment == 'plasma':
                    return EnvSettingsPlasma()

                if self.__desktop_environment == 'cinnamon':
                    return EnvSettingsCinnamon()

                if self.__desktop_environment == 'xfce':
                    return EnvSettingsXFCE()

                return EnvSettingsGnome()

            if self.__operational_system == 'mac':
                return EnvSettingsMac()

            if self.__operational_system == 'windows':

                if self.__desktop_environment == 'windows-7':
                    return EnvSettingsWindows7()

                if self.__desktop_environment == 'windows-10':
                    return EnvSettingsWindows10()

                return EnvSettingsWindows11()

        return EnvSettings()
