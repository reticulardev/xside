#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class QMainWindow(QtWidgets.QFrame):
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

        self.__central_widget = QMainWindow()
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
