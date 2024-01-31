#!/usr/bin/env python3
import logging

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.quick_context_menu_button import (
    QQuickContextMenuButton)
from PySideX.QtWidgetsX.quick_context_menu_separator import (
    QQuickContextMenuSeparator)


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
        if self.__main_window.platform_settings().is_dark_widget(self):
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

        separator = QQuickContextMenuSeparator(self.__main_window)
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