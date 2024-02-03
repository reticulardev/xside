#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.platform.platformsettings import PlatformSettings
from PySideX.platform.stylebuilder import StyleBuilder


class QApplicationWindow(QtWidgets.QMainWindow):
    """Application main window prepared to use CSD

    The edges are rounded and there is no title bar. A custom header bar can
    be added
    """
    event_filter_signal = QtCore.Signal(object)
    reset_style_signal = QtCore.Signal(object)
    resize_event_signal = QtCore.Signal(object)
    set_style_signal = QtCore.Signal(object)

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
        self.__platform_settings = PlatformSettings(follow_platform)

        # Flags
        self.__shadow_size = 5
        self.__shadow_is_disabled = self.__is_server_side_decorated
        self.__active_resize_border = None
        self.__default_resize_border_size = 5
        self.__resize_border_size = self.__default_resize_border_size

        # Layout
        self.__central_widget = QtWidgets.QWidget()
        self.set_central_widget(self.__central_widget)
        self.__central_widget.set_object_name('QApplicationWindow')

        # Style
        self.__style_builder = StyleBuilder(self)
        self.__style_sheet = self.__style_builder.build_style()
        self.__style_sheet_fullscreen = (
            self.__style_builder.adapt_to_fullscreen(self.__style_sheet))

        self.__shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.__shadow_effect.set_blur_radius(self.__shadow_size)
        self.__shadow_effect.set_offset(QtCore.QPointF(0.0, 0.0))
        self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 90))

        self.__set_window_decoration()

        # Events
        self.install_event_filter(self)

    def central_widget(self) -> QtWidgets.QWidget:
        """Returns the central widget for the main window

        This function returns None if the central widget has not been set.
        """
        return self.__central_widget

    def is_server_side_decorated(self) -> bool:
        """..."""
        return self.__is_server_side_decorated

    def platform_settings(self) -> PlatformSettings:
        """..."""
        return self.__platform_settings

    def reset_style(self) -> None:
        """Reset the application style sheet to default"""
        self.__reset_style_properties()

        if self.is_maximized() or self.is_full_screen():
            self.__central_widget.set_style_sheet(
                self.__style_sheet_fullscreen)
        else:
            self.__central_widget.set_style_sheet(self.__style_sheet)
        self.reset_style_signal.emit(0)

    def set_shadow_size(self, size: int) -> None:
        """..."""
        self.__shadow_size = size

    def set_style_sheet(self, style: str) -> None:
        """Set the application style sheet

        See the documentation about the 'qss' style at:
        doc.qt.io/qtforpython-6/tutorials/basictutorial/widgetstyling.html

        :param style: string containing 'qss' style
        """
        if 'QApplicationWindow' in style:
            if '#QApplicationWindow' not in style:
                style = style.replace(
                    'QApplicationWindow', '#QApplicationWindow')

        self.__reset_style_properties()
        self.__style_sheet += style

        self.__style_sheet_fullscreen = (
            self.__style_builder.adapt_to_fullscreen(self.__style_sheet))

        if self.__is_server_side_decorated:
            self.__style_sheet = self.__style_sheet_fullscreen

        if self.is_maximized() or self.is_full_screen():
            self.__central_widget.set_style_sheet(
                self.__style_sheet_fullscreen)
        else:
            self.__central_widget.set_style_sheet(
                self.__style_sheet)

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
        self.__style_sheet = self.__style_builder.build_style()
        self.__style_sheet_fullscreen = (
            self.__style_builder.adapt_to_fullscreen(self.__style_sheet))

    def __set_window_decoration(self) -> None:
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        if not self.__is_server_side_decorated:
            self.set_window_flags(
                QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
            self.__window_shadow_visible(True)
        else:
            self.__shadow_is_disabled = True

    def __set_edge_position(self, event: QtCore.QEvent) -> None:
        # Saves the position of the window where the mouse cursor is
        pos = event.position().to_point()  # QtGui.QHoverEvent(ev.clone())
        window_area = [
            self.__shadow_size < pos.x() < self.width() - self.__shadow_size,
            self.__shadow_size < pos.y() < self.height() - self.__shadow_size]
        if self.__shadow_is_disabled:
            window_area = [pos.x() < self.width(), pos.y() < self.height()]

        if all(window_area):
            # top-right, top-left, bottom-right, bottom-left
            if (pos.x() > (self.width() - self.__resize_border_size) and
                    pos.y() < self.__resize_border_size):
                self.__active_resize_border = (
                        QtCore.Qt.Edge.RightEdge | QtCore.Qt.Edge.TopEdge)
            elif (pos.x() < self.__resize_border_size and
                  pos.y() < self.__resize_border_size):
                self.__active_resize_border = (
                        QtCore.Qt.Edge.LeftEdge | QtCore.Qt.Edge.TopEdge)
            elif (pos.x() > (self.width() - self.__resize_border_size) and
                  pos.y() > (self.height() - self.__resize_border_size)):
                self.__active_resize_border = (
                        QtCore.Qt.Edge.RightEdge | QtCore.Qt.Edge.BottomEdge)
            elif (pos.x() < self.__resize_border_size and
                  pos.y() > (self.height() - self.__resize_border_size)):
                self.__active_resize_border = (
                        QtCore.Qt.Edge.LeftEdge | QtCore.Qt.Edge.BottomEdge)

            # left, right, top, bottom
            elif pos.x() <= self.__resize_border_size:
                self.__active_resize_border = QtCore.Qt.Edge.LeftEdge
            elif pos.x() >= (self.width() - self.__resize_border_size):
                self.__active_resize_border = QtCore.Qt.Edge.RightEdge
            elif pos.y() <= self.__resize_border_size:
                self.__active_resize_border = QtCore.Qt.Edge.TopEdge
            elif pos.y() >= (self.height() - self.__resize_border_size):
                self.__active_resize_border = QtCore.Qt.Edge.BottomEdge
            else:
                self.__active_resize_border = None
        else:
            self.__active_resize_border = None

    def __window_shadow_visible(self, visible: bool) -> None:
        if self.__shadow_is_disabled:
            self.__resize_border_size = self.__default_resize_border_size
        else:
            if visible:
                if self.__platform_settings.is_dark_widget(self):
                    self.__shadow_effect.set_color(
                        QtGui.QColor(10, 10, 10, 180))

                self.set_contents_margins(
                    self.__shadow_size, self.__shadow_size,
                    self.__shadow_size, self.__shadow_size)

                self.__resize_border_size = (
                        self.__default_resize_border_size + self.__shadow_size)

                self.__central_widget.set_graphics_effect(self.__shadow_effect)
            else:
                self.set_contents_margins(0, 0, 0, 0)
                self.__resize_border_size = self.__default_resize_border_size

    def __update_cursor_shape(self) -> None:
        # Updates the mouse cursor appearance
        if not self.__active_resize_border:
            self.set_cursor(QtCore.Qt.CursorShape.ArrowCursor)
        else:
            if (self.__active_resize_border == QtCore.Qt.Edge.LeftEdge or
                    self.__active_resize_border == QtCore.Qt.Edge.RightEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeHorCursor)

            elif (self.__active_resize_border == QtCore.Qt.Edge.TopEdge or
                  self.__active_resize_border == QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeVerCursor)

            elif (self.__active_resize_border == QtCore.Qt.Edge.LeftEdge |
                  QtCore.Qt.Edge.TopEdge or
                  self.__active_resize_border == QtCore.Qt.Edge.RightEdge |
                  QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeFDiagCursor)

            elif (self.__active_resize_border == QtCore.Qt.Edge.RightEdge |
                  QtCore.Qt.Edge.TopEdge or
                  self.__active_resize_border == QtCore.Qt.Edge.LeftEdge |
                  QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeBDiagCursor)

    def event_filter(
            self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        self.event_filter_signal.emit(event)

        if self.__is_server_side_decorated:
            self.__central_widget.set_style_sheet(self.__style_sheet)
            if event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(event)
        else:
            if event.type() == QtCore.QEvent.HoverMove:
                self.__set_edge_position(event)
                self.__update_cursor_shape()

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self.__update_cursor_shape()
                if self.__active_resize_border:
                    self.window_handle().start_system_resize(
                        self.__active_resize_border)

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.set_cursor(QtCore.Qt.CursorShape.ArrowCursor)

            elif event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(0)

                if self.is_maximized() or self.is_full_screen():
                    self.__central_widget.set_style_sheet(
                        self.__style_sheet_fullscreen)
                    self.__window_shadow_visible(False)
                else:
                    self.__central_widget.set_style_sheet(self.__style_sheet)
                    self.__window_shadow_visible(True)

        return QtWidgets.QMainWindow.event_filter(self, watched, event)
