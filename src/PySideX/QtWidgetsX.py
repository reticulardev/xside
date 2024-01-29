#!/usr/bin/env python3
import logging
import math
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

import PySideX.platform.settings as settings

SRC_DIR = os.path.dirname(os.path.abspath(__file__))


class QQuickContextSeparator(QtWidgets.QFrame):
    """..."""
    def __init__(self, top_level: QtWidgets, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__top_level = top_level
        self.__bd_color = self.__top_level.palette().color(
            QtGui.QPalette.Window.Mid)

        self.set_frame_shape(QtWidgets.QFrame.HLine)
        self.set_frame_shadow(QtWidgets.QFrame.Plain)
        self.set_line_width(0)
        self.set_mid_line_width(3)
        self.set_contents_margins(0, 0, 0, 0)
        self.set_color(color=QtGui.QColor(self.__bd_color))

    def set_color(self, color: QtGui.QColor) -> None:
        """..."""
        palette = self.palette()
        palette.set_color(QtGui.QPalette.WindowText, color)
        self.set_palette(palette)


class QQuickContextMenuButton(QtWidgets.QFrame):
    """..."""
    def __init__(
            self,
            parent_window: QtWidgets,
            parent_context_menu: QtWidgets,
            text: str,
            receiver: callable,
            icon: QtGui.QIcon | None = None,
            shortcut: QtGui.QKeySequence | None = None,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.set_contents_margins(0, 0, 0, 0)

        self.__parent_window = parent_window
        self.__parent = parent_context_menu
        self.__text = text
        self.__receiver = receiver
        self.__icon = icon
        self.__shortcut = shortcut

        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_spacing(0)
        self.set_layout(self.__main_layout)

        self.__left_layout = QtWidgets.QHBoxLayout()
        self.__left_layout.set_alignment(QtCore.Qt.AlignLeft)
        self.__main_layout.add_layout(self.__left_layout)

        if not self.__icon:
            dark = (
                '-symbolic' if
                self.__parent_window.platform_settings().is_dark(self) else '')
            icon_path = os.path.join(
                SRC_DIR, 'platform', 'static', f'context-menu-item{dark}.svg')
            self.__icon = QtGui.QIcon(QtGui.QPixmap(icon_path))

        icon_label = QtWidgets.QLabel()
        icon_label.set_pixmap(self.__icon.pixmap(QtCore.QSize(16, 16)))
        icon_label.set_contents_margins(0, 0, 5, 0)
        icon_label.set_alignment(QtCore.Qt.AlignLeft)
        self.__left_layout.add_widget(icon_label)

        text_label = QtWidgets.QLabel(self.__text)
        text_label.set_alignment(QtCore.Qt.AlignLeft)
        self.__left_layout.add_widget(text_label)

        txt_shortcut = self.__shortcut.to_string() if self.__shortcut else ' '
        shortcut_label = QtWidgets.QLabel(txt_shortcut)
        shortcut_label.set_enabled(False)
        shortcut_label.set_contents_margins(20, 0, 0, 0)
        shortcut_label.set_alignment(QtCore.Qt.AlignRight)
        self.__main_layout.add_widget(shortcut_label)

    def text(self) -> str:
        """..."""
        return self.__text

    def mouse_press_event(self, event):
        """..."""
        logging.info(event)
        self.__receiver()
        self.__parent.close()


class QQuickContextMenu(QtWidgets.QWidget):
    """..."""
    def __init__(self, main_window: QtWidgets, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.__main_window = main_window
        self.set_minimum_width(50)
        self.set_minimum_height(35)

        self.__separator_layouts = []
        self.__context_buttons_layout = []
        self.__context_buttons = []

        self.__style_saved = None
        self.__point_x = None
        self.__point_y = None

        self.__spacing = self.__main_window.platform_settings(
            ).gui_env.context_menu_spacing()
        self.__left_margin = self.__main_window.platform_settings(
            ).gui_env.context_menu_padding()
        self.__top_margin = self.__main_window.platform_settings(
            ).gui_env.context_menu_padding()
        self.__right_margin = self.__main_window.platform_settings(
            ).gui_env.context_menu_padding()
        self.__bottom_margin = self.__main_window.platform_settings(
            ).gui_env.context_menu_padding()
        
        # Main
        self.set_contents_margins(0, 0, 0, 0)
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(5, 5, 5, 5)
        self.__main_layout.set_spacing(0)
        self.set_layout(self.__main_layout)

        self.__main_widget = QtWidgets.QWidget()
        self.__main_widget.set_object_name('QQuickContextMenu')
        self.__main_layout.add_widget(self.__main_widget)

        # Layout
        self.__menu_context_layout = QtWidgets.QVBoxLayout()
        self.__menu_context_layout.set_contents_margins(
            0, self.__top_margin, 0, self.__bottom_margin)
        self.__menu_context_layout.set_spacing(0)
        self.__main_widget.set_layout(self.__menu_context_layout)

        # Shadow
        self.__shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.__shadow_effect.set_blur_radius(5)
        self.__shadow_effect.set_offset(QtCore.QPointF(0.0, 0.0))
        if self.__main_window.platform_settings().is_dark(self):
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 100))
        else:
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 70))
        self.__main_widget.set_graphics_effect(self.__shadow_effect)

        self.__main_window.set_style_signal.connect(self.__set_style_signal)
        self.__main_window.reset_style_signal.connect(self.__set_style_signal)

    def add_action(
            self,
            text: str,
            receiver: callable,
            icon: QtGui.QIcon | None = None,
            shortcut: QtGui.QKeySequence | None = None) -> None:
        """..."""
        ctx_btn_l = QtWidgets.QHBoxLayout()
        ctx_btn_l.set_contents_margins(
            self.__left_margin, 0, self.__right_margin, 0)

        if self.__context_buttons_layout:
            self.__context_buttons_layout[-1].set_contents_margins(
                self.__left_margin, 0, self.__right_margin, self.__spacing)

        ctx_btn = QQuickContextMenuButton(
            self.__main_window, self, text, receiver, icon, shortcut)
        ctx_btn.set_style_sheet(self.__style_saved)
        ctx_btn_l.add_widget(ctx_btn)

        self.__menu_context_layout.add_layout(ctx_btn_l)

        self.__context_buttons_layout.append(ctx_btn_l)
        self.__context_buttons.append(ctx_btn)

    def add_separator(self) -> None:
        """..."""
        separator_layout = QtWidgets.QVBoxLayout()

        margin = self.__main_window.platform_settings(
            ).gui_env.context_menu_separator_margin()
        separator_layout.set_contents_margins(
            margin[0], margin[1], margin[2], margin[3] + self.__spacing)

        separator = QQuickContextSeparator(self.__main_window)
        separator_layout.add_widget(separator)
        
        self.__menu_context_layout.add_layout(separator_layout)
        self.__separator_layouts.append(separator_layout)

    def exec(self, point: QtCore.QPoint) -> None:
        """..."""
        self.__point_x = point.x()
        self.__point_y = point.y()

        self.__main_widget.set_style_sheet(self.__style())
        for btn in self.__context_buttons:
            btn.set_style_sheet(self.__style_saved)

        self.move(self.__point_x - 5, self.__point_y - 5)
        self.show()
        self.__set_dynamic_positioning()

    def mouse_press_event(self, event: QtGui.QMouseEvent) -> None:
        """..."""
        logging.info(event)
        self.close()

    def set_contents_paddings(
            self, left: int, top: int, right: int, bottom: int) -> None:
        """..."""
        self.__left_margin = left
        self.__top_margin = top
        self.__right_margin = right
        self.__bottom_margin = bottom

        if self.__context_buttons_layout:
            for item in self.__context_buttons_layout:
                item.set_contents_margins(
                    self.__left_margin, 0, self.__right_margin, self.__spacing)

        self.__menu_context_layout.set_contents_margins(
            0, self.__top_margin, 0, self.__bottom_margin)

    def set_separators_margins(
            self, left: int, top: int, right: int, bottom: int) -> None:
        """..."""
        if self.__separator_layouts:
            for item in self.__separator_layouts:
                item.set_contents_margins(
                    left, top, right, bottom + self.__spacing)

    def set_spacing(self, spacing: int) -> None:
        """..."""
        self.__spacing = spacing

        if self.__context_buttons_layout:
            for item in self.__context_buttons_layout:
                item.set_contents_margins(
                    self.__left_margin, 0, self.__right_margin, self.__spacing)

        if self.__separator_layouts:
            for item in self.__separator_layouts:
                margins = item.contents_margins()
                margins.set_bottom(self.__spacing)
                item.set_contents_margins(margins)

    def __set_dynamic_positioning(self) -> None:
        x = self.geometry().x()
        y = self.geometry().y()

        screen_width = self.__main_window.screen().geometry().width()
        screen_height = self.__main_window.screen().geometry().height()

        if self.geometry().x() + self.geometry().width() > screen_width:
            x = screen_width - self.geometry().width()

        if self.geometry().y() + self.geometry().height() > screen_height:
            y = self.geometry().y() - self.geometry().height() + 10
        
        self.move(x, y)

    def __set_style_signal(self) -> None:
        self.__style_saved = self.__main_window.style_sheet()

    def __style(self) -> str:
        if self.__style_saved:
            return self.__style_saved.replace(
                '#QQuickContextMenu', 'QQuickContextMenu').replace(
                'QQuickContextMenu', '#QQuickContextMenu')
        return self.__main_window.style_sheet()


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
        self.__quick_context_menu = None
        self.__configure_window()

    def quick_context_menu(self) -> QQuickContextMenu | None:
        """..."""
        return self.__quick_context_menu

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

    def set_quick_context_menu(self, context_menu: QQuickContextMenu) -> None:
        """..."""
        self.__quick_context_menu = context_menu

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
        if self.__platform_settings.is_dark(self):
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 180))
        else:
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 80))
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
                    self.__set_visible_shadow(False)
                else:
                    self.__central_widget.set_style_sheet(self.__style_sheet)
                    self.__set_visible_shadow(True)

        return QtWidgets.QMainWindow.event_filter(self, watched, event)


