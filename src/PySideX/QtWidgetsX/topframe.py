#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.core import BaseTopFrame
from PySideX.QtWidgetsX.modules.platform import Platform
from PySideX.QtWidgetsX.modules.dynamicstyle import DynamicStyle
from PySideX.QtWidgetsX.modules.dynamicstyle import StyleParser


class TopFrame(BaseTopFrame):
    """..."""

    def __init__(self, follow_platform: bool = True, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__follow_platform = follow_platform
        self.__platform = Platform()

        self.__dynamic_style = DynamicStyle(self)
        self.__style_sheet = self.__dynamic_style.build_style()

        self.__style_parser = StyleParser(self.__style_sheet)
        self.__style_sheet = self.__style_parser.style_sheet()

        self.central_widget().set_style_sheet(self.__style_sheet)

    def follow_platform(self) -> bool:
        """..."""
        return self.__follow_platform

    def platform(self) -> Platform:
        """..."""
        return self.__platform

    def set_style_sheet(self, style: str) -> None:
        """..."""
        self.__style_parser.set_style_sheet(self.__style_sheet + style)
        self.__style_sheet = self.__style_parser.style_sheet()

        self.central_widget().set_style_sheet(self.__style_sheet)
