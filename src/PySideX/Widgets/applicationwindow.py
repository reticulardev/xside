#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

import PySideX.Widgets.modules.color as color
from PySideX.Widgets.modules.platform import Platform
from PySideX.Widgets.modules.envsettings import GuiEnv
from PySideX.Widgets.modules.dynamicstyle import DynamicStyle
from PySideX.Widgets.modules.dynamicstyle import StyleParser
from PySideX.Widgets.core import BaseWindow


class ApplicationWindow(BaseWindow):
    """Application main window prepared to use CSD

    The edges are rounded and there is no title bar. A custom header bar can
    be added
    """
    event_filter_signal = QtCore.Signal(object)
    reset_style_signal = QtCore.Signal(object)
    resize_event_signal = QtCore.Signal(object)
    set_style_signal = QtCore.Signal(object)
    shadow_visibility_signal = QtCore.Signal(object)

    def __init__(
            self,
            server_side_decoration: bool = False,
            follow_platform: bool = True,
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        # Param
        self.__is_server_side_decorated = server_side_decoration
        self.__follow_platform = follow_platform
        self.__platform = Platform()

        # Flags
        self.__shadow_size = 8
        self.__edge_cursor_position = None
        self.__default_edge_resize_size = 5
        self.__edge_resize_size = self.__default_edge_resize_size

        self.__gui_env = GuiEnv(
            self.__platform.operational_system(),
            self.__platform.desktop_environment(),
            self.__follow_platform)

        self.__is_dark = color.is_dark(
            self.__gui_env.settings().window_background_color().to_tuple())

        self.__timer = QtCore.QTimer()

        # Style
        self.__dynamic_style = DynamicStyle(self)
        self.__style_sheet = self.__dynamic_style.build_style()

        self.__style_parser = StyleParser(self.__style_sheet)
        self.__style_sheet = self.__style_parser.style_sheet()

        self.__style_sheet_fullscreen = (
            self.__dynamic_style.fullscreen_adapted_style(
                self.__style_sheet))

        self.__set_window_decoration()

        # Events
        self.install_event_filter(self)

    def follow_platform(self) -> bool:
        """..."""
        return self.__follow_platform

    def is_dark(self) -> bool:
        """..."""
        return self.__is_dark

    def is_server_side_decorated(self) -> bool:
        """..."""
        return self.__is_server_side_decorated

    def platform(self) -> Platform:
        """..."""
        return self.__platform

    def reset_style(self) -> None:
        """Reset the application style sheet to default"""
        self.__reset_style_properties()

        if self.is_maximized() or self.is_full_screen():
            self.central_widget().set_style_sheet(
                self.__style_sheet_fullscreen)
        else:
            self.central_widget().set_style_sheet(self.__style_sheet)

        self.reset_style_signal.emit(0)

    def set_style_sheet(self, style: str) -> None:
        """Set the application style sheet

        See the documentation about the 'qss' style at:
        doc.qt.io/qtforpython-6/tutorials/basictutorial/widgetstyling.html

        :param style: string containing 'qss' style
        """
        self.__style_parser.set_style_sheet(self.__style_sheet + style)
        self.__style_sheet = self.__style_parser.style_sheet()

        self.__style_sheet_fullscreen = (
            self.__dynamic_style.fullscreen_adapted_style(
                self.__style_sheet))

        if self.__is_server_side_decorated:
            self.__style_sheet = self.__style_sheet_fullscreen

        if self.is_maximized() or self.is_full_screen():
            self.central_widget().set_style_sheet(
                self.__style_sheet_fullscreen)
        else:
            self.central_widget().set_style_sheet(self.__style_sheet)

        self.set_style_signal.emit(0)

    def shadow_size(self) -> int:
        """..."""
        return self.__shadow_size

    def style_sheet(self) -> str:
        """The application style sheet

        :return: string containing 'qss' style
        """
        return self.__style_sheet

    def __reset_style_properties(self) -> None:
        # ...
        self.__style_sheet = self.__dynamic_style.build_style()
        self.__style_sheet_fullscreen = (
            self.__dynamic_style.fullscreen_adapted_style(self.__style_sheet))

    def __set_window_decoration(self) -> None:
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        if not self.__is_server_side_decorated:
            self.set_window_flags(
                QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
            self.__window_shadow_visible(True)

    def __set_edge_cursor_position(self, event: QtCore.QEvent) -> None:
        # Saves the position of the window where the mouse cursor is
        shadow_size = self.__shadow_size if self.is_shadow_visible() else 0
        resize_area = (
            -3 if self.__is_server_side_decorated else shadow_size - 3)
        pos = event.position().to_point()  # QtGui.QHoverEvent(ev.clone())
        window_area = [
            resize_area < pos.x() < self.width() - resize_area,
            resize_area < pos.y() < self.height() - resize_area]
        if self.__is_server_side_decorated:
            window_area = [
                pos.x() < self.width(), pos.y() < self.height()]

        if all(window_area):
            # top-right, top-left, bottom-right, bottom-left
            if (pos.x() > (self.width() - self.__edge_resize_size) and
                    pos.y() < self.__edge_resize_size):
                self.__edge_cursor_position = (
                        QtCore.Qt.Edge.RightEdge | QtCore.Qt.Edge.TopEdge)
            elif (pos.x() < self.__edge_resize_size and
                  pos.y() < self.__edge_resize_size):
                self.__edge_cursor_position = (
                        QtCore.Qt.Edge.LeftEdge | QtCore.Qt.Edge.TopEdge)
            elif (pos.x() > (self.width() - self.__edge_resize_size) and
                  pos.y() > (self.height() - self.__edge_resize_size)):
                self.__edge_cursor_position = (
                        QtCore.Qt.Edge.RightEdge | QtCore.Qt.Edge.BottomEdge)
            elif (pos.x() < self.__edge_resize_size and
                  pos.y() > (self.height() - self.__edge_resize_size)):
                self.__edge_cursor_position = (
                        QtCore.Qt.Edge.LeftEdge | QtCore.Qt.Edge.BottomEdge)

            # left, right, top, bottom
            elif pos.x() <= self.__edge_resize_size:
                self.__edge_cursor_position = QtCore.Qt.Edge.LeftEdge
            elif pos.x() >= (self.width() - self.__edge_resize_size):
                self.__edge_cursor_position = QtCore.Qt.Edge.RightEdge
            elif pos.y() <= self.__edge_resize_size:
                self.__edge_cursor_position = QtCore.Qt.Edge.TopEdge
            elif pos.y() >= (self.height() - self.__edge_resize_size):
                self.__edge_cursor_position = QtCore.Qt.Edge.BottomEdge
            else:
                self.__edge_cursor_position = None
        else:
            self.__edge_cursor_position = None

    def __show_shadow_on_condition(self):
        conditions = [
            self.x() + self.width() != self.screen().size().width(),
            self.y() + self.height() != self.screen().size().height(),
            self.x() != 0, self.y() != 0]
        if any(conditions):
            if not self.is_server_side_decorated():
                self.set_shadow_as_hidden(False)
        self.__timer.stop()

    def __hide_shadow_on_condition(self):
        conditions = [
            self.x() + self.width() == self.screen().size().width(),
            self.y() + self.height() == self.screen().size().height(),
            self.x() == 0, self.y() == 0]
        if any(conditions):
            if self.is_shadow_visible():
                self.set_shadow_as_hidden(True)
                self.shadow_visibility_signal.emit(False)
        else:
            if not self.is_server_side_decorated():
                if not self.is_shadow_visible():
                    self.set_shadow_as_hidden(False)
                    self.shadow_visibility_signal.emit(True)
        self.__timer.stop()

    def __window_shadow_visible(self, visible: bool) -> None:
        # if self.__shadow_is_disabled:
        if self.__is_server_side_decorated:
            self.__edge_resize_size = self.__default_edge_resize_size
        else:
            self.set_shadow_as_hidden(False if visible else True)
            if visible:
                self.__edge_resize_size = (
                        self.__default_edge_resize_size + self.__shadow_size)
            else:
                self.__edge_resize_size = self.__default_edge_resize_size

    def __update_cursor_shape(self) -> None:
        # Updates the mouse cursor appearance
        if not self.__edge_cursor_position:
            self.set_cursor(QtCore.Qt.CursorShape.ArrowCursor)
        else:
            if (self.__edge_cursor_position == QtCore.Qt.Edge.LeftEdge or
                    self.__edge_cursor_position == QtCore.Qt.Edge.RightEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeHorCursor)

            elif (self.__edge_cursor_position == QtCore.Qt.Edge.TopEdge or
                  self.__edge_cursor_position == QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeVerCursor)

            elif (self.__edge_cursor_position == QtCore.Qt.Edge.LeftEdge |
                  QtCore.Qt.Edge.TopEdge or
                  self.__edge_cursor_position == QtCore.Qt.Edge.RightEdge |
                  QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeFDiagCursor)

            elif (self.__edge_cursor_position == QtCore.Qt.Edge.RightEdge |
                  QtCore.Qt.Edge.TopEdge or
                  self.__edge_cursor_position == QtCore.Qt.Edge.LeftEdge |
                  QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeBDiagCursor)

    def event_filter(
            self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        self.event_filter_signal.emit(event)

        if self.__is_server_side_decorated:
            self.central_widget().set_style_sheet(self.__style_sheet)
            if event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(event)
        else:
            if event.type() == QtCore.QEvent.HoverMove:
                self.__set_edge_cursor_position(event)
                self.__update_cursor_shape()

            elif event.type() == QtCore.QEvent.Type.HoverEnter:
                self.__timer.timeout.connect(self.__hide_shadow_on_condition)
                self.__timer.start(100)

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self.__update_cursor_shape()
                if self.__edge_cursor_position:
                    self.window_handle().start_system_resize(
                        self.__edge_cursor_position)

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.set_cursor(QtCore.Qt.CursorShape.ArrowCursor)

            elif event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(0)

                if self.is_maximized() or self.is_full_screen():
                    self.central_widget().set_style_sheet(
                        self.__style_sheet_fullscreen)

                    self.__window_shadow_visible(False)
                else:
                    self.central_widget().set_style_sheet(self.__style_sheet)

                    if not self.__is_server_side_decorated:
                        self.__window_shadow_visible(True)

        return QtWidgets.QMainWindow.event_filter(self, watched, event)