class QHeaderBar(QtWidgets.QFrame):
    """Window header bar

    Replaces traditional title bar and allows adding and editing widgets
    """
    resize_event_signal = QtCore.Signal(object)

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
            .gui_env.control_button_order())

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.set_contents_margins(4, 4, 4, 4)
        self.__layout.set_spacing(6)

        self.__bar_item_layout_left = QtWidgets.QHBoxLayout()
        self.__bar_item_layout_left.set_contents_margins(0, 0, 0, 0)
        self.__layout.add_layout(self.__bar_item_layout_left)

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

    def add_widget_to_left(self, widget: QtWidgets.QWidget) -> None:
        """Adds a widget to the left side of the header bar

        After the control buttons or window icon.
        """
        self.__left_layout.add_widget(widget)

    def add_widget_to_right(self, widget: QtWidgets.QWidget) -> None:
        """Adds a widget to the right side of the header bar

        Before the control buttons or window icon.
        """
        self.__right_layout.add_widget(widget)

    def control_buttons_side(self) -> str:
        """Window control buttons side

        Return 'left' or 'right' string
        """
        if 2 in self.__right_ctrl_buttons.button_order():
            return 'right'
        return 'left'

    def lef_layout(self) -> QtWidgets.QHBoxLayout:
        """QHBoxLayout on left

        Gets the QHBoxLayout of the widgets that are on the left of the
        QHeaderBar
        """
        return self.__left_layout

    def resize_event(self, event: QtGui.QResizeEvent) -> None:
        """The resize_event method has been rewritten

        Use the resize_event_signal signal, or consider using event-specific
        methods such as event_filter
        """
        self.resize_event_signal.emit(event)

        if self.__main_window.is_decorated():
            self.__left_ctrl_buttons.set_visible(False)
            self.__right_ctrl_buttons.set_visible(False)
            _50_percent_left = self.__50_percent_left_size(True)
        else:
            _50_percent_left = self.__50_percent_left_size(False)

            if self.__main_window.is_maximized():
                if (self.__main_window.platform_settings()
                        .gui_env.use_global_menu()):
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

    def right_layout(self) -> QtWidgets.QHBoxLayout:
        """QHBoxLayout on right

        Gets the QHBoxLayout of the widgets that are on the right of the
        QHeaderBar
        """
        return self.__right_layout

    def set_left_control_buttons_visible(self, visible: bool) -> None:
        """Visibility of the control buttons on the left side of the window

        Setting this to False will hide them, and True will show them
        """
        self.__left_ctrl_buttons_visibility = visible
        self.__left_ctrl_buttons.set_visible(visible)

    def set_close_window_button_visible(self, visible: bool):
        """..."""
        self.__left_ctrl_buttons.set_close_window_button_visible(visible)
        self.__right_ctrl_buttons.set_close_window_button_visible(visible)

    def set_maximize_window_button_visible(self, visible: bool):
        """..."""
        self.__left_ctrl_buttons.set_maximize_window_button_visible(visible)
        self.__right_ctrl_buttons.set_maximize_window_button_visible(visible)

    def set_minimize_window_button_visible(self, visible: bool):
        """..."""
        self.__left_ctrl_buttons.set_minimize_window_button_visible(visible)
        self.__right_ctrl_buttons.set_minimize_window_button_visible(visible)

    def set_move_area_as_enable(self, enable: bool):
        """..."""
        self.__window_move_area.set_enable(enable)

    def set_right_control_buttons_visible(self, visible: bool) -> None:
        """Visibility of the control buttons on the right side of the window

        Setting this to False will hide them, and True will show them
        """
        self.__right_ctrl_buttons_visibility = visible
        self.__right_ctrl_buttons.set_visible(visible)

    def set_text(self, text: str) -> None:
        """Sets a text in the center

        :param text: The text to be shown in the center of the QWindowMoveArea
        """
        if not self.__main_window.is_decorated():
            self.__window_move_area_text.set_text(text)

    def set_window_icon(self, icon: QtGui.QIcon) -> None:
        """Window icon

        A new icon to update the application icon
        """
        self.__right_ctrl_buttons.update_window_icon(icon)
        self.__left_ctrl_buttons.update_window_icon(icon)

    def text(self) -> str:
        """Get the QWindowMoveArea's text

        The text shown in the center of the QWindowMoveArea
        """
        return self.__window_move_area.text()

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


