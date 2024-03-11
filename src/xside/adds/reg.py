#!/usr/bin/env python3
import os
import pathlib

from xside.modules.platform import Platform
import xside.modules.reg as reg


class Reg(reg.Reg):
    """Additions registration"""
    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)
        self.__reg = os.path.join(
            pathlib.Path(__file__).resolve().parent, 'static', 'reg.json')


class RegUser(reg.Reg):
    """Additions registration"""
    def __init__(self, *args, **kwargs):
        """..."""
        super().__init__(*args, **kwargs)

        platform = Platform()
        if platform.operational_system() == 'windows':
            self.__path = os.path.join(
                pathlib.Path.home(), 'AppData', 'Roaming', 'xside', 'reg')
        else:
            self.__path = os.path.join(
                pathlib.Path.home(), '.config', 'xside', 'reg')

            self.__reg = path

        pathlib.Path(self.__path).mkdir(parents=True, exist_ok=True)
        self.__reg = os.path.join(self.__path, 'reg.json')

    def path(self) -> str:
        """Registration path

        json db file path
        Default for Unix: <pathlib.Path.home()>/.config/xside/reg
        Default for Windows: <pathlib.Path.home()>/AppData/Roaming/xside/reg/
        """
        return self.__path

    def set_path(self, path: str) -> None:
        """Set the registration path

        json db file path
        Default for Unix: <pathlib.Path.home()>/.config/xside/reg
        Default for Windows: <pathlib.Path.home()>/AppData/Roaming/xside/reg/
        """
        self.__path = path
