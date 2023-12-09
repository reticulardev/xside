#!/usr/bin/env python3
import os
import subprocess
import sys
from enum import Enum

from PySideX.tools.desktop_entry_parse import DesktopFile


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class EnvSettings(object):
    """..."""

    def __init__(self, *args, **kwargs):
        """..."""
        self.__kwinrc = self.rc_file_content(
            os.path.join(os.environ['HOME'], '.config', 'kwinrc')).content
        self.__breezerc = self.rc_file_content(
            os.path.join(os.environ['HOME'], '.config', 'breezerc')).content

    @property
    def breeze_rc_content(self) -> dict:
        """..."""
        return self.__breezerc

    @staticmethod
    def command_output(command_args: list) -> str | None:
        """..."""
        # ['ls', '-l']
        try:
            command = subprocess.Popen(
                command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = command.communicate()
        except ValueError as er:
            print(er)
            print(f'Error in command args: "{command_args}"')
        else:
            return stdout.decode() if not stderr.decode() else None

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
            'border-radius: 10px;'
            'padding: 1px;'
            'background-color: rgba(127, 127, 127, 0.5);'
            '}'
            'QControlButton:hover {'
            'background-color: rgba(200, 200, 200, 0.5);'
            '}')

    @property
    def kwin_rc_content(self) -> dict:
        """..."""
        return self.__kwinrc

    @staticmethod
    def rc_file_content(file_url: str) -> str | None:
        """..."""
        if os.path.isfile(file_url):
            return DesktopFile(url=file_url)
        return None

    def use_global_menu(self) -> bool:
        """..."""
        top, key = '[Windows]', 'BorderlessMaximizedWindows'
        if top in self.__kwinrc and key in self.__kwinrc[top]:
            return True if self.__kwinrc[top][key] == 'true' else False

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 5, 5, 5, 5


class EnvSettingsPlasma(EnvSettings):
    """..."""

    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)

    def control_button_order(self) -> tuple:
        """..."""
        right_buttons = 'IAX'  # X = close, A = max, I = min
        left_buttons = 'M'  # M = icon, F = above all

        top = '[org.kde.kdecoration2]'
        key_left, key_right = 'ButtonsOnLeft', 'ButtonsOnRight'
        if top in self.kwin_rc_content:
            if key_left in self.kwin_rc_content[top]:
                left_buttons = self.kwin_rc_content[top][key_left]

            if key_right in self.kwin_rc_content[top]:
                right_buttons = self.kwin_rc_content[top][key_right]

        d = {'X': 2, 'A': 1, 'I': 0, 'M': 3}
        return tuple(
            d[x] for x in left_buttons
            if x == 'X' or x == 'A' or x == 'I' or x == 'M'), tuple(
            d[x] for x in right_buttons
            if x == 'X' or x == 'A' or x == 'I' or x == 'M')

    def control_button_style(
            self, window_is_dark: bool, button_name: str, button_state) -> str:
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
            if (top in self.breeze_rc_content and
                    key in self.breeze_rc_content[top]):
                if self.breeze_rc_content[top][key] == 'true':
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
            SRC_DIR, 'kde-breeze-control-buttons', button_name + '.svg')
        return (
            # f'background: url({url_icon}) top center no-repeat;'
            'QControlButton {'
            f'background: url({url_icon}) center no-repeat;'
            '}')

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 4, 4, 0, 0


class Platform(object):
    """..."""
    OperationalSystem = Enum(
        'OperationalSystem', ['UNKNOWN', 'LINUX', 'BSD', 'MAC', 'WINDOWS'])
    DesktopEnvironment = Enum(
        'DesktopEnvironment', ['UNKNOWN', 'KDE', 'GNOME', 'CINNAMON', 'XFCE'])

    def __init__(self, platform_integration: bool = True):
        """..."""
        self.__platform_integration = platform_integration
        self.__desktop_environment = self.__get_desktop_environment()
        self.__operational_system = self.__get_operational_system()
        self.__env_settings = self.env_settings()

    @property
    def desktop_environment(self) -> DesktopEnvironment:
        """..."""
        return self.__desktop_environment

    def env_settings(self) -> EnvSettings | None:
        """..."""
        if self.__platform_integration:
            if self.__operational_system == self.OperationalSystem.LINUX:
                if self.__desktop_environment == self.DesktopEnvironment.KDE:
                    return EnvSettingsPlasma()
        return EnvSettings()

    @property
    def operational_system(self) -> OperationalSystem:
        """..."""
        return self.__operational_system

    def window_control_button_style(
            self, window_is_dark: bool,
            button_name: str, button_state) -> str | None:
        """Control button style

        :param window_is_dark: True or False
        :param button_name: 'minimize', 'maximize', 'restore' or 'close'
        :param button_state: 'normal', 'hover', 'inactive'
        """

        return self.__env_settings.control_button_style(
            window_is_dark, button_name, button_state)

    def window_control_button_order(self) -> tuple | None:
        """..."""
        return self.__env_settings.control_button_order()

    def window_border_radius(self) -> tuple | None:
        """..."""
        return self.__env_settings.window_border_radius()

    def window_use_global_menu(self) -> bool:
        """..."""
        return self.__env_settings.use_global_menu()

    def __get_desktop_environment(self) -> DesktopEnvironment:
        # ...
        if (os.environ['DESKTOP_SESSION'] == 'plasma' or
                os.environ['XDG_SESSION_DESKTOP'] == 'KDE' or
                os.environ['XDG_CURRENT_DESKTOP'] == 'KDE'):
            return self.DesktopEnvironment.KDE

        return self.DesktopEnvironment.UNKNOWN

    def __get_operational_system(self) -> OperationalSystem:
        # ...
        if sys.platform == 'win32':
            # Config path: $HOME + AppData\Roaming\
            return self.OperationalSystem.WINDOWS
        # Config path: $HOME + .config
        return self.OperationalSystem.LINUX
