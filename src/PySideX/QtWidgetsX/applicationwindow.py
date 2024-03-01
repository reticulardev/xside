#!/usr/bin/env python3
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

import PySideX.QtWidgetsX.modules.color as color
from PySideX.QtWidgetsX.modules.platform import Platform
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv
from PySideX.QtWidgetsX.modules.dynamicstyle import DynamicStyle
from PySideX.QtWidgetsX.modules.dynamicstyle import StyleParser
from PySideX.QtWidgetsX.modules import texture


class MainWindow(QtWidgets.QFrame):
    """..."""
    def __init__(self, *args, **kwargs):
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)


class Shadow(QtWidgets.QFrame):
    """..."""
    def __init__(self, position: str, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.set_object_name('toplevelwindowshadow')
        self.__shadow_color = 'rgba(0, 0, 0, 20)'
        self.__corner_shadow_color = 'rgba(0, 0, 0, 15)'
        self.__end_color = 'rgba(0, 0, 0, 0)'

        if position == 'top-left':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background:'
                '  qradialgradient('
                '  cx: 0.7, cy: 0.7, radius: 2, fx: 1.0, fy: 1.0,'
                f' stop: 0.0 {self.__corner_shadow_color},'
                f' stop: 0.4 {self.__end_color});'
                '}')

        elif position == 'top':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background: qlineargradient('
                '  x1:0 y1:0, x2:0 y2:1,'
                f' stop:0.0 {self.__end_color},'
                f' stop:1.0 {self.__shadow_color});'
                '}')

        elif position == 'top-right':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background:'
                '  qradialgradient('
                '  cx: 0.3, cy: 0.7, radius: 2, fx: 0.0, fy: 1.0,'
                f' stop: 0.0 {self.__corner_shadow_color},'
                f' stop: 0.4 {self.__end_color});'
                '}')

        elif position == 'left':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background: qlineargradient('
                '  x1:0 y1:0, x2:1 y2:0,'
                f' stop:0.0 {self.__end_color},'
                f' stop:1.0 {self.__shadow_color});'
                '}')

        elif position == 'right':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background: qlineargradient('
                '  x1:0 y1:0, x2:1 y2:0,'
                f' stop:0.0 {self.__shadow_color},'
                f' stop:1.0 {self.__end_color});'
                '}')

        elif position == 'bottom-left':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background:'
                '  qradialgradient('
                '  cx: 0.7, cy: 0.3, radius: 2, fx: 1.0, fy: 0.0,'
                f' stop: 0.0 {self.__corner_shadow_color},'
                f' stop: 0.4 {self.__end_color});'
                '}')

        elif position == 'bottom':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background: qlineargradient('
                '  x1:0 y1:0, x2:0 y2:1,'
                f' stop:0.0 {self.__shadow_color},'
                f' stop:1.0 {self.__end_color});'
                '}')

        elif position == 'bottom-right':
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                'background:'
                '  qradialgradient('
                '  cx: 0.3, cy: 0.3, radius: 2, fx: 0.0, fy: 0.0,'
                f' stop: 0.0 {self.__corner_shadow_color},'
                f' stop: 0.4 {self.__end_color});'
                '}')
        else:
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                f'background-color: {self.__shadow_color};'
                '}')

    def set_background_color_visible(self, visible: bool) -> None:
        if visible:
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                f'background-color: {self.__shadow_color};'
                '}')
        else:
            self.set_style_sheet(
                '#toplevelwindowshadow {'
                f'background-color: {self.__end_color};'
                '}')


class BaseShadowWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.set_contents_margins(0, 0, 0, 0)

        self.__is_shadow_has_removed = False
        self.__is_shadow_has_added = True

        self.__border_radius = (10, 10, 0, 0)
        self.__width = 500
        self.__height = 500
        self.__shadow_size = 8

        self.__mainwidget = QtWidgets.QWidget()
        self.__mainwidget.set_contents_margins(0, 0, 0, 0)
        self.set_central_widget(self.__mainwidget)

        self.__main_box = QtWidgets.QVBoxLayout()
        self.__main_box.set_contents_margins(0, 0, 0, 0)
        self.__main_box.set_spacing(0)
        self.__mainwidget.set_layout(self.__main_box)

        # Top
        self.__top_box = QtWidgets.QHBoxLayout()
        self.__main_box.add_layout(self.__top_box)

        self.__top_left_shadow = Shadow('top-left')
        self.__top_left_shadow.set_fixed_width(self.__shadow_size)
        self.__top_left_shadow.set_fixed_height(self.__shadow_size)
        self.__top_box.add_widget(self.__top_left_shadow)

        self.__top_shadow = Shadow('top')
        self.__top_shadow.set_fixed_height(self.__shadow_size)
        self.__top_box.add_widget(self.__top_shadow)

        self.__top_right_shadow = Shadow('top-right')
        self.__top_right_shadow.set_fixed_width(self.__shadow_size)
        self.__top_right_shadow.set_fixed_height(self.__shadow_size)
        self.__top_box.add_widget(self.__top_right_shadow)

        # Left
        self.__left_center_right_box = QtWidgets.QHBoxLayout()
        self.__main_box.add_layout(self.__left_center_right_box)

        self.__left_shadow = Shadow('left')
        self.__left_shadow.set_fixed_width(self.__shadow_size)
        self.__left_center_right_box.add_widget(self.__left_shadow)

        # Center
        self.__center_shadow = Shadow('center')
        self.__center_shadow.resize(self.__width, self.__height)
        self.__left_center_right_box.add_widget(self.__center_shadow)

        self.__central_widget_box = QtWidgets.QVBoxLayout()
        self.__central_widget_box.set_contents_margins(0, 0, 0, 0)
        self.__central_widget_box.set_spacing(0)
        self.__center_shadow.set_layout(self.__central_widget_box)

        self.__central_widget = MainWindow()
        self.__central_widget_box.add_widget(self.__central_widget)

        # Right
        self.__right_shadow = Shadow('right')
        self.__right_shadow.set_fixed_width(self.__shadow_size)
        self.__left_center_right_box.add_widget(self.__right_shadow)

        # Bottom
        self.__bottom_box = QtWidgets.QHBoxLayout()
        self.__main_box.add_layout(self.__bottom_box)

        self.__bottom_left_shadow = Shadow('bottom-left')
        self.__bottom_left_shadow.set_fixed_width(self.__shadow_size)
        self.__bottom_left_shadow.set_fixed_height(self.__shadow_size)
        self.__bottom_box.add_widget(self.__bottom_left_shadow)

        self.__bottom_shadow = Shadow('bottom')
        self.__bottom_shadow.set_fixed_height(self.__shadow_size)
        self.__bottom_box.add_widget(self.__bottom_shadow)

        self.__bottom_right_shadow = Shadow('bottom-right')
        self.__bottom_right_shadow.set_fixed_width(self.__shadow_size)
        self.__bottom_right_shadow.set_fixed_height(self.__shadow_size)
        self.__bottom_box.add_widget(self.__bottom_right_shadow)

    def central_widget(self) -> QtWidgets:
        """..."""
        return self.__central_widget

    def is_shadow_visible(self) -> bool:
        return self.__is_shadow_has_added

    def set_shadow_as_hidden(self, hide_value: bool) -> None:
        """..."""
        if hide_value:
            self.__center_shadow.set_background_color_visible(False)

            self.__bottom_left_shadow.set_visible(False)
            self.__bottom_shadow.set_visible(False)
            self.__bottom_right_shadow.set_visible(False)

            self.__top_left_shadow.set_visible(False)
            self.__top_shadow.set_visible(False)
            self.__top_right_shadow.set_visible(False)

            self.__left_shadow.set_visible(False)
            self.__right_shadow.set_visible(False)

            self.__is_shadow_has_removed = True
            self.__is_shadow_has_added = False

        else:
            self.__center_shadow.set_background_color_visible(True)

            self.__bottom_left_shadow.set_visible(True)
            self.__bottom_shadow.set_visible(True)
            self.__bottom_right_shadow.set_visible(True)

            self.__top_left_shadow.set_visible(True)
            self.__top_shadow.set_visible(True)
            self.__top_right_shadow.set_visible(True)

            self.__left_shadow.set_visible(True)
            self.__right_shadow.set_visible(True)

            self.__is_shadow_has_added = True
            self.__is_shadow_has_removed = False


