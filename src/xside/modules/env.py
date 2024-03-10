#!/usr/bin/env python3
import xside.modules.desktopstyles as desktopstyles
import xside.modules.desktopsettings as desktopsettings


class Env(object):
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

    def style(self) -> desktopstyles.EnvStyle:
        """..."""
        return self.__get_env(style=True)

    def settings(self) -> desktopsettings.EnvSettings:
        """..."""
        return self.__get_env()

    def __get_env(
            self, style: bool = False
            ) -> desktopstyles.EnvStyle | desktopsettings.EnvSettings:
        # ...
        if self.__follow_platform:
            if self.__operational_system == 'linux':

                if self.__desktop_environment == 'plasma':
                    if style:
                        return desktopstyles.EnvStylePlasma()
                    return desktopsettings.EnvSettingsPlasma()

                if self.__desktop_environment == 'cinnamon':
                    if style:
                        return desktopstyles.EnvStyleCinnamon()
                    return desktopsettings.EnvSettingsCinnamon()

                if self.__desktop_environment == 'xfce':
                    if style:
                        return desktopstyles.EnvStyleXFCE()
                    return desktopsettings.EnvSettingsXFCE()

                if self.__desktop_environment == 'mate':
                    if style:
                        return desktopstyles.EnvStyleMate()
                    return desktopsettings.EnvSettingsMate()

                if style:
                    return desktopstyles.EnvStyleGnome()
                return desktopsettings.EnvSettingsGnome()

            if self.__operational_system == 'mac':
                if style:
                    return desktopstyles.EnvStyleMac()
                return desktopsettings.EnvSettingsMac()

            if self.__operational_system == 'windows':

                if self.__desktop_environment == 'windows-7':
                    if style:
                        return desktopstyles.EnvStyleWindows7()
                    return desktopsettings.EnvSettingsWindows7()

                if self.__desktop_environment == 'windows-10':
                    if style:
                        return desktopstyles.EnvStyleWindows10()
                    return desktopsettings.EnvSettingsWindows10()

                if style:
                    return desktopstyles.EnvStyleWindows11()
                return desktopsettings.EnvSettingsWindows11()

        if style:
            return desktopstyles.EnvStyle()
        return desktopsettings.EnvSettings()
