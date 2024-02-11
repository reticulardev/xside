#!/usr/bin/env python3
import os
import sys

from PySide6 import QtGui
from __feature__ import snake_case

from PySideX.QtWidgetsX.modules.parser import DesktopFile
import PySideX.QtWidgetsX.modules.cli as cli
import PySideX.QtWidgetsX.modules.color as color

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class GlobalEnvSettings(object):
    """Base environment settings"""

    def __init__(self):
        self.palette = QtGui.QPalette()

    def contextmenu_background_color(self) -> QtGui.QColor:
        """..."""
        return self.window_background_color()

    def contextmenu_border_color(self) -> QtGui.QColor:
        """..."""
        return self.window_border_color()

    def contextmenu_border_radius(self) -> int:
        """..."""
        return self.window_border_radius()[0]

    @staticmethod
    def contextmenu_padding() -> tuple:
        """..."""
        return 4, 4, 4, 4

    def contextmenu_separator_color(self) -> QtGui.QColor:
        """..."""
        return self.window_border_color()

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 0, 4, 0, 4

    @staticmethod
    def contextmenu_spacing() -> int:
        """..."""
        return 0

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_accent_color()

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_accent_color()

    def contextmenubutton_border_radius(self) -> int:
        """..."""
        contextmenu_bdr = self.contextmenu_border_radius()
        return contextmenu_bdr - 4 if contextmenu_bdr > 4 else contextmenu_bdr

    def contextmenubutton_foreground_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_foreground_color()

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 4, 6, 4, 6

    @staticmethod
    def controlbutton_margin() -> tuple:
        """..."""
        return 2, 0, 2, 0

    @staticmethod
    def controlbutton_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (2, 1, 0), (3,)

    @staticmethod
    def controlbutton_style(*args, **kwargs) -> str:
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

    def desktop_is_using_global_menu(self) -> bool:
        """..."""
        return False

    @staticmethod
    def headerbar_margin() -> tuple:
        """..."""
        return 4, 4, 4, 4

    @staticmethod
    def icon_theme_name() -> str:
        """..."""
        return 'hicolor'

    def text_disabled_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(170, 170, 170, 255)
        return QtGui.QColor(120, 120, 120, 255)

    @staticmethod
    def windowcontrolbutton_margin() -> tuple:
        """..."""
        return 2, 0, 2, 0

    @staticmethod
    def windowcontrolbutton_spacing() -> int:
        """..."""
        return 6

    def window_accent_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)

    def window_background_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(QtGui.QPalette.Window)

    def window_background_darker_color(self) -> QtGui.QColor:
        """..."""
        step = 4 if self.window_is_dark() else 10
        return color.rgba_to_qcolor(color.darken_rgba(
            self.window_background_color().to_tuple(), step))

    def window_background_lighter_color(self) -> QtGui.QColor:
        """..."""
        step = 4 if self.window_is_dark() else 5
        return color.rgba_to_qcolor(color.lighten_rgba(
            self.window_background_color().to_tuple(), step))

    def window_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return color.rgba_to_qcolor(
                color.lighten_rgba(
                    self.palette.color(QtGui.QPalette.Window).to_tuple(), 15))

        return color.rgba_to_qcolor(color.darken_rgba(
            self.palette.color(QtGui.QPalette.Window).to_tuple(), 30))

    def window_foreground_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.WindowText)

    def window_is_dark(self) -> bool:
        """..."""
        return color.is_dark(self.window_background_color().to_tuple())

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 5, 5, 5, 5

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 0, 1, 0, 1


