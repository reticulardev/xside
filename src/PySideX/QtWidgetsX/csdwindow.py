#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class CentralW(QtWidgets.QFrame):
    """..."""
    def __init__(
            self, toplevel, border_radius: tuple, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.set_style_sheet(
            f'border-top-left-radius: {border_radius[0]}px;'
            f'border-top-right-radius: {border_radius[1]}px;'
            f'border-bottom-left-radius: {border_radius[3]}px;'
            f'border-bottom-right-radius: {border_radius[2]}px;'
            'background-color: rgba(100, 200, 50, 200);')

        self.__toplevel = toplevel

        self.__main_box = QtWidgets.QVBoxLayout()
        self.set_layout(self.__main_box)

        self.__btn = QtWidgets.QPushButton('Remove shadow')
        self.__main_box.add_widget(self.__btn)
        self.__btn.clicked.connect(lambda: self.__toplevel.remove_shadow())

        self.__btn2 = QtWidgets.QPushButton('Add shadow')
        self.__main_box.add_widget(self.__btn2)
        self.__btn2.clicked.connect(lambda: self.__toplevel.add_shadow())


class Shadow(QtWidgets.QFrame):
    """..."""
    def __init__(self, position: str, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        # self.set_auto_fill_background(True)
        #
        # palette = self.palette()
        # palette.set_color(QtGui.QPalette.Window, QtGui.QColor(color))
        # self.set_palette(palette)
        self.__shadow_color = 'rgba(0, 0, 0, 50)'
        end_color = 'rgba(0, 0, 0, 0)'
        if position == 'top-left':
            self.set_style_sheet(
                'background:'
                '  qradialgradient('
                '  cx: 0.5, cy: 0.5, radius: 2, fx: 1.0, fy: 1.0,'
                f' stop: 0.0 {self.__shadow_color},'
                f' stop: 0.4 {end_color}'
                ');')

        elif position == 'top':
            self.set_style_sheet(
                'background: qlineargradient('
                '  x1:0 y1:0, x2:0 y2:1,'
                f' stop:0.0 {end_color},'
                f' stop:1.0 {self.__shadow_color});')

        elif position == 'top-right':
            self.set_style_sheet(
                'background:'
                '  qradialgradient('
                '  cx: 0.5, cy: 0.5, radius: 2, fx: 0.0, fy: 1.0,'
                f' stop: 0.0 {self.__shadow_color},'
                f' stop: 0.4 {end_color}'
                ');')

        elif position == 'left':
            self.set_style_sheet(
                'background: qlineargradient('
                '  x1:0 y1:0, x2:1 y2:0,'
                f' stop:0.0 {end_color},'
                f' stop:1.0 {self.__shadow_color});')

        elif position == 'right':
            self.set_style_sheet(
                'background: qlineargradient('
                '  x1:0 y1:0, x2:1 y2:0,'
                f' stop:0.0 {self.__shadow_color},'
                f' stop:1.0 {end_color});')

        elif position == 'bottom-left':
            self.set_style_sheet(
                'background:'
                '  qradialgradient('
                '  cx: 0.5, cy: 0.5, radius: 2, fx: 1.0, fy: 0.0,'
                f' stop: 0.0 {self.__shadow_color},'
                f' stop: 0.4 {end_color}'
                ');')

        elif position == 'bottom':
            self.set_style_sheet(
                'background: qlineargradient('
                '  x1:0 y1:0, x2:0 y2:1,'
                f' stop:0.0 {self.__shadow_color},'
                f' stop:1.0 {end_color});')

        elif position == 'bottom-right':
            self.set_style_sheet(
                'background:'
                '  qradialgradient('
                '  cx: 0.5, cy: 0.5, radius: 2, fx: 0.0, fy: 0.0,'
                f' stop: 0.0 {self.__shadow_color},'
                f' stop: 0.4 {end_color}'
                ');')
        else:
            self.set_style_sheet(
                f'background-color: {self.__shadow_color};')

    def set_color(self, color: tuple = None) -> None:
        if not color:
            self.set_style_sheet(f'background-color: {self.__shadow_color};')
        else:
            self.set_style_sheet(
                'background-color: rgba('
                f'{color[0]}, {color[1], color[2], color[3]});')


class CSDWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

        self.__border_radius = (20, 20, 0, 0)
        self.__width = 500
        self.__height = 500
        self.__shadow_size = 20
        self.__base_shadow_size = self.__shadow_size
        # self.__base_shadow_size = 0 + self.__border_radius[0]  # desco maior

        self.resize(
            self.__width + self.__shadow_size,
            self.__height + self.__shadow_size)

        self.set_contents_margins(0, 0, 0, 0)

        self.__central_shadow = QtWidgets.QWidget()
        self.__central_shadow.set_contents_margins(0, 0, 0, 0)
        self.set_central_widget(self.__central_shadow)

        self.__main_box = QtWidgets.QVBoxLayout()
        self.__main_box.set_contents_margins(0, 0, 0, 0)
        self.__main_box.set_spacing(0)
        self.__central_shadow.set_layout(self.__main_box)

        # Top
        self.__top_box = QtWidgets.QHBoxLayout()
        self.__main_box.add_layout(self.__top_box)

        self.__top_left_shadow = Shadow('top-left')
        self.__top_left_shadow.set_fixed_width(self.__base_shadow_size)
        self.__top_left_shadow.set_fixed_height(self.__base_shadow_size)
        self.__top_box.add_widget(self.__top_left_shadow)

        self.__top_shadow = Shadow('top')
        self.__top_shadow.set_fixed_height(self.__base_shadow_size)
        self.__top_box.add_widget(self.__top_shadow)

        self.__top_right_shadow = Shadow('top-right')
        self.__top_right_shadow.set_fixed_width(self.__base_shadow_size)
        self.__top_right_shadow.set_fixed_height(self.__base_shadow_size)
        self.__top_box.add_widget(self.__top_right_shadow)

        # Center
        self.__center_box = QtWidgets.QHBoxLayout()
        self.__main_box.add_layout(self.__center_box)

        self.__left_shadow = Shadow('left')
        self.__left_shadow.set_fixed_width(self.__base_shadow_size)
        self.__center_box.add_widget(self.__left_shadow)

        # ---
        self.__center_shadow = Shadow('center')
        self.__center_shadow.resize(self.__width, self.__height)
        self.__center_box.add_widget(self.__center_shadow)

        self.__central_widget_box = QtWidgets.QVBoxLayout()
        self.__central_widget_box.set_contents_margins(0, 0, 0, 0)
        self.__central_widget_box.set_spacing(0)
        self.__center_shadow.set_layout(self.__central_widget_box)

        self.__central_widget = CentralW(self, self.__border_radius)
        self.__central_widget_box.add_widget(self.__central_widget)
        # ---

        self.__right_shadow = Shadow('right')
        self.__right_shadow.set_fixed_width(self.__base_shadow_size)
        self.__center_box.add_widget(self.__right_shadow)

        # Bottom
        self.__bottom_box = QtWidgets.QHBoxLayout()
        self.__main_box.add_layout(self.__bottom_box)

        self.__bottom_left_shadow = Shadow('bottom-left')
        self.__bottom_left_shadow.set_fixed_width(self.__base_shadow_size)
        self.__bottom_left_shadow.set_fixed_height(self.__base_shadow_size)
        self.__bottom_box.add_widget(self.__bottom_left_shadow)

        self.__bottom_shadow = Shadow('bottom')
        self.__bottom_shadow.set_fixed_height(self.__base_shadow_size)
        self.__bottom_box.add_widget(self.__bottom_shadow)

        self.__bottom_right_shadow = Shadow('bottom-right')
        self.__bottom_right_shadow.set_fixed_width(self.__base_shadow_size)
        self.__bottom_right_shadow.set_fixed_height(self.__base_shadow_size)
        self.__bottom_box.add_widget(self.__bottom_right_shadow)

        self.install_event_filter(self)

    def remove_bottom_shadow(self) -> None:
        self.__bottom_left_shadow.set_visible(False)
        self.__bottom_shadow.set_visible(False)
        self.__bottom_right_shadow.set_visible(False)

    def remove_left_shadow(self) -> None:
        self.__top_left_shadow.set_visible(False)
        self.__left_shadow.set_visible(False)
        self.__bottom_left_shadow.set_visible(False)

    def remove_right_shadow(self) -> None:
        self.__top_right_shadow.set_visible(False)
        self.__right_shadow.set_visible(False)
        self.__bottom_right_shadow.set_visible(False)

    def remove_shadow(self) -> None:
        self.__center_shadow.set_color((0, 0, 0, 0))
        self.remove_bottom_shadow()
        self.remove_left_shadow()
        self.remove_right_shadow()
        self.remove_top_shadow()

    def remove_top_shadow(self) -> None:
        self.__top_left_shadow.set_visible(False)
        self.__top_shadow.set_visible(False)
        self.__top_right_shadow.set_visible(False)

    def add_shadow(self):
        self.__center_shadow.set_color()

        self.__bottom_left_shadow.set_visible(True)
        self.__bottom_shadow.set_visible(True)
        self.__bottom_right_shadow.set_visible(True)

        self.__top_left_shadow.set_visible(True)
        self.__left_shadow.set_visible(True)
        self.__bottom_left_shadow.set_visible(True)

        self.__top_right_shadow.set_visible(True)
        self.__right_shadow.set_visible(True)
        self.__bottom_right_shadow.set_visible(True)

        self.__top_left_shadow.set_visible(True)
        self.__top_shadow.set_visible(True)
        self.__top_right_shadow.set_visible(True)

    def event_filter(
            self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.Resize:
            self.__center_shadow.set_minimum_height(100)
            self.__center_shadow.set_minimum_width(100)

        elif event.type() == QtCore.QEvent.HoverMove:
            pass

        elif event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                if self.under_mouse():
                    self.window_handle().start_system_move()

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self.under_mouse():
                # self.close()
                pass

        return QtWidgets.QMainWindow.event_filter(self, watched, event)
