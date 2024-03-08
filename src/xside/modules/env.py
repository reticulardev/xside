#!/usr/bin/env python3
import xside.modules.styles as styles


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

    def settings(self) -> styles.EnvStyle:
        """..."""
        return self.__gui_env_settings

    def __get_gui_env_settings(self) -> styles.EnvStyle:
        # ...
        if self.__follow_platform:
            if self.__operational_system == 'linux':

                if self.__desktop_environment == 'plasma':
                    return styles.EnvStylePlasma()

                if self.__desktop_environment == 'cinnamon':
                    return styles.EnvStyleCinnamon()

                if self.__desktop_environment == 'xfce':
                    return styles.EnvStyleXFCE()

                if self.__desktop_environment == 'mate':
                    return styles.EnvStyleMate()

                return EnvStyleGnome()

            if self.__operational_system == 'mac':
                return styles.EnvStyleMac()

            if self.__operational_system == 'windows':

                if self.__desktop_environment == 'windows-7':
                    return styles.EnvStyleWindows7()

                if self.__desktop_environment == 'windows-10':
                    return styles.EnvStyleWindows10()

                return styles.EnvStyleWindows11()

        return styles.EnvStyle()
