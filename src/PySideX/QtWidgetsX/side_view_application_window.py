#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.application_window import QApplicationWindow
from PySideX.QtWidgetsX.header_bar import QHeaderBar

SRC_DIR = os.path.dirname(os.path.abspath(__file__))


class QOverlaySidePanel(QtWidgets.QFrame):
    """..."""
    panel_closed_signal = QtCore.Signal(object)

    def __init__(self, widget: QtWidgets.QWidget, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Param
        self.__sideview_widget = widget
        self.__sideview_widget_box = self.__sideview_widget.parent().layout()
        self.__toplevel = self.__sideview_widget.parent().window()

        # Settings
        self.set_contents_margins(
            self.__toplevel.shadow_size(), self.__toplevel.shadow_size(),
            self.__toplevel.shadow_size(), self.__toplevel.shadow_size())
        self.__overlay_base_style = self.__parse_toplevel_style()

        # Main layout
        self.__main_box = QtWidgets.QHBoxLayout()
        self.__main_box.set_contents_margins(0, 0, 0, 0)
        self.__main_box.set_spacing(0)
        self.set_layout(self.__main_box)

        # Side
        self.__sideview_background = QtWidgets.QWidget()
        self.__sideview_background.set_fixed_width(
            self.__sideview_widget.width())
        self.__sideview_background.set_contents_margins(0, 0, 0, 0)
        self.__sideview_background.set_object_name('__sideview_background')
        self.__main_box.add_widget(self.__sideview_background)

        self.__sideview_box = QtWidgets.QHBoxLayout()
        self.__sideview_box.set_contents_margins(0, 0, 0, 0)
        self.__sideview_background.set_layout(self.__sideview_box)

        # Close
        class CloseArea(QtWidgets.QWidget):
            def __init__(self, toplevel: QtWidgets.QWidget) -> None:
                super().__init__()
                self.__top = toplevel

            def mouse_press_event(self, ev: QtGui.QMouseEvent) -> None:
                if ev.button() == QtCore.Qt.LeftButton and self.under_mouse():
                    self.__top.close()

        self.__close_view_background = QtWidgets.QWidget()
        self.__close_view_background.set_contents_margins(0, 0, 0, 0)
        self.__close_view_background.set_object_name('__close_view_background')
        self.__main_box.add_widget(self.__close_view_background)

        self.__close_view_box = QtWidgets.QVBoxLayout()
        self.__close_view_background.set_layout(self.__close_view_box)
        self.__close_view_box.add_widget(CloseArea(self))

        self.__toplevel.resize_event_signal.connect(self.__resize_sig)

    def close(self) -> None:
        """..."""
        self.__sideview_widget.set_visible(False)
        self.__sideview_box.remove_widget(self.__sideview_widget)
        self.__sideview_widget_box.insert_widget(0, self.__sideview_widget)
        self.set_visible(False)

    def open(self) -> None:
        """..."""
        self.__update_style()
        self.__sideview_widget.set_visible(True)
        self.resize(self.__toplevel.width(), self.__toplevel.height())
        self.__sideview_widget_box.remove_widget(self.__sideview_widget)
        self.__sideview_box.add_widget(self.__sideview_widget)
        self.set_visible(True)
        self.move(0, 0)

    def __update_style(self) -> None:
        self.__overlay_base_style = self.__parse_toplevel_style()
        self.__sideview_background.set_style_sheet(
            self.__toplevel.style_sheet() +
            '#__sideview_background {'
            f'{self.__overlay_base_style}'
            'border-right: 0px; '
            'border-top-right-radius: 0;'
            'border-bottom-right-radius: 0;}')

        self.__close_view_background.set_style_sheet(
            '#__close_view_background {'
            f'{self.__overlay_base_style}'
            'background-color: rgba(0, 0, 0, 0.2);'
            'border-left: 0px;'
            'border-top-left-radius: 0;'
            'border-bottom-left-radius: 0;}')

    def __parse_toplevel_style(self) -> str:
        return '; '.join(
            [x.replace('#QApplicationWindow', '').replace('{', '').strip()
             for x in self.__toplevel.style_sheet().split('}')
             if 'QApplicationWindow' in x][-1].split(';'))

    def __resize_sig(self) -> None:
        self.resize(self.__toplevel.width(), self.__toplevel.height())


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

        # Side view overlay
        self.__sideview_overlay = QOverlaySidePanel(
            self.__sideview_width, parent=self)
        self.__sideview_overlay.set_visible(False)

        # Signals
        self.resize_event_signal.connect(self.__resize_event)
        self.set_style_signal.connect(lambda _: self.set_panel_color())
        self.reset_style_signal.connect(self.__reset_style)

    def close_sideview(self) -> None:
        """..."""
        self.__sideview_overlay.close()
        self.sideview_closed_signal.emit('sideview-closed-signal')
        self.__is_panel_open = False

    def frame_view_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__frameview_box

    def horizontal_and_vertical_flip_width(self) -> int:
        """..."""
        return self.__horizontal_and_vertical_flip_width

    def open_sideview(self) -> None:
        self.__sideview_overlay.open()
        self.sideview_opened_signal.emit('sideview-opened-signal')
        self.__is_panel_open = True

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
        # self.__sideview_headerbar.set_move_area_as_enable(False)
        self.__sideview_close_button.set_visible(True)

    def __switch_to_horizontal(self) -> None:
        self.__sideview_width.set_visible(True)
        self.__frameview_header_bar.set_left_control_buttons_visible(False)
        self.__sideview_open_button.set_visible(False)
        # self.__sideview_headerbar.set_move_area_as_enable(True)
        self.__sideview_close_button.set_visible(False)

        if self.__is_panel_open:
            self.close_sideview()
            self.__sideview_width.set_visible(True)

    def __visibility_of_window_control_buttons(self) -> None:
        if self.is_maximized():
            if self.platform_settings().gui_env.use_global_menu():
                self.__sideview_headerbar.set_left_control_buttons_visible(
                    False)

            if self.__is_panel_open:
                self.close_sideview()
                self.__sideview_width.set_visible(True)

        elif self.is_full_screen():
            self.__sideview_headerbar.set_left_control_buttons_visible(False)

            if self.__is_panel_open:
                self.close_sideview()
                self.__sideview_width.set_visible(True)
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