class ApplicationWindow(BaseShadowWindow):
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
        self.__follow_platform = follow_platform
        self.__platform = Platform()

        # Flags
        self.__shadow_size = 8
        self.__active_resize_border = None
        self.__default_resize_border_size = 5
        self.__resize_border_size = self.__default_resize_border_size

        self.__gui_env = GuiEnv(
            self.__platform.operational_system(),
            self.__platform.desktop_environment(),
            self.__follow_platform)

        self.__is_dark = color.is_dark(
            self.__gui_env.settings().window_background_color().to_tuple())

        # Layout
        self.__central_widget = self.central_widget()

        # Style
        self.__dynamic_style = DynamicStyle(self)
        self.__style_sheet = self.__dynamic_style.build_style()

        self.__style_parser = StyleParser(self.__style_sheet)
        self.__style_sheet = self.__style_parser.style_sheet()

        self.__texture = texture.Texture(self, self.__style_sheet)
        self.__handle_texture = True

        self.__style_sheet_fullscreen = (
            self.__dynamic_style.fullscreen_adapted_style(
                self.__style_sheet))

        self.__set_window_decoration()

        # Events
        self.install_event_filter(self)

    def follow_platform(self) -> bool:
        """..."""
        return self.__follow_platform

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
            self.__central_widget.set_style_sheet(
                self.__style_sheet_fullscreen)
        else:
            self.__central_widget.set_style_sheet(self.__style_sheet)

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
            self.__central_widget.set_style_sheet(
                self.__style_sheet_fullscreen)
        else:
            self.__central_widget.set_style_sheet(self.__style_sheet)

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

    def __set_edge_position(self, event: QtCore.QEvent) -> None:
        # Saves the position of the window where the mouse cursor is
        resize_area = (
            -3 if self.__is_server_side_decorated else self.__shadow_size - 3)
        pos = event.position().to_point()  # QtGui.QHoverEvent(ev.clone())
        window_area = [
            resize_area < pos.x() < self.width() - resize_area,
            resize_area < pos.y() < self.height() - resize_area]
        if self.__is_server_side_decorated:
            window_area = [
                pos.x() < self.width(), pos.y() < self.height()]

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
        # if self.__shadow_is_disabled:
        if self.__is_server_side_decorated:
            self.__resize_border_size = self.__default_resize_border_size
        else:
            self.set_shadow_as_hidden(False if visible else True)
            if visible:
                self.__resize_border_size = (
                        self.__default_resize_border_size + self.__shadow_size)
            else:
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

            elif event.type() == QtCore.QEvent.HoverEnter:
                # if self.__handle_texture:
                #     self.__texture.apply_texture()
                pass

            elif event.type() == QtCore.QEvent.HoverLeave:
                if self.__handle_texture:
                    self.__texture.remove_texture()

            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self.__update_cursor_shape()
                if self.__active_resize_border:
                    self.window_handle().start_system_resize(
                        self.__active_resize_border)

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.set_cursor(QtCore.Qt.CursorShape.ArrowCursor)
                if self.__handle_texture:
                    self.__texture.apply_texture()

            elif event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(0)
                if self.__handle_texture:
                    self.__texture.remove_texture()

                if self.is_maximized() or self.is_full_screen():
                    self.__central_widget.set_style_sheet(
                        self.__style_sheet_fullscreen)

                    self.__window_shadow_visible(False)
                    if self.__handle_texture:
                        self.__texture.apply_texture()
                else:
                    self.__central_widget.set_style_sheet(self.__style_sheet)

                    if not self.__is_server_side_decorated:
                        self.__window_shadow_visible(True)

        return QtWidgets.QMainWindow.event_filter(self, watched, event)
