#!/usr/bin/env python3
from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.control_button import QControlButton
from PySideX.QtWidgetsX.application_window import QApplicationWindow


class QWindowControlButtons(QtWidgets.QFrame):
    """window control buttons

    Contains minimize, maximize and close buttons
    """

    def __init__(
            self, main_window: QApplicationWindow,
            button_order: tuple = (0, 1, 2),
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
