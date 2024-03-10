#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from xside.modules.platform import Platform
from xside.modules.env import Env
from xside.modules.stylesheetops import StyleSheetOps
from xside.widgets.core import BaseTopFrame


class TopFrame(BaseTopFrame):
    """..."""

    def __init__(self, follow_platform: bool = True, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__follow_platform = follow_platform
        self.__platform = Platform()

        self.__env = Env(
            self.__platform.operational_system(),
            self.__platform.desktop_environment(),
            self.__follow_platform)
        self.__style_sheet = self.__env.style().style_sheet()
        self.__styleop = StyleSheetOps()
        self.central_widget().set_style_sheet(self.__style_sheet)

    def follow_platform(self) -> bool:
        """..."""
        return self.__follow_platform

    def platform(self) -> Platform:
        """..."""
        return self.__platform

    def set_style_sheet(self, style: str) -> None:
        """..."""
        self.__styleop.set_stylesheet(self.__style_sheet + style)
        self.__style_sheet = self.__styleop.stylesheet()

        self.central_widget().set_style_sheet(self.__style_sheet)
