#!/usr/bin/env python3
import logging
import os
import pathlib

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.application_window import QApplicationWindow
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv
from PySideX.QtWidgetsX.modules.colorop import ColorOp

SRC_DIR = os.path.dirname(os.path.abspath(__file__))


class QQuickContextMenuSeparator(QtWidgets.QFrame):
    """..."""
    def __init__(self, color: QtGui.QColor = None, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__color = color if color else QtGui.QPalette().color(
                QtGui.QPalette.Window.Mid)
        self.set_frame_shape(QtWidgets.QFrame.HLine)
        self.set_frame_shadow(QtWidgets.QFrame.Plain)
        self.set_line_width(0)
        self.set_mid_line_width(3)
        self.set_contents_margins(0, 0, 0, 0)
        self.set_color(self.__color)

    def set_color(self, color: QtGui.QColor) -> None:
        """..."""
        palette = self.palette()
        palette.set_color(QtGui.QPalette.WindowText, color)
        self.set_palette(palette)


class QQuickContextMenuButton(QtWidgets.QFrame):
    """..."""
    def __init__(
            self,
            context_menu: QtWidgets.QWidget,
            text: str,
            receiver: callable,
            icon: QtGui.QIcon | None = None,
            shortcut: QtGui.QKeySequence | None = None,
            is_dark: bool = False,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.set_contents_margins(0, 0, 0, 0)

        self.__context_menu = context_menu
        self.__text = text
        self.__receiver = receiver
        self.__icon = icon
        self.__shortcut = shortcut
        self.__is_dark = is_dark

        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_spacing(0)
        self.set_layout(self.__main_layout)

        self.__left_layout = QtWidgets.QHBoxLayout()
        self.__left_layout.set_alignment(QtCore.Qt.AlignLeft)
        self.__main_layout.add_layout(self.__left_layout)

        if not self.__icon:
            symbolic = ''
            if self.__is_dark:
                symbolic = '-symbolic'

            icon_path = os.path.join(
                pathlib.Path(SRC_DIR).parent,
                'platform', 'static', f'context-menu-item{symbolic}.svg')

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
        self.__context_menu.close()


class QQuickContextMenu(QtWidgets.QFrame):
    """..."""

    def __init__(self, toplevel: QtWidgets.QWidget, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param toplevel: QApplicationWindow app main window instance
        """
        super().__init__(*args, **kwargs)
        # Param
        self.__toplevel = toplevel

        # Settings
        color = self.palette().color(QtGui.QPalette.Window)
        self.__color_op = ColorOp((color.red(), color.green(), color.blue()))

        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        # Flags
        self.set_minimum_width(50)
        self.set_minimum_height(35)

        self.__separator_layouts = []
        self.__context_buttons_layout = []
        self.__context_buttons = []

        self.__style_saved = None
        self.__point_x = None
        self.__point_y = None

        # Properties
        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment())

        self.__spacing = self.__gui_env.settings().context_menu_spacing()
        self.__left_margin = self.__gui_env.settings().context_menu_padding()
        self.__top_margin = self.__gui_env.settings().context_menu_padding()
        self.__right_margin = self.__gui_env.settings().context_menu_padding()
        self.__bottom_margin = self.__gui_env.settings().context_menu_padding()

        self.__is_dark = self.__color_op.is_dark()

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

        if self.__is_dark:
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 100))
        else:
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 70))
        self.__main_widget.set_graphics_effect(self.__shadow_effect)

        self.__toplevel.set_style_signal.connect(self.__set_style_signal)
        self.__toplevel.reset_style_signal.connect(self.__set_style_signal)

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
            self, text, receiver, icon, shortcut, self.__is_dark)
        ctx_btn.set_style_sheet(self.__style_saved)
        ctx_btn_l.add_widget(ctx_btn)

        self.__menu_context_layout.add_layout(ctx_btn_l)

        self.__context_buttons_layout.append(ctx_btn_l)
        self.__context_buttons.append(ctx_btn)

    def add_separator(self, color: QtGui.QColor = None) -> None:
        """..."""
        color = color if color else QtGui.QPalette().color(
            QtGui.QPalette.Window.Mid)
        if self.__gui_env.settings().context_menu_separator_color_type(
                ) == 'disabled-text':
            color = QtGui.QColor(
                QtGui.QPalette().color(
                    QtGui.QPalette.Disabled, QtGui.QPalette.Text))

        separator_layout = QtWidgets.QVBoxLayout()

        margin = self.__gui_env.settings().context_menu_separator_margin()
        separator_layout.set_contents_margins(
            margin[0], margin[1], margin[2], margin[3] + self.__spacing)

        separator = QQuickContextMenuSeparator(color)
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

        screen_width = self.__toplevel.screen().geometry().width()
        screen_height = self.__toplevel.screen().geometry().height()

        if self.geometry().x() + self.geometry().width() > screen_width:
            x = screen_width - self.geometry().width()

        if self.geometry().y() + self.geometry().height() > screen_height:
            y = self.geometry().y() - self.geometry().height() + 10

        self.move(x, y)

    def __set_style_signal(self) -> None:
        self.__style_saved = self.__toplevel.style_sheet()

    def __style(self) -> str:
        if self.__style_saved:
            return self.__style_saved.replace(
                '#QQuickContextMenu', 'QQuickContextMenu').replace(
                'QQuickContextMenu', '#QQuickContextMenu')
        return self.__toplevel.style_sheet()
