#!/usr/bin/env python3
import logging
import math

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case


class QControlButton(QtWidgets.QToolButton):
    """Control Button

    Window control button, such as window close and maximize buttons
    """
    enter_event_signal = QtCore.Signal(object)
    leave_event_signal = QtCore.Signal(object)

    def __init__(
            self, main_window: QtWidgets, button_id: int,
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes.

        :param button_id:
            0 is the minimize button
            1 is the maximize button
            2 is the close button
        """
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.__button_id = button_id
        self.__buttons_schema = {0: 'minimize', 1: 'maximize', 2: 'close'}

        self.__maximize_or_restore_icon = 'maximize'
        self.__main_window.resize_event_signal.connect(
            self.__check_maximize_and_restore_icon)

        self.__configure_buttons()

    def __configure_buttons(self) -> None:
        # if QtGui.QIcon.theme_name() != icon_theme:
        #     QtGui.QIcon.set_theme_name(icon_theme)

        if self.__button_id not in (0, 1, 2):
            raise ValueError(
                'The value must be 0, 1 or 2. The values represent "minimize",'
                ' "maximize" and "close" buttons respectively.')

        if self.__button_id == 0:
            style = (
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(), 'minimize', 'normal'))

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(
                    QtGui.QIcon.from_theme('window-minimize-symbolic'))

            self.clicked.connect(
                lambda _: self.__main_window.show_minimized())

        elif self.__button_id == 1:
            style = (
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(), 'maximize', 'normal'))

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(
                    QtGui.QIcon.from_theme('window-maximize-symbolic'))
        else:
            style = (
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(), 'close', 'normal'))

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(QtGui.QIcon.from_theme('window-close-symbolic'))

            self.clicked.connect(
                lambda _: self.__main_window.close())

    def __is_dark(self) -> bool:
        # ...
        color = self.__main_window.palette().color(QtGui.QPalette.Window)
        r, g, b = (color.red(), color.green(), color.blue())
        hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
        return False if hsp > 127.5 else True

    def __check_maximize_and_restore_icon(
            self, event: QtGui.QResizeEvent) -> None:
        # Change maximize button depending on window state
        logging.info(event)  # self.native_parent_widget()

        if self.__button_id == 1:
            self.__maximize_or_restore_icon = 'maximize'
            if (self.__main_window.is_maximized() or
                    self.__main_window.is_full_screen()):
                self.__maximize_or_restore_icon = 'restore'

            maximize_style = (
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(),
                    self.__maximize_or_restore_icon, 'normal'))

            self.set_style_sheet(maximize_style)
            if self.__maximize_or_restore_icon == 'restore':
                if 'background: url' not in maximize_style:
                    self.set_icon(
                        QtGui.QIcon.from_theme('window-restore-symbolic'))
            else:
                if 'background: url' not in maximize_style:
                    self.set_icon(QtGui.QIcon.from_theme('go-up'))

            if self.__maximize_or_restore_icon == 'restore':
                self.clicked.connect(
                    lambda _: self.native_parent_widget().show_normal())
            else:
                self.clicked.connect(
                    lambda _: self.native_parent_widget().show_maximized())

    def enter_event(self, event: QtGui.QEnterEvent) -> None:
        if self.__button_id == 1:
            self.set_style_sheet(
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(),
                    self.__maximize_or_restore_icon, 'hover'))
        else:
            self.set_style_sheet(
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(),
                    self.__buttons_schema[self.__button_id], 'hover'))

        logging.info(event)
        self.enter_event_signal.emit(self)

    def leave_event(self, event: QtGui.QEnterEvent) -> None:
        if self.__button_id == 1:
            self.set_style_sheet(
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(),
                    self.__maximize_or_restore_icon, 'normal'))
        else:
            self.set_style_sheet(
                self.__main_window.platform_settings()
                .gui_env.control_button_style(
                    self.__is_dark(),
                    self.__buttons_schema[self.__button_id], 'normal'))

        logging.info(event)
        self.leave_event_signal.emit(self)
