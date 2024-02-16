#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.applicationwindow import QApplicationWindow


class QWindowMoveArea(QtWidgets.QFrame):
    """Window move area"""
    mouse_double_click_event_signal = QtCore.Signal(object)
    mouse_press_event_signal = QtCore.Signal(object)
    mouse_release_event_signal = QtCore.Signal(object)

    def __init__(
            self, toplevel: QApplicationWindow, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param toplevel: QApplicationWindow app main window instance
        """
        super().__init__(*args, **kwargs)
        self.__toplevel = toplevel
        self.__enable = True

        self.__screen_w = self.__toplevel.screen().size().width()
        self.__screen_h = self.__toplevel.screen().size().height()

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.set_contents_margins(0, 0, 0, 0)

        self.__timer = QtCore.QTimer()

    def set_enable(self, enable: bool) -> None:
        """Enable or disable the window moving area.

        The area does not disappear, it just does not respond to clicking and
        dragging the mouse cursor.
        """
        self.__enable = enable

    def __shadow_on_press(self):
        conditions = [
            self.__toplevel.x() + self.__toplevel.width() != self.__screen_w,
            self.__toplevel.y() + self.__toplevel.height() != self.__screen_h,
            self.__toplevel.x() != 0, self.__toplevel.y() != 0]
        if any(conditions):
            if not self.__toplevel.is_server_side_decorated():
                self.__toplevel.set_shadow_as_hidden(False)
        self.__timer.stop()

    def __shadow_on_release(self):
        conditions = [
            self.__toplevel.x() + self.__toplevel.width() == self.__screen_w,
            self.__toplevel.y() + self.__toplevel.height() == self.__screen_h,
            self.__toplevel.x() == 0, self.__toplevel.y() == 0]
        if any(conditions):
            self.__toplevel.set_shadow_as_hidden(True)
        else:
            if not self.__toplevel.is_server_side_decorated():
                self.__toplevel.set_shadow_as_hidden(False)
        self.__timer.stop()

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
                    self.__timer.timeout.connect(self.__shadow_on_press)
                    self.__timer.start(100)
                    self.__toplevel.window_handle().start_system_move()

    def mouse_release_event(self, event: QtGui.QMouseEvent) -> None:
        """..."""
        if self.__enable:
            self.mouse_release_event_signal.emit(event)
            if not self.__toplevel.is_server_side_decorated():
                self.__timer.timeout.connect(self.__shadow_on_release)
                self.__timer.start(100)

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
