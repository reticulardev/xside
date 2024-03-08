#!/usr/bin/env python3
import logging
import os
import pathlib
import sys

from PIL import Image
from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from xside.modules import color
from xside.modules.env import GuiEnv
from xside.modules.style import StyleParser
from xside.widgets.applicationwindow import ApplicationWindow
from xside.widgets.headerbar import HeaderBar


class OverlaySideView(QtWidgets.QFrame):
    """..."""
    side_view_closed_signal = QtCore.Signal(object)

    def __init__(
            self, sideview_widget: QtWidgets.QWidget,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Param
        self.__sideview_widget = sideview_widget

        # Properties
        self.__sideview_widget_box = self.__sideview_widget.parent().layout()
        self.__toplevel = self.__sideview_widget.parent().window()
        self.__style_parser = StyleParser(self.__toplevel.style_sheet())

        # Anim
        self.anim_open = QtCore.QPropertyAnimation(self, b"size")
        self.anim_open_group = QtCore.QSequentialAnimationGroup()
        self.anim_close = QtCore.QPropertyAnimation(self, b"size")
        self.anim_close_group = QtCore.QSequentialAnimationGroup()

        self.__close_timer = QtCore.QTimer()

        # Main layout
        self.__main_box = QtWidgets.QHBoxLayout()
        self.__main_box.set_contents_margins(0, 0, 0, 0)
        self.__main_box.set_spacing(0)
        self.set_layout(self.__main_box)

        # Side view
        self.__sideview_background = QtWidgets.QWidget()
        self.__sideview_background.set_fixed_width(
            self.__sideview_widget.width())
        self.__sideview_background.set_contents_margins(0, 0, 0, 0)
        self.__sideview_background.set_object_name('__sideviewbgstyle')
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
                    self.__top.close_sideview()

        self.__close_view_background = QtWidgets.QWidget()
        self.__close_view_background.set_contents_margins(0, 5, 5, 5)
        self.__close_view_background.set_object_name('__closeviewbgtyle')
        self.__main_box.add_widget(self.__close_view_background)

        self.__close_view_box = QtWidgets.QVBoxLayout()
        self.__close_view_box.set_contents_margins(0, 0, 0, 0)
        self.__close_view_background.set_layout(self.__close_view_box)
        self.__close_view_box.add_widget(CloseArea(self.__toplevel))

        self.__toplevel.resize_event_signal.connect(self.__resize_sig)
        self.__toplevel.shadow_visibility_signal.connect(
            self.__set_shadow_visible)

    def set_sideview_fixed_width(self, width: int) -> None:
        """..."""
        self.__sideview_background.set_fixed_width(width)

    def close(self) -> None:
        """..."""
        self.anim_close.set_start_value(
            QtCore.QSize(
                self.__toplevel.width() - 1, self.__toplevel.height()))
        self.anim_close.set_end_value(
            QtCore.QSize(
                5, self.__toplevel.height()))
        self.anim_close.set_duration(100)
        self.anim_close_group.add_animation(self.anim_close)
        self.anim_close_group.start()

        self.__close_timer.timeout.connect(self.__close)
        self.__close_timer.start(100)

    def __close(self):
        self.__close_timer.stop()
        self.__sideview_widget.set_visible(False)
        self.__sideview_box.remove_widget(self.__sideview_widget)
        self.__sideview_widget_box.insert_widget(0, self.__sideview_widget)
        self.set_visible(False)

    def open(self) -> None:
        """..."""
        if not self.__toplevel.is_server_side_decorated():
            self.__set_shadow_visible(self.__toplevel.is_shadow_visible())
        else:
            self.set_contents_margins(0, 0, 0, 0)

        self.__update_style()
        self.__sideview_widget.set_visible(True)
        self.resize(self.__toplevel.width(), self.__toplevel.height())
        self.__sideview_widget_box.remove_widget(self.__sideview_widget)
        self.__sideview_box.add_widget(self.__sideview_widget)
        self.set_visible(True)
        self.move(0, 0)

        self.anim_open.set_start_value(
            QtCore.QSize(50, self.__toplevel.height()))
        self.anim_open.set_end_value(
            QtCore.QSize(
                self.__toplevel.width() - 1, self.__toplevel.height()))
        self.anim_open.set_duration(40)
        self.anim_open_group.add_animation(self.anim_open)
        self.anim_open_group.start()

    def __update_style(self) -> None:
        # ...
        self.__style_parser.set_style_sheet(self.__toplevel.style_sheet())
        base_style = self.__style_parser.widget_scope('MainWindow')

        url = None
        for x in base_style.split(';'):
            if x.replace(' ', '').startswith('background:url('):
                url = x.strip().split('(')[1].split(')')[0]
            if url:
                break
        if url:
            sideview_texture = Image.open(url)
            sideview_texture.putalpha(245)
            url = url.replace('.png', 'sideview.png')
            sideview_texture.save(url)

        background = f'background: url({url});'
        self.__sideview_background.set_style_sheet(
            f'{self.__toplevel.style_sheet()}'
            '#__sideviewbgstyle {'
            f'{base_style}'
            f'{background}'
            'border-right: 0px; '
            'border-top-right-radius: 0;'
            'border-bottom-right-radius: 0;'
            'border: 0px;'
            '}')

        self.__close_view_background.set_style_sheet(
            '#__closeviewbgtyle {'
            f'{base_style}'
            # 'background-color: rgba(0, 0, 0, 0.1);'
            # 'color: qlineargradient('
            # '  spread:pad, '
            # '  x1:0 y1:0, x2:1 y2:0, '
            # '  stop:0 rgba(0, 0, 0, 255), '
            # '  stop:1 rgba(255, 255, 255, 255));'
            'background: qlineargradient('
            '  x1:0 y1:0, x2:1 y2:0,'
            '  stop:0.0 rgba(0, 0, 0, 50),'
            '  stop:0.4 rgba(0, 0, 0, 30),'
            '  stop:1.0 rgba(0, 0, 0, 30));'
            'border: 0px;'
            'border-top-left-radius: 0;'
            'border-bottom-left-radius: 0;}')

    def __resize_sig(self) -> None:
        self.resize(self.__toplevel.width(), self.__toplevel.height())

    def __set_shadow_visible(self, visible) -> None:
        if visible:
            self.set_contents_margins(
                self.__toplevel.shadow_size() + 1,
                self.__toplevel.shadow_size() + 1,
                self.__toplevel.shadow_size(),
                self.__toplevel.shadow_size() + 1)
        else:
            self.set_contents_margins(1, 1, 1, 1)


class ApplicationWindowSideView(ApplicationWindow):
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
        # Properties
        self.__gui_env = GuiEnv(
            self.platform().operational_system(),
            self.platform().desktop_environment())
        self.__minimum_width = 350
        self.__minimum_height = 200
        self.__border_size = 12
        self.__is_sideview_open = False
        self.__adaptive_mode_toggle_width = 650
        self.__is_adaptive_mode = False
        self.__is_sideview_headerbar_left_control_set_as_visible = True
        self.__is_sideview_close_button_set_as_visible = False
        self.__sideview_width = 250
        self.__sideview_color = self.__gui_env.settings(
            ).window_background_darker_color().to_tuple()

        # Settings
        self.set_window_title('MPX Application Window')
        self.set_minimum_width(self.__minimum_width)
        self.set_minimum_height(self.__minimum_height)
        self.resize(self.__initial_width(), 500)

        # Icon
        icon_path = os.path.join(
            pathlib.Path(__file__).resolve().parent, 'icon.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)

        # Main layout
        self.__main_box = QtWidgets.QHBoxLayout()
        self.__main_box.set_contents_margins(0, 0, 0, 0)
        self.__main_box.set_spacing(0)
        self.central_widget().set_layout(self.__main_box)

        # Side view
        self.__sideview_width_area = QtWidgets.QWidget()
        self.__sideview_width_area.set_object_name('__panelwidthstyle')
        self.__sideview_width_area.set_fixed_width(self.__sideview_width)
        self.__main_box.add_widget(self.__sideview_width_area, 9)

        self.__sideview_main_box = QtWidgets.QVBoxLayout()
        self.__sideview_main_box.set_contents_margins(0, 0, 0, 0)
        self.__sideview_main_box.set_alignment(QtCore.Qt.AlignTop)
        self.__sideview_width_area.set_layout(self.__sideview_main_box)

        # Side header bar
        self.__sideview_headerbar_box = QtWidgets.QHBoxLayout()
        self.__sideview_headerbar_box.set_spacing(0)
        self.__sideview_headerbar_box.set_contents_margins(0, 0, 6, 0)
        self.__sideview_main_box.add_layout(self.__sideview_headerbar_box)

        self.__sideview_headerbar = HeaderBar(self)
        self.__sideview_headerbar.set_right_control_buttons_visible(False)
        self.__sideview_headerbar_box.add_widget(self.__sideview_headerbar)

        self.__sideview_close_button = QtWidgets.QToolButton()
        self.__sideview_close_button.set_visible(False)
        self.__sideview_close_button.clicked.connect(self.close_sideview)
        self.__sideview_close_button.set_icon(
            QtGui.QIcon.from_theme('go-previous-symbolic'))
        self.__sideview_headerbar_box.add_widget(self.__sideview_close_button)

        # Side view layout
        self.__sideview_box = QtWidgets.QVBoxLayout()
        self.__sideview_box.set_spacing(6)
        self.__sideview_box.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__sideview_main_box.add_layout(self.__sideview_box)
        self.__color_sideview()

        # Frame view
        self.__frameview_main_box = QtWidgets.QVBoxLayout()
        self.__frameview_main_box.set_alignment(QtCore.Qt.AlignTop)
        self.__main_box.add_layout(self.__frameview_main_box)

        # Frame view header bar
        self.__frameview_headerbar = HeaderBar(self)
        self.__frameview_headerbar.set_left_control_buttons_visible(False)
        self.__frameview_main_box.add_widget(self.__frameview_headerbar)

        self.__sideview_open_button = QtWidgets.QToolButton()
        self.__sideview_open_button.set_icon(
            QtGui.QIcon.from_theme('sidebar-show-symbolic'))
        self.__sideview_open_button.clicked.connect(self.open_sideview)
        self.__frameview_headerbar.add_widget_to_left(
            self.__sideview_open_button)
        self.__sideview_open_button.set_visible(False)

        self.__frameview_box = QtWidgets.QVBoxLayout()
        self.__frameview_box.set_contents_margins(
            self.__border_size, 0, self.__border_size, self.__border_size)
        self.__frameview_main_box.add_layout(self.__frameview_box, 9)

        # Side view overlay
        self.__sideview_overlay = OverlaySideView(
            self.__sideview_width_area, parent=self)
        self.__sideview_overlay.set_visible(False)

        # Signals
        self.resize_event_signal.connect(self.__resize_event)
        self.set_style_signal.connect(lambda _: self.__color_sideview())
        self.reset_style_signal.connect(lambda _: self.__color_sideview())

    def close_sideview(self) -> None:
        """..."""
        if self.__is_sideview_open:
            self.__sideview_overlay.close()
            self.sideview_closed_signal.emit('sideview-closed-signal')
            self.__is_sideview_open = False

    def frameview_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__frameview_box

    def adaptive_mode_toggle_width(self) -> int:
        """..."""
        return self.__adaptive_mode_toggle_width

    def open_sideview(self) -> None:
        """..."""
        if not self.__is_sideview_open:
            self.__sideview_headerbar.set_left_control_buttons_visible(False)
            self.__sideview_overlay.open()
            self.sideview_opened_signal.emit('sideview-opened-signal')
            self.__is_sideview_open = True

    def sideview_color(self) -> tuple:
        """..."""
        return self.__sideview_color

    def sideview_headerbar(self) -> HeaderBar:
        """..."""
        return self.__sideview_headerbar

    def sideview_layout(self) -> QtWidgets.QVBoxLayout:
        """..."""
        return self.__sideview_box

    def set_close_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_close_window_button_visible(visible)
        self.__frameview_headerbar.set_close_window_button_visible(visible)

    def set_headerbar_icon(self, icon: QtGui.QIcon) -> None:
        """..."""
        self.set_window_icon(icon)
        self.__sideview_headerbar.set_window_icon(icon)
        self.__frameview_headerbar.set_window_icon(icon)

    def set_headerbar_title(self, text: str) -> None:
        """..."""
        self.__frameview_headerbar.set_text(text)

    def set_adaptive_mode_toggle_width(self, width: int) -> None:
        """..."""
        self.__adaptive_mode_toggle_width = width

    def set_left_control_buttons_visible(self, visible: bool) -> None:
        """..."""
        self.__is_sideview_headerbar_left_control_set_as_visible = visible
        self.__sideview_headerbar.set_left_control_buttons_visible(visible)

    def set_maximize_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_maximize_window_button_visible(visible)
        self.__frameview_headerbar.set_maximize_window_button_visible(
            visible)

    def set_minimize_window_button_visible(self, visible: bool) -> None:
        """..."""
        self.__sideview_headerbar.set_minimize_window_button_visible(visible)
        self.__frameview_headerbar.set_minimize_window_button_visible(
            visible)

    def set_sideview_close_button_visible(self, visible: bool) -> None:
        """Visibility of the side view close button

        The button to close the side view is only visible when the side view
        is in floating/overlay mode.

        :param visible: True to be visible. Default is False
        """
        self.__is_sideview_close_button_set_as_visible = visible

    def set_sideview_color(self, rgba_color: tuple | None) -> None:
        """..."""
        if not rgba_color:
            self.__sideview_color = self.__gui_env.settings(
                ).window_background_darker_color().to_tuple()
        else:
            self.__sideview_color = rgba_color

        self.__color_sideview()

    def set_sideview_fixed_width(self, width: int) -> None:
        """It's just a simple adjustment.

        The side view is not smaller than 150px or larger than the minimum
        window size (350px).

        :param width: Integer with the new side view width
        """
        if width < 150:
            width = 150
        elif width > self.__minimum_width - 50:
            width = self.__minimum_width - 50
        self.__sideview_width = width
        self.__sideview_width_area.set_fixed_width(self.__sideview_width)
        self.__sideview_overlay.set_sideview_fixed_width(self.__sideview_width)

    def set_right_control_buttons_visible(self, visible: bool) -> None:
        """..."""
        self.__frameview_headerbar.set_right_control_buttons_visible(visible)

    def __color_sideview(self) -> None:
        """..."""
        basestyle = StyleParser(self.style_sheet()).widget_scope('MainWindow')
        sideview_style_sheet = (
            '#__panelwidthstyle {'
            f'{basestyle}'
            'background: url();'
            'background-color: rgba('
            f'{self.__sideview_color[0]}, {self.__sideview_color[1]}, '
            f'{self.__sideview_color[2]}, {self.__sideview_color[3]});'
            'border: 0px;')

        if self.is_maximized():
            self.__sideview_width_area.set_style_sheet(
                f'{sideview_style_sheet}'
                'border-radius: 0;'
                'padding: 0px;'
                'margin: 0px;}')
        else:
            self.__sideview_width_area.set_style_sheet(
                f'{sideview_style_sheet}'
                'border-top-right-radius: 0;'
                'border-bottom-right-radius: 0;'
                'padding: 0px;'
                'margin: 0px;}')

    def __fullscreen_maximized_and_windowed_modes_adjusts(self) -> None:
        if self.is_maximized():
            if self.__gui_env.settings().desktop_is_using_global_menu():
                self.__sideview_headerbar.set_left_control_buttons_visible(
                    False)
                self.__color_sideview()

            if self.__is_sideview_open:
                self.close_sideview()
                self.__sideview_width_area.set_visible(True)

        elif self.is_full_screen():
            self.__sideview_headerbar.set_left_control_buttons_visible(False)
            self.__color_sideview()

            if self.__is_sideview_open:
                self.close_sideview()
                self.__sideview_width_area.set_visible(True)
        else:
            if self.__is_sideview_headerbar_left_control_set_as_visible:
                if not self.__is_sideview_open:
                    self.__sideview_headerbar.set_left_control_buttons_visible(
                        True)
            self.__color_sideview()

    def __initial_width(self) -> int:
        if self.screen().size().width() < self.__sideview_width < 500:
            return self.__minimum_width
        return 750

    def __sideview_was_closed_signal(self, event: QtCore.Signal) -> None:
        if self.__is_sideview_open:
            self.sideview_closed_signal.emit(event)
            self.__is_sideview_open = False

    def __switch_adaptive_and_wide_mode_window(self) -> None:
        # Vertical
        if (not self.__is_adaptive_mode and self.size().width() <
                self.__adaptive_mode_toggle_width):
            self.__is_adaptive_mode = True
            self.__switch_to_adaptive_mode()
            self.adaptive_mode_signal.emit('adaptive-mode-signal')

        # Horizontal
        elif (self.__is_adaptive_mode and self.size().width() >
              self.__adaptive_mode_toggle_width):
            self.__is_adaptive_mode = False
            self.__switch_to_wide_mode()
            self.wide_mode_signal.emit('wide-mode-signal')

    def __switch_to_adaptive_mode(self) -> None:
        self.__sideview_width_area.set_visible(False)
        if self.__is_sideview_headerbar_left_control_set_as_visible:
            self.__frameview_headerbar.set_left_control_buttons_visible(True)
        self.__sideview_open_button.set_visible(True)
        if self.__is_sideview_close_button_set_as_visible:
            self.__sideview_close_button.set_visible(True)

    def __switch_to_wide_mode(self) -> None:
        self.__sideview_width_area.set_visible(True)
        self.__frameview_headerbar.set_left_control_buttons_visible(False)
        self.__sideview_open_button.set_visible(False)
        self.__sideview_close_button.set_visible(False)

        if self.__is_sideview_open:
            self.close_sideview()
            self.__sideview_width_area.set_visible(True)

    def __resize_event(self, event: QtGui.QResizeEvent) -> None:
        logging.info(event)
        self.__switch_adaptive_and_wide_mode_window()
        self.__fullscreen_maximized_and_windowed_modes_adjusts()