class QSideViewApplicationWindow(QApplicationWindow):
    """Window with side panel"""
    adaptive_mode_signal = QtCore.Signal(object)
    sideview_opened_signal = QtCore.Signal(object)
    sideview_closed_signal = QtCore.Signal(object)
    wide_mode_signal = QtCore.Signal(object)

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes
        """
        super().__init__(*args, **kwargs)
        # Flags
        self.__minimum_width = 340
        self.__minimum_height = 200
        self.__border_size = 12
        self.__is_panel_open = False
        self.__panel_width = 250
        self.__panel_color_default = (0, 0, 0, 0.05)
        self.__panel_color = self.__panel_color_default
        self.__horizontal_and_vertical_flip_width = 650
        self.__is_vertical = False

        # Settings
        self.set_window_title('MPX Application Window')
        self.set_minimum_width(self.__minimum_width)
        self.set_minimum_height(self.__minimum_height)
        self.resize(self.__initial_width(), 500)

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)

        # Main layout
        self.__main_box = QtWidgets.QHBoxLayout()
        self.__main_box.set_contents_margins(0, 0, 0, 0)
        self.__main_box.set_spacing(0)
        self.central_widget().set_layout(self.__main_box)

        # Side view
        self.__sideview_width = QtWidgets.QWidget()
        self.__sideview_width.set_fixed_width(self.__panel_width)
        self.__main_box.add_widget(self.__sideview_width, 9)

        self.__sideview_main_box = QtWidgets.QVBoxLayout()
        self.__sideview_main_box.set_contents_margins(0, 0, 0, 0)
        self.__sideview_main_box.set_alignment(QtCore.Qt.AlignTop)
        self.__sideview_width.set_layout(self.__sideview_main_box)

        # Side header bar
        self.__sideview_headerbar_box = QtWidgets.QHBoxLayout()
        self.__sideview_headerbar_box.set_spacing(0)
        self.__sideview_headerbar_box.set_contents_margins(0, 0, 6, 0)
        self.__sideview_main_box.add_layout(self.__sideview_headerbar_box)

        self.__sideview_headerbar = QHeaderBar(self)
        self.__sideview_headerbar.set_right_control_buttons_visible(False)
        self.__sideview_headerbar_box.add_widget(self.__sideview_headerbar)

        self.__sideview_close_button = QtWidgets.QToolButton()
        self.__sideview_close_button.set_visible(False)
        self.__sideview_close_button.clicked.connect(self.close_sideview)
        self.__sideview_close_button.set_icon(
            QtGui.QIcon.from_theme('arrow-left'))
        self.__sideview_headerbar_box.add_widget(self.__sideview_close_button)

        # Side panel
        self.__sideview_box = QtWidgets.QVBoxLayout()
        self.__sideview_box.set_spacing(6)
        self.__sideview_box.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__sideview_main_box.add_layout(self.__sideview_box)

        self.set_panel_color()

        # Frame view
        self.__frameview_main_box = QtWidgets.QVBoxLayout()
        self.__frameview_main_box.set_alignment(QtCore.Qt.AlignTop)
        self.__main_box.add_layout(self.__frameview_main_box)

        # Frame view header bar
        self.__frameview_header_bar = QHeaderBar(self)
        self.__frameview_header_bar.set_left_control_buttons_visible(False)
        self.__frameview_main_box.add_widget(self.__frameview_header_bar)

        self.__sideview_open_button = QtWidgets.QToolButton()
        self.__sideview_open_button.set_icon(
            QtGui.QIcon.from_theme('page-2sides'))  # sidebar-collapse
        self.__sideview_open_button.clicked.connect(self.open_sideview)
        self.__frameview_header_bar.add_widget_to_left(
            self.__sideview_open_button)
        self.__sideview_open_button.set_visible(False)

        self.__frameview_box = QtWidgets.QVBoxLayout()
        self.__frameview_box.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__frameview_main_box.add_layout(self.__frameview_box, 9)

        # Signals
        self.resize_event_signal.connect(self.__resize_event)
        self.set_style_signal.connect(lambda _: self.set_panel_color())
        self.reset_style_signal.connect(self.__reset_style)

    def close_sideview(self) -> None:
        """..."""
        print('close sideview', self)

    def frame_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__frameview_box

    def horizontal_and_vertical_flip_width(self) -> int:
        """..."""
        return self.__horizontal_and_vertical_flip_width

    def open_sideview(self) -> None:
        self.sideview_opened_signal.emit('panel-opened-signal')
        self.__is_panel_open = True
        print('open sideview')

    def panel_color(self) -> tuple:
        """..."""
        return self.__panel_color

    def panel_header_bar(self) -> QHeaderBar:
        """..."""
        return self.__sideview_headerbar

    def panel_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__sideview_box

    def set_close_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_close_window_button_visible(visible)
        self.__frameview_header_bar.set_close_window_button_visible(visible)

    def set_header_bar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__sideview_headerbar.set_window_icon(icon)
        self.__frameview_header_bar.set_window_icon(icon)

    def set_header_bar_title(self, text: str) -> None:
        """..."""
        self.__frameview_header_bar.set_text(text)

    def set_horizontal_and_vertical_flip_width(self, width: int) -> None:
        """..."""
        self.__horizontal_and_vertical_flip_width = width

    def set_left_control_buttons_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_left_control_buttons_visible(visible)

    def set_maximize_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_maximize_window_button_visible(visible)
        self.__frameview_header_bar.set_maximize_window_button_visible(
            visible)

    def set_minimize_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_minimize_window_button_visible(visible)
        self.__frameview_header_bar.set_minimize_window_button_visible(
            visible)

    def set_panel_color(self, rgba: tuple = None) -> None:
        """..."""
        self.__panel_color = rgba if rgba else self.__panel_color_default
        application_style_sheet = '; '.join(
            [x.replace('#QApplicationWindow', '').replace('{', '').strip()
             for x in self.style_sheet().split('}')
             if 'QApplicationWindow' in x][-1].split(';'))

        self.__sideview_width.set_object_name('__panelwidthstyle')
        self.__sideview_width.set_style_sheet(
            '#__panelwidthstyle {'
            f'{application_style_sheet}'
            'background-color: rgba('
            f'{self.__panel_color[0]}, {self.__panel_color[1]}, '
            f'{self.__panel_color[2]}, {self.__panel_color[3]});'
            'border: 0px; '
            'border-top-right-radius: 0;'
            'border-bottom-right-radius: 0;'
            'padding: 0px;'
            'margin: 1px 0px 1px 1px;}')

    def set_panel_fixed_width(self, width: int) -> None:
        """..."""
        self.__panel_width = width
        self.__sideview_width.set_fixed_width(self.__panel_width)

    def set_right_control_buttons_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_right_control_buttons_visible(visible)

    def __initial_width(self) -> int:
        if self.screen().size().width() < self.__panel_width < 500:
            return self.__minimum_width
        return 750

    def __panel_was_closed_signal(self, event: QtCore.Signal) -> None:
        if self.__is_panel_open:
            self.sideview_closed_signal.emit(event)
            self.__is_panel_open = False

    def __switch_vertical_and_horizontal_window(self) -> None:
        # Vertical
        if (not self.__is_vertical and self.size().width() <
                self.__horizontal_and_vertical_flip_width):
            self.__is_vertical = True
            self.__switch_to_vertical()
            self.adaptive_mode_signal.emit('adaptive-mode-signal')

        # Horizontal
        elif (self.__is_vertical and self.size().width() >
              self.__horizontal_and_vertical_flip_width):
            self.__is_vertical = False
            self.__switch_to_horizontal()
            self.wide_mode_signal.emit('wide-mode-signal')

    def __switch_to_vertical(self) -> None:
        self.__sideview_width.set_visible(False)
        self.__frameview_header_bar.set_left_control_buttons_visible(True)
        self.__sideview_open_button.set_visible(True)
        self.__sideview_headerbar.set_move_area_as_enable(False)
        self.__sideview_close_button.set_visible(True)

    def __switch_to_horizontal(self) -> None:
        self.__sideview_width.set_visible(True)
        self.__frameview_header_bar.set_left_control_buttons_visible(False)
        self.__sideview_open_button.set_visible(False)
        self.__sideview_headerbar.set_move_area_as_enable(True)
        self.__sideview_close_button.set_visible(False)

    def __visibility_of_window_control_buttons(self) -> None:
        if self.is_maximized():
            if self.platform_settings().gui_env.use_global_menu():
                self.__sideview_headerbar.set_left_control_buttons_visible(
                    False)
            # Close panel
        elif self.is_full_screen():
            self.__sideview_headerbar.set_left_control_buttons_visible(False)
            # Close panel
        else:
            self.__sideview_headerbar.set_left_control_buttons_visible(True)

    def __resize_event(self, event: QtGui.QResizeEvent) -> None:
        logging.info(event)
        self.__switch_vertical_and_horizontal_window()
        self.__visibility_of_window_control_buttons()

    def __reset_style(self, event) -> None:
        logging.info(event)
        self.set_panel_color()

    def __str__(self) -> str:
        return 'QSidePanelApplicationWindow()'

    def __repr__(self) -> str:
        return 'QSidePanelApplicationWindow(QtWidgetsX.QApplicationWindow)'


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

    def button_order(self) -> tuple:
        """Tuple with the order of the buttons

        0 is the minimize button, 1 is the maximize button, 2 is the close
        button and 3 is window icon. Like: (0, 1, 2,)
        """
        return self.__button_order

    def update_window_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.__window_icon.set_pixmap(icon.pixmap(20))

    def set_close_window_button_visible(self, visible: bool) -> None:
        """..."""
        if 2 in self.__button_order:
            self.__close_button.set_visible(visible)

    def set_maximize_window_button_visible(self, visible: bool) -> None:
        """..."""
        if 1 in self.__button_order:
            self.__maximize_button.set_visible(visible)

    def set_minimize_window_button_visible(self, visible: bool) -> None:
        """..."""
        if 0 in self.__button_order:
            self.__minimize_button.set_visible(visible)

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
        self.__default_style = settings.StyleBuilder(self.__main_window)

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
            if not self.__main_window.is_decorated():
                if (event.button() == QtCore.Qt.LeftButton and
                        self.under_mouse()):
                    self.__main_window.window_handle().start_system_move()

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
                if self.__main_window.is_maximized():
                    self.native_parent_widget().show_normal()
                elif self.__main_window.is_full_screen():
                    self.native_parent_widget().show_maximized()
                else:
                    self.native_parent_widget().show_maximized()
