#!/usr/bin/env python3
import xside.modules.desktopstyles as desktopstyles


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

    def settings(self) -> desktopstyles.EnvStyle:
        """..."""
        return self.__gui_env_settings

    def __get_gui_env_settings(self) -> desktopstyles.EnvStyle:
        # ...
        if self.__follow_platform:
            if self.__operational_system == 'linux':

                if self.__desktop_environment == 'plasma':
                    return desktopstyles.EnvStylePlasma()

                if self.__desktop_environment == 'cinnamon':
                    return desktopstyles.EnvStyleCinnamon()

                if self.__desktop_environment == 'xfce':
                    return desktopstyles.EnvStyleXFCE()

                if self.__desktop_environment == 'mate':
                    return desktopstyles.EnvStyleMate()

                return EnvStyleGnome()

            if self.__operational_system == 'mac':
                return desktopstyles.EnvStyleMac()

            if self.__operational_system == 'windows':

                if self.__desktop_environment == 'windows-7':
                    return desktopstyles.EnvStyleWindows7()

                if self.__desktop_environment == 'windows-10':
                    return desktopstyles.EnvStyleWindows10()

                return desktopstyles.EnvStyleWindows11()

        return desktopstyles.EnvStyle()