class EnvSettingsPlasma(GlobalEnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()
        filerc = os.path.join(os.environ['HOME'], '.config', 'kwinrc')
        self.__kwinrc = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})

        filerc = os.path.join(os.environ['HOME'], '.config', 'breezerc')
        self.__breezerc = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})

        filerc = os.path.join(os.environ['HOME'], '.config', 'kdeglobals')
        self.__kde_globals = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})

    def contextmenu_background_color(self) -> QtGui.QColor:
        """..."""
        cor = self.window_background_color()
        return QtGui.QColor(cor.red(), cor.green(), cor.blue(), 225)

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 8, 4, 8, 4

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        cor = self.window_accent_color()
        return QtGui.QColor(cor.red(), cor.green(), cor.blue(), 100)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_accent_color()

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 2, 6, 2, 6

    def controlbutton_order(self) -> tuple:
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

    def controlbutton_style(
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

    def desktop_is_using_global_menu(self) -> bool:
        """..."""
        group, key = '[Windows]', 'BorderlessMaximizedWindows'
        if group in self.__kwinrc and key in self.__kwinrc[group]:
            return True if self.__kwinrc[group][key] == 'true' else False

    def icon_theme_name(self) -> str | None:
        """..."""
        group, key = '[Icons]', 'Theme'
        if group in self.__kde_globals and key in self.__kde_globals[group]:
            return self.__kde_globals[group][key]
        return None

    def text_disabled_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(
            QtGui.QPalette.Disabled, QtGui.QPalette.Text)

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 4, 4, 0, 0


class EnvSettingsGnome(GlobalEnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()

    @staticmethod
    def contextmenu_bg_alpha() -> float:
        """..."""
        return 1.0

    @staticmethod
    def contextmenu_padding() -> tuple:
        """..."""
        return 6, 6, 6, 6

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 8, 6, 8, 6

    @staticmethod
    def contextmenubutton_bg_hover_alpha() -> float:
        """..."""
        return 1.0

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.palette.color(QtGui.QPalette.AlternateBase)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.contextmenubutton_background_hover_color()

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 6, 12, 6, 12

    def controlbutton_order(self) -> tuple:
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
    def controlbutton_style(*args, **kwargs) -> str:
        """..."""
        return (
            'QControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 5px 4px 5px 4px;'
            '  padding: 2px 1px 1px 2px;'
            '}'
            'QControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')

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

    def controlbutton_style(
            self, window_is_dark: bool,
            button_name: str,
            button_state: str) -> str:
        """..."""
        if button_name == 'close':
            url_icon = os.path.join(
                SRC_DIR, 'static', 'cinnamon-control-buttons',
                'window-close.svg')

            accent = self.window_accent_color()
            accent_light = color.lighten_rgba(accent.to_tuple(), 20)
            return (
                'QControlButton {'
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
                'QControlButton:hover {'
                '  background-color: rgba('
                f' {accent_light[0]},'
                f' {accent_light[1]},'
                f' {accent_light[2]},'
                f' {accent_light[3]});'
                '}')
        return (
            'QControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 5px 2px 5px 2px;'
            '  padding: 1px 0px 0px 1px;'
            '}'
            'QControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')


class EnvSettingsXFCE(GlobalEnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()

    @staticmethod
    def contextmenu_bg_alpha() -> float:
        """..."""
        return 1.0

    def contextmenu_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(50, 50, 50, 255)
        return QtGui.QColor(180, 180, 180, 255)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return color.rgba_to_qcolor(
            color.darken_rgba(self.window_accent_color().to_tuple(), 50))

    def contextmenubutton_foreground_hover_color(self) -> QtGui.QColor:
        """..."""
        return QtGui.QColor(255, 255, 255, 255)

    def contextmenu_border_radius(self) -> int:
        """..."""
        return 0

    @staticmethod
    def contextmenu_padding() -> tuple:
        """..."""
        return 1, 6, 1, 6

    def contextmenu_separator_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(50, 50, 50, 255)
        return QtGui.QColor(180, 180, 180, 255)

    @staticmethod
    def contextmenu_separator_margin() -> tuple:
        """Left, top, right and bottom margins tuple"""
        return 1, 0, 1, 0

    @staticmethod
    def contextmenubutton_bg_hover_alpha() -> float:
        """..."""
        return 1.0

    @staticmethod
    def contextmenubutton_padding() -> tuple:
        """..."""
        return 2, 4, 2, 4

    def controlbutton_order(self) -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (3,), (0, 1, 2)

    @staticmethod
    def controlbutton_style(*args, **kwargs) -> str:
        """..."""
        return (
            'QControlButton {'
            '  border: 0px;'
            '  border-radius: 3px;'
            '  margin: 0px;'
            '  padding: 1px;'
            '}'
            'QControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '}')

    def window_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return color.rgba_to_qcolor(
                color.lighten_rgba(
                    self.palette.color(QtGui.QPalette.Window).to_tuple(), 30))

        return color.rgba_to_qcolor(color.darken_rgba(
            self.palette.color(QtGui.QPalette.Window).to_tuple(), 60))

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 8, 8, 0, 0


class EnvSettingsMate(EnvSettingsXFCE):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()

    def contextmenu_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(80, 80, 80, 255)
        return QtGui.QColor(180, 180, 180, 255)

    def contextmenu_border_radius(self) -> int:
        """..."""
        return self.window_border_radius()[0]

    def contextmenu_separator_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(80, 80, 80, 255)
        return QtGui.QColor(200, 200, 200, 255)

    def contextmenubutton_background_hover_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return QtGui.QColor(62, 62, 62, 255)
        return QtGui.QColor(222, 222, 222, 255)

    def contextmenubutton_border_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.contextmenubutton_background_hover_color()

    def contextmenubutton_border_radius(self) -> int:
        """..."""
        return 0

    def contextmenubutton_foreground_hover_color(self) -> QtGui.QColor:
        """..."""
        return self.window_foreground_color()

    @staticmethod
    def controlbutton_style(*args, **kwargs) -> str:
        """..."""
        return (
            'QControlButton {'
            '  border: 0px;'
            '  border-radius: 10px;'
            '  background-color: rgba(127, 127, 127, 0.2);'
            '  margin: 3px 4px 3px 4px;'
            '  padding: 1px 0px 0px 1px;'
            '}'
            'QControlButton:hover {'
            '  background-color: rgba(127, 127, 127, 0.3);'
            '}')


class EnvSettingsMac(GlobalEnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()


class EnvSettingsWindows11(GlobalEnvSettings):
    """..."""

    def __init__(self):
        """..."""
        super().__init__()

    @staticmethod
    def controlbutton_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def controlbutton_order() -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        return (3,), (0, 1, 2)

    def controlbutton_style(
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
            button_name = 'window-close'

        if button_state == 'hover':
            button_name += '-hover'
        if button_state == 'inactive':
            button_name += '-inactive'

        if window_is_dark:
            button_name += '-symbolic'

        url_icon = os.path.join(
            SRC_DIR, 'static',
            'windows-11-control-buttons', button_name + '.svg')

        return (
            'QControlButton {'
            f'background: url({url_icon}) center no-repeat;'
            f'width: {44 if "close" in button_name else 42}px;'
            'height: 26px;'
            'border-radius: 0px;'
            'border: 0px;'
            'margin: 0px;'
            '}')

    @staticmethod
    def headerbar_margin() -> tuple:
        """..."""
        return 0, 1, 0, 0

    @staticmethod
    def windowcontrolbutton_margin() -> tuple:
        """..."""
        return 0, 0, 0, 0

    @staticmethod
    def windowcontrolbutton_spacing() -> int:
        """..."""
        return 0

    def window_border_color(self) -> QtGui.QColor:
        """..."""
        if self.window_is_dark():
            return color.rgba_to_qcolor(
                color.lighten_rgba(
                    self.palette.color(QtGui.QPalette.Window).to_tuple(), 15))

        return color.rgba_to_qcolor(color.darken_rgba(
            self.palette.color(QtGui.QPalette.Window).to_tuple(), 50))

    @staticmethod
    def window_border_radius() -> tuple:
        """..."""
        return 8, 8, 0, 0

    @staticmethod
    def window_icon_margin() -> tuple:
        """..."""
        return 5, 2, 5, 2


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

    def settings(self) -> GlobalEnvSettings:
        """..."""
        return self.__gui_env_settings

    def __get_gui_env_settings(self) -> GlobalEnvSettings:
        # ...
        if self.__follow_platform:
            if self.__operational_system == 'linux':

                if self.__desktop_environment == 'plasma':
                    # EnvSettingsWindows11()  # EnvSettingsPlasma()
                    return EnvSettingsPlasma()

                if self.__desktop_environment == 'cinnamon':
                    return EnvSettingsCinnamon()

                if self.__desktop_environment == 'xfce':
                    return EnvSettingsXFCE()

                if self.__desktop_environment == 'mate':
                    return EnvSettingsMate()

                return EnvSettingsGnome()

            if self.__operational_system == 'mac':
                return EnvSettingsMac()

            if self.__operational_system == 'windows':

                if self.__desktop_environment == 'windows-7':
                    return EnvSettingsWindows7()

                if self.__desktop_environment == 'windows-10':
                    return EnvSettingsWindows10()

                return EnvSettingsWindows11()

        return GlobalEnvSettings()
