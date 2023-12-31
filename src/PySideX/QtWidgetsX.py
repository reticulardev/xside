#!/usr/bin/env python3
import logging
import math
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

import PySideX.platform.integration as integration


class QApplicationWindow(QtWidgets.QMainWindow):
    """Application main window prepared to use CSD

    The edges are rounded and there is no title bar. A custom header bar can
    be added
    """
    resize_event_signal = QtCore.Signal(object)

    def __init__(
            self, is_decorated: bool = False, platform: bool = True,
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        self.__is_decorated = is_decorated
        self.__platform_settings = integration.PlatformSettings(platform)

        self.__resize_corner_active = None
        self.__resize_corner_size_default = 5
        self.__resize_corner_size = self.__resize_corner_size_default

        self.__shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.__shadow_size = 5
        self.__shadow_is_disabled = self.__is_decorated

        self.__style_builder = integration.StyleBuilder(self)
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

    def platform_settings(self) -> integration.PlatformSettings:
        """..."""
        return self.__platform_settings

    def style_sheet(self) -> str:
        """The application style sheet

        :return: string containing 'qss' style
        """
        return self.__style_sheet

    def reset_style(self) -> None:
        """Reset the application style sheet to default"""
        self.__reset_style_properties()

        if self.is_maximized() or self.is_full_screen():
            self.__central_widget.set_style_sheet(
                self.__style_sheet_fullscreen)
        else:
            self.__central_widget.set_style_sheet(self.__style_sheet)

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
        self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 180))
        self.__central_widget.set_graphics_effect(self.__shadow_effect)
        self.__set_visible_shadow(True)

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

    def __set_visible_shadow(self, visible: bool = True) -> None:
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

    def event_filter(
            self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if self.__is_decorated:
            self.__central_widget.set_style_sheet(self.__style_sheet)
            if event.type() == QtCore.QEvent.Resize:
                self.resize_event_signal.emit(0)
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
                    self.__set_visible_shadow(False)
                else:
                    self.__central_widget.set_style_sheet(self.__style_sheet)
                    self.__set_visible_shadow(True)

        return QtWidgets.QMainWindow.event_filter(self, watched, event)


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
        if self.__button_id not in (0, 1, 2):
            raise ValueError(
                'The value must be 0, 1 or 2. The values represent "minimize",'
                ' "maximize" and "close" buttons respectively.')

        if self.__button_id == 0:
            style = (
                self.__main_window.platform_settings()
                .window_control_button_style(
                    self.__is_dark(), 'minimize', 'normal'))

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(QtGui.QIcon.from_theme('go-down'))

            self.clicked.connect(
                lambda _: self.__main_window.show_minimized())

        elif self.__button_id == 1:
            style = (
                self.__main_window.platform_settings()
                .window_control_button_style(
                    self.__is_dark(), 'maximize', 'normal'))

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(QtGui.QIcon.from_theme('go-up'))
        else:
            style = (
                self.__main_window.platform_settings()
                .window_control_button_style(
                    self.__is_dark(), 'close', 'normal'))

            self.set_style_sheet(style)
            if 'background: url' not in style:
                self.set_icon(QtGui.QIcon.from_theme('edit-delete-remove'))

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
                .window_control_button_style(
                    self.__is_dark(),
                    self.__maximize_or_restore_icon, 'normal'))

            self.set_style_sheet(maximize_style)
            if self.__maximize_or_restore_icon == 'restore':
                if 'background: url' not in maximize_style:
                    self.set_icon(QtGui.QIcon.from_theme('window-restore'))
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
                .window_control_button_style(
                    self.__is_dark(),
                    self.__maximize_or_restore_icon, 'hover'))
        else:
            self.set_style_sheet(
                self.__main_window.platform_settings()
                .window_control_button_style(
                    self.__is_dark(),
                    self.__buttons_schema[self.__button_id], 'hover'))

        logging.info(event)
        self.enter_event_signal.emit(self)

    def leave_event(self, event: QtGui.QEnterEvent) -> None:
        if self.__button_id == 1:
            self.set_style_sheet(
                self.__main_window.platform_settings()
                .window_control_button_style(
                    self.__is_dark(),
                    self.__maximize_or_restore_icon, 'normal'))
        else:
            self.set_style_sheet(
                self.__main_window.platform_settings()
                .window_control_button_style(
                    self.__is_dark(),
                    self.__buttons_schema[self.__button_id], 'normal'))

        logging.info(event)
        self.leave_event_signal.emit(self)


