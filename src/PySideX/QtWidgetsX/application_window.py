#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

import PySideX.platform.settings as settings


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
            self, is_decorated: bool = False, platform: bool = True,
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        self.__is_decorated = is_decorated
        self.__platform_settings = settings.Settings(platform)

        self.__resize_corner_active = None
        self.__resize_corner_size_default = 5
        self.__resize_corner_size = self.__resize_corner_size_default

        self.__shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.__shadow_size = 5
        self.__shadow_is_disabled = self.__is_decorated

        self.__style_builder = settings.StyleBuilder(self)
        self.__style_sheet = self.__style_builder.build_style()
        self.__style_sheet_fullscreen = (
            self.__style_builder.adapt_to_fullscreen(self.__style_sheet))

        self.__central_widget = QtWidgets.QWidget()
        self.__configure_window()

    def central_widget(self) -> QtWidgets.QWidget:
        """Returns the central widget for the main window

        This function returns None if the central widget has not been set.
        """
        return self.__central_widget

    def is_decorated(self) -> bool:
        """..."""
        return self.__is_decorated

    def platform_settings(self) -> settings.Settings:
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

        if self.__is_decorated:
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

    def __configure_window(self) -> None:
        # Layout
        self.set_central_widget(self.__central_widget)
        self.__central_widget.set_object_name('QApplicationWindow')

        # Decorations
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        if not self.__is_decorated:
            self.set_window_flags(
                QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        else:
            self.__shadow_is_disabled = True

        # Shadow
        self.__shadow_effect.set_blur_radius(self.__shadow_size)
        self.__shadow_effect.set_offset(QtCore.QPointF(0.0, 0.0))
        if self.__platform_settings.is_dark_widget(self):
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 180))
        else:
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 90))
        self.__central_widget.set_graphics_effect(self.__shadow_effect)
        self.__shadow_visible(True)

        # Filter
        self.install_event_filter(self)

    def __set_decoration(self) -> None:
        # ...
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        if not self.__is_decorated:
            self.set_window_flags(
                QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
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
            if (pos.x() > (self.width() - self.__resize_corner_size) and
                    pos.y() < self.__resize_corner_size):
                self.__resize_corner_active = (
                        QtCore.Qt.Edge.RightEdge | QtCore.Qt.Edge.TopEdge)
            elif (pos.x() < self.__resize_corner_size and
                  pos.y() < self.__resize_corner_size):
                self.__resize_corner_active = (
                        QtCore.Qt.Edge.LeftEdge | QtCore.Qt.Edge.TopEdge)
            elif (pos.x() > (self.width() - self.__resize_corner_size) and
                  pos.y() > (self.height() - self.__resize_corner_size)):
                self.__resize_corner_active = (
                        QtCore.Qt.Edge.RightEdge | QtCore.Qt.Edge.BottomEdge)
            elif (pos.x() < self.__resize_corner_size and
                  pos.y() > (self.height() - self.__resize_corner_size)):
                self.__resize_corner_active = (
                        QtCore.Qt.Edge.LeftEdge | QtCore.Qt.Edge.BottomEdge)

            # left, right, top, bottom
            elif pos.x() <= self.__resize_corner_size:
                self.__resize_corner_active = QtCore.Qt.Edge.LeftEdge
            elif pos.x() >= (self.width() - self.__resize_corner_size):
                self.__resize_corner_active = QtCore.Qt.Edge.RightEdge
            elif pos.y() <= self.__resize_corner_size:
                self.__resize_corner_active = QtCore.Qt.Edge.TopEdge
            elif pos.y() >= (self.height() - self.__resize_corner_size):
                self.__resize_corner_active = QtCore.Qt.Edge.BottomEdge
            else:
                self.__resize_corner_active = None
        else:
            self.__resize_corner_active = None

    def __shadow_visible(self, visible: bool = True) -> None:
        if self.__shadow_is_disabled:
            self.__resize_corner_size = self.__resize_corner_size_default
        else:
            if visible:
                self.set_contents_margins(
                    self.__shadow_size, self.__shadow_size,
                    self.__shadow_size, self.__shadow_size)
                self.__resize_corner_size = (
                        self.__resize_corner_size_default + self.__shadow_size)
            else:
                self.set_contents_margins(0, 0, 0, 0)
                self.__resize_corner_size = self.__resize_corner_size_default

    def __update_cursor(self) -> None:
        # Updates the mouse cursor appearance
        if not self.__resize_corner_active:
            self.set_cursor(QtCore.Qt.CursorShape.ArrowCursor)
        else:
            if (self.__resize_corner_active == QtCore.Qt.Edge.LeftEdge or
                    self.__resize_corner_active == QtCore.Qt.Edge.RightEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeHorCursor)

            elif (self.__resize_corner_active == QtCore.Qt.Edge.TopEdge or
                  self.__resize_corner_active == QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeVerCursor)

            elif (self.__resize_corner_active == QtCore.Qt.Edge.LeftEdge |
                  QtCore.Qt.Edge.TopEdge or
                  self.__resize_corner_active == QtCore.Qt.Edge.RightEdge |
                  QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeFDiagCursor)

            elif (self.__resize_corner_active == QtCore.Qt.Edge.RightEdge |
                  QtCore.Qt.Edge.TopEdge or
                  self.__resize_corner_active == QtCore.Qt.Edge.LeftEdge |
                  QtCore.Qt.Edge.BottomEdge):
                self.set_cursor(QtCore.Qt.CursorShape.SizeBDiagCursor)

    @staticmethod
    def __variant_icon_theme() -> tuple:
        # ...
        theme_name = QtGui.QIcon.theme_name()
        variant_theme_name = None
        variant_theme_path = None

        icon_theme_is_dark = False
        if 'dark' in theme_name.lower():
            icon_theme_is_dark = True

        variant = 'dark'
        if icon_theme_is_dark:
            variant = 'light'

        for path_dirs in QtGui.QIcon.theme_search_paths():
            if os.path.isdir(path_dirs):
                for dire in os.listdir(path_dirs):

                    if variant == 'dark':
                        if theme_name in dire and 'dark' in dire.lower():
                            variant_theme_name = dire
                            variant_theme_path = os.path.join(path_dirs, dire)
                    else:
                        name = theme_name.replace(
                            '-Dark', '').replace('-dark', '').replace(
                            '-DARK', '').replace('Dark', '').replace(
                            'dark', '').replace('DARK', '')
                        if 'dark' not in dire.lower() and name in dire:
                            variant_theme_name = dire
                            variant_theme_path = os.path.join(path_dirs, dire)

        return variant_theme_name, variant_theme_path

    def event_filter(
            self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        self.event_filter_signal.emit(event)

        if self.__is_decorated:
            self.__central_widget.set_style_sheet(self.__style_sheet)
            if event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(event)
        else:
            if event.type() == QtCore.QEvent.HoverMove:
                self.__set_edge_position(event)
                self.__update_cursor()

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self.__update_cursor()
                if self.__resize_corner_active:
                    self.window_handle().start_system_resize(
                        self.__resize_corner_active)

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.set_cursor(QtCore.Qt.CursorShape.ArrowCursor)

            elif event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(0)

                if self.is_maximized() or self.is_full_screen():
                    self.__central_widget.set_style_sheet(
                        self.__style_sheet_fullscreen)
                    self.__shadow_visible(False)
                else:
                    self.__central_widget.set_style_sheet(self.__style_sheet)
                    self.__shadow_visible(True)

        return QtWidgets.QMainWindow.event_filter(self, watched, event)
