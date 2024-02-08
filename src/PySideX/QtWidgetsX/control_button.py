#!/usr/bin/env python3
import logging
import math
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.application_window import QApplicationWindow
import PySideX.QtWidgetsX.modules.color as color
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv

SRC_DIR = os.path.dirname(os.path.abspath(__file__))


class QControlButton(QtWidgets.QToolButton):
    """Control Button

    Window control button, such as window close and maximize buttons
    """
    enter_event_signal = QtCore.Signal(object)
    leave_event_signal = QtCore.Signal(object)

    def __init__(
            self, toplevel: QApplicationWindow, button_id: int,
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes.

        :param button_id:
            0 is the minimize button
            1 is the maximize button
            2 is the close button
        """
        super().__init__(*args, **kwargs)
        # Param
        self.__toplevel = toplevel
        self.__button_id = button_id

        # Flags
        self.__buttons_schema = {0: 'minimize', 1: 'maximize', 2: 'close'}
        self.__background_color = None
        self.__is_dark = self.__is_dark_tone()
        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment())

        self.__maximize_or_restore_icon = 'maximize'
        self.__toplevel.resize_event_signal.connect(
            self.__check_maximize_and_restore_icon)

        self.__update_button()

    def __update_button(self, background_color: tuple = None) -> None:
        """..."""
        if background_color:
            self.__background_color = background_color
            self.__is_dark = self.__is_dark_tone()

        if self.__button_id not in (0, 1, 2):
            raise ValueError(
                'The value must be 0, 1 or 2. The values represent "minimize",'
                ' "maximize" and "close" buttons respectively.')

        if self.__button_id == 0:
            style = self.__gui_env.settings().controlbutton_style(
                self.__is_dark, 'minimize', 'normal')

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(
                    QtGui.QIcon.from_theme('window-minimize-symbolic'))

            self.clicked.connect(
                lambda _: self.__toplevel.show_minimized())

        elif self.__button_id == 1:
            style = self.__gui_env.settings().controlbutton_style(
                self.__is_dark, 'maximize', 'normal')

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(
                    QtGui.QIcon.from_theme('window-maximize-symbolic'))
        else:
            style = self.__gui_env.settings().controlbutton_style(
                self.__is_dark, 'close', 'normal')

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(QtGui.QIcon.from_theme('window-close-symbolic'))

            self.clicked.connect(
                lambda _: self.__toplevel.close())

    def __is_dark_tone(self) -> bool:
        # ...
        palette = self.__toplevel.color_by_state_name('window-background')
        self.__background_color = (
            palette.red(), palette.green(), palette.blue(), palette.alpha())

        return color.is_dark(self.__background_color)

    def __check_maximize_and_restore_icon(
            self, event: QtGui.QResizeEvent) -> None:
        # Change maximize button depending on window state
        logging.info(event)  # self.native_parent_widget()

        if self.__button_id == 1:
            self.__maximize_or_restore_icon = 'maximize'
            if (self.__toplevel.is_maximized() or
                    self.__toplevel.is_full_screen()):
                self.__maximize_or_restore_icon = 'restore'

            maximize_style = self.__gui_env.settings().controlbutton_style(
                self.__is_dark, self.__maximize_or_restore_icon, 'normal')

            self.set_style_sheet(maximize_style)
            if self.__maximize_or_restore_icon == 'restore':
                if 'background: url' not in maximize_style:
                    self.set_icon(
                        QtGui.QIcon.from_theme('window-restore-symbolic'))
            else:
                if 'background: url' not in maximize_style:
                    self.set_icon(
                        QtGui.QIcon.from_theme('window-maximize-symbolic'))

            if self.__maximize_or_restore_icon == 'restore':
                self.clicked.connect(
                    lambda _: self.native_parent_widget().show_normal())
            else:
                self.clicked.connect(
                    lambda _: self.native_parent_widget().show_maximized())

    def enter_event(self, event: QtGui.QEnterEvent) -> None:
        if self.__button_id == 1:
            self.set_style_sheet(
                self.__gui_env.settings().controlbutton_style(
                    self.__is_dark, self.__maximize_or_restore_icon, 'hover'))
        else:
            self.set_style_sheet(
                self.__gui_env.settings().controlbutton_style(
                    self.__is_dark,
                    self.__buttons_schema[self.__button_id], 'hover'))

        logging.info(event)
        self.enter_event_signal.emit(self)

    def leave_event(self, event: QtGui.QEnterEvent) -> None:
        if self.__button_id == 1:
            self.set_style_sheet(
                self.__gui_env.settings().controlbutton_style(
                    self.__is_dark, self.__maximize_or_restore_icon, 'normal'))
        else:
            self.set_style_sheet(
                self.__gui_env.settings().controlbutton_style(
                    self.__is_dark,
                    self.__buttons_schema[self.__button_id], 'normal'))

        logging.info(event)
        self.leave_event_signal.emit(self)
