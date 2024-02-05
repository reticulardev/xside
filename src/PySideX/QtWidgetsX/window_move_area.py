#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.application_window import QApplicationWindow


class QWindowMoveArea(QtWidgets.QFrame):
    """Window move area"""
    mouse_double_click_event_signal = QtCore.Signal(object)
    mouse_press_event_signal = QtCore.Signal(object)

    def __init__(
            self, toplevel: QApplicationWindow, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param toplevel: QApplicationWindow app main window instance
        """
        super().__init__(*args, **kwargs)
        self.__toplevel = toplevel

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.set_contents_margins(0, 0, 0, 0)
        self.__enable = True

    def set_enable(self, enable: bool) -> None:
        """Enable or disable the window moving area.

        The area does not disappear, it just does not respond to clicking and
        dragging the mouse cursor.
        """
        self.__enable = enable

    def mouse_press_event(self, event: QtGui.QMouseEvent) -> None:
        """This method has changed.
        Instead, use the 'mouse_press_event_signal' sign

        Such as:
        self.my_window.mouse_press_event_signal.connect(
            self.my_mouse_press_event_method)
        """
        if self.__enable:
            self.mouse_press_event_signal.emit(event)
            if not self.__toplevel.is_server_side_decorated():
                if (event.button() == QtCore.Qt.LeftButton and
                        self.under_mouse()):
                    self.__toplevel.window_handle().start_system_move()

    def mouse_double_click_event(self, event: QtGui.QMouseEvent) -> None:
        """This method has changed.
        Instead, use the 'mouse_double_click_event_signal' sign

        Such as:
        self.my_window.mouse_double_click_event_signal.connect(
            self.my_mouse_double_click_event_method)
        """
        if self.__enable:
            self.mouse_double_click_event_signal.emit(event)
            if event.button() == QtCore.Qt.LeftButton:
                if self.__toplevel.is_maximized():
                    self.native_parent_widget().show_normal()
                elif self.__toplevel.is_full_screen():
                    self.native_parent_widget().show_maximized()
                else:
                    self.native_parent_widget().show_maximized()