class QWindowControlButtons(QtWidgets.QFrame):
    """window control buttons

    Contains minimize, maximize and close buttons
    """

    def __init__(
            self, main_window: QtWidgets, button_order: tuple = (0, 1, 2),
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes.
        In the button order parameter, each number represents a type of button:
            0 is the minimize button
            1 is the maximize button
            2 is the close button
            3 is window icon

        :param main_window: Main window instance
        :param button_order:
            Tuple with the order of the buttons. Default is (0, 1, 2).
        """
        super().__init__(*args, **kwargs)

        self.__main_window = main_window
        self.__button_order = button_order

        self.__window_icon = QtWidgets.QLabel()
        self.__window_icon.set_pixmap(
            self.__main_window.window_icon().pixmap(20))

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.set_contents_margins(2, 0, 2, 0)

        self.__minimize_button = QControlButton(self.__main_window, 0)
        self.__maximize_button = QControlButton(self.__main_window, 1)
        self.__close_button = QControlButton(self.__main_window, 2)

        self.__set_buttons_order()

    def __set_buttons_order(self) -> None:
        # Add the buttons in the configured order
        buttons_dict = {
            0: self.__minimize_button,
            1: self.__maximize_button,
            2: self.__close_button,
            3: self.__window_icon}
        if self.__button_order:
            for index in self.__button_order:
                self.__layout.add_widget(buttons_dict[index])


class QWindowMoveArea(QtWidgets.QFrame):
    """Window move area"""
    mouse_press_event_signal = QtCore.Signal(object)
    mouse_double_click_event_signal = QtCore.Signal(object)

    def __init__(
            self, main_window: QtWidgets, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param main_window: QApplicationWindow app main window instance
        """
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.__default_style = integration.StyleBuilder(self.__main_window)

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.set_contents_margins(0, 0, 0, 0)

    def mouse_press_event(self, event: QtGui.QMouseEvent) -> None:
        """This method has changed.
        Instead, use the 'mouse_press_event_signal' sign

        Such as:
        self.my_window.mouse_press_event_signal.connect(
            self.my_mouse_press_event_method)
        """
        self.mouse_press_event_signal.emit(event)
        if not self.__main_window.is_decorated():
            if event.button() == QtCore.Qt.LeftButton and self.under_mouse():
                self.__main_window.window_handle().start_system_move()

    def mouse_double_click_event(self, event: QtGui.QMouseEvent) -> None:
        """This method has changed.
        Instead, use the 'mouse_double_click_event_signal' sign

        Such as:
        self.my_window.mouse_double_click_event_signal.connect(
            self.my_mouse_double_click_event_method)
        """
        self.mouse_double_click_event_signal.emit(event)
        if event.button() == QtCore.Qt.LeftButton:
            if self.__main_window.is_maximized():
                self.native_parent_widget().show_normal()
            elif self.__main_window.is_full_screen():
                self.native_parent_widget().show_maximized()
            else:
                self.native_parent_widget().show_maximized()


class QHeaderBar(QtWidgets.QFrame):
    """Window header bar

    Replaces traditional title bar and allows adding and editing widgets
    """

    def __init__(self, main_window: QtWidgets, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param main_window: QApplicationWindow app main window instance
        :param window_control_buttons_on_left:
            window control buttons (minimize, maximize and close) on left
        :param window_control_buttons_order:
            Tuple with the order of the buttons. 0 is the minimize button, 1 is
            the maximize button and 2 is the close button. Default is (0, 1, 2)
        """
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.__left_ctrl_buttons_visibility = True
        self.__right_ctrl_buttons_visibility = True
        self.__window_control_buttons_order = (
            self.__main_window.platform_settings()
            .window_control_button_order())

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.set_contents_margins(4, 4, 4, 4)
        self.__layout.set_spacing(6)

        self.__bar_item_layout_left = QtWidgets.QHBoxLayout()
        self.__bar_item_layout_left.set_contents_margins(0, 0, 0, 0)
        self.__layout.add_layout(self.__bar_item_layout_left)

        self.__window_icon = QtWidgets.QLabel()
        self.__window_icon.set_pixmap(
            self.__main_window.window_icon().pixmap(20))

        self.__left_layout = QtWidgets.QHBoxLayout()
        self.__left_layout.set_contents_margins(0, 0, 0, 0)
        self.__layout.add_layout(self.__left_layout)

        self.__bar_item_layout_center = QtWidgets.QHBoxLayout()
        self.__bar_item_layout_center.set_contents_margins(0, 0, 0, 0)
        self.__layout.add_layout(self.__bar_item_layout_center)

        self.__window_move_area = QWindowMoveArea(self.__main_window)
        self.__bar_item_layout_center.add_widget(self.__window_move_area, 9)

        self.__window_move_area_text = QtWidgets.QLabel()
        self.__window_move_area_text.set_alignment(QtCore.Qt.AlignLeft)
        self.__window_move_area.layout().add_widget(
            self.__window_move_area_text)

        self.__right_layout = QtWidgets.QHBoxLayout()
        self.__right_layout.set_contents_margins(0, 0, 0, 0)
        self.__layout.add_layout(self.__right_layout)

        self.__bar_item_layout_right = QtWidgets.QHBoxLayout()
        self.__bar_item_layout_right.set_contents_margins(0, 0, 0, 0)
        self.__layout.add_layout(self.__bar_item_layout_right)

        self.__left_ctrl_buttons = QWindowControlButtons(
            self.__main_window,
            self.__window_control_buttons_order[0])
        self.__bar_item_layout_left.add_widget(self.__left_ctrl_buttons)

        self.__right_ctrl_buttons = QWindowControlButtons(
            self.__main_window,
            self.__window_control_buttons_order[1])
        self.__bar_item_layout_right.add_widget(self.__right_ctrl_buttons)

    def text(self) -> str:
        """Get the QWindowMoveArea's text

        The text shown in the center of the QWindowMoveArea
        """
        return self.__window_move_area.text()

    def set_text(self, text: str) -> None:
        """Sets a text in the center

        :param text: The text to be shown in the center of the QWindowMoveArea
        """
        if not self.__main_window.is_decorated():
            self.__window_move_area_text.set_text(text)

    def lef_layout(self) -> QtWidgets.QHBoxLayout:
        """QHBoxLayout on left

        Gets the QHBoxLayout of the widgets that are on the left of the
        QHeaderBar
        """
        return self.__left_layout

    def right_layout(self) -> QtWidgets.QHBoxLayout:
        """QHBoxLayout on right

        Gets the QHBoxLayout of the widgets that are on the right of the
        QHeaderBar
        """
        return self.__right_layout

    def add_widget_to_left(self, widget: QtWidgets.QWidget) -> None:
        """..."""
        self.__left_layout.add_widget(widget)

    def add_widget_to_right(self, widget: QtWidgets.QWidget) -> None:
        """..."""
        self.__right_layout.add_widget(widget)

    def set_left_control_buttons_visible(self, visible: bool) -> None:
        self.__left_ctrl_buttons_visibility = visible
        self.__left_ctrl_buttons.set_visible(visible)

    def set_right_control_buttons_visible(self, visible: bool) -> None:
        self.__right_ctrl_buttons_visibility = visible
        self.__right_ctrl_buttons.set_visible(visible)

    def resize_event(self, event: QtGui.QResizeEvent) -> None:
        """..."""
        if self.__main_window.is_decorated():
            self.__left_ctrl_buttons.set_visible(False)
            self.__right_ctrl_buttons.set_visible(False)
            _50_percent_left = self.__50_percent_left_size(True)
        else:
            _50_percent_left = self.__50_percent_left_size(False)

            if self.__main_window.is_maximized():
                if (self.__main_window.platform_settings()
                        .window_use_global_menu()):
                    self.__left_ctrl_buttons.set_visible(False)
                    self.__right_ctrl_buttons.set_visible(False)
                    _50_percent_left = self.__50_percent_left_size(True)

            elif self.__main_window.is_full_screen():
                self.__left_ctrl_buttons.set_visible(False)
                self.__right_ctrl_buttons.set_visible(False)
                _50_percent_left = self.__50_percent_left_size(True)
            else:
                if self.__left_ctrl_buttons_visibility:
                    self.__left_ctrl_buttons.set_visible(True)
                if self.__right_ctrl_buttons_visibility:
                    self.__right_ctrl_buttons.set_visible(True)
                _50_percent_left = self.__50_percent_left_size(False)

        text_size = self.__window_move_area_text.font_metrics().bounding_rect(
            self.__window_move_area_text.text()).width()
        margin_left_size = (
            (self.width() // 2) - _50_percent_left - (text_size // 2))

        if ((margin_left_size + text_size + self.__layout.spacing()) >
                self.__window_move_area.width()):
            self.__window_move_area_text.set_alignment(QtCore.Qt.AlignRight)
            self.__window_move_area_text.set_style_sheet(
                f'margin-left: 0px;')
        else:
            self.__window_move_area_text.set_alignment(QtCore.Qt.AlignLeft)
            if margin_left_size > 0:
                self.__window_move_area_text.set_style_sheet(
                    f'margin-left: {margin_left_size}px;')
            else:
                self.__window_move_area_text.set_style_sheet(
                    f'margin-left: 0px;')

        logging.info(event)

    def __50_percent_left_size(self, hidden_sides: bool) -> int:
        # ...
        if hidden_sides or not self.__left_ctrl_buttons_visibility:
            return (
                (self.__layout.spacing() * 2) +
                self.__left_layout.geometry().width())
        else:
            return (
                self.__left_ctrl_buttons.width() +
                (self.__layout.spacing() * 2) +
                self.__left_layout.geometry().width())
