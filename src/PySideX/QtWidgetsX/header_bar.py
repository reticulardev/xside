#!/usr/bin/env python3
import logging

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.application_window import QApplicationWindow
from PySideX.QtWidgetsX.window_move_area import QWindowMoveArea
from PySideX.QtWidgetsX.window_control_buttons import QWindowControlButtons
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv


class QHeaderBar(QtWidgets.QFrame):
    """Window header bar

    Replaces traditional title bar and allows adding and editing widgets
    """
    resize_event_signal = QtCore.Signal(object)

    def __init__(self, toplevel: QApplicationWindow, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param toplevel: QApplicationWindow app main window instance
        :param window_control_buttons_on_left:
            window control buttons (minimize, maximize and close) on left
        :param window_control_buttons_order:
            Tuple with the order of the buttons. 0 is the minimize button, 1 is
            the maximize button and 2 is the close button. Default is (0, 1, 2)
        """
        super().__init__(*args, **kwargs)
        self.__toplevel = toplevel
        self.__left_ctrl_buttons_visibility = True
        self.__right_ctrl_buttons_visibility = True

        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment())

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

        self.__window_move_area = QWindowMoveArea(self.__toplevel)
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
            self.__toplevel, side='left')
        self.__bar_item_layout_left.add_widget(self.__left_ctrl_buttons)

        self.__right_ctrl_buttons = QWindowControlButtons(
            self.__toplevel, side='right')
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

        if self.__toplevel.is_server_side_decorated():
            self.__left_ctrl_buttons.set_visible(False)
            self.__right_ctrl_buttons.set_visible(False)
            _50_percent_left = self.__50_percent_left_size(True)
        else:
            _50_percent_left = self.__50_percent_left_size(False)

            if self.__toplevel.is_maximized():
                if self.__gui_env.settings().desktop_is_using_global_menu():
                    self.__left_ctrl_buttons.set_visible(False)
                    self.__right_ctrl_buttons.set_visible(False)
                    _50_percent_left = self.__50_percent_left_size(True)

            elif self.__toplevel.is_full_screen():
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
        if not self.__toplevel.is_server_side_decorated():
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
