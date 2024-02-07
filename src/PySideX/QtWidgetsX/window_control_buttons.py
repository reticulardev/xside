#!/usr/bin/env python3
from PySide6 import QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.control_button import QControlButton
from PySideX.QtWidgetsX.application_window import QApplicationWindow
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv


class QWindowControlButtons(QtWidgets.QFrame):
    """window control buttons

    Contains minimize, maximize and close buttons
    """

    def __init__(
            self, toplevel: QApplicationWindow,
            button_order: tuple = None,
            side: str = 'right',
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes.
        In the button order parameter, each number represents a type of button:
            0 is the minimize button
            1 is the maximize button
            2 is the close button
            3 is window icon

        :param toplevel: Main window instance
        :param button_order:
            Tuple with the order of the buttons. Default is (0, 1, 2).
            If defined, the 'side' parameter will be ignored.
        :param side:
            The values are 'left' or 'right'.
            Try setting the buttons to the right or left of the window.
            Will be ignored if parameter 'button_order' is defined.
        """
        # Param
        super().__init__(*args, **kwargs)
        self.__toplevel = toplevel
        self.__button_order = button_order
        self.__side = side

        # Flags
        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment())

        self.__env_btn_order = self.__gui_env.settings().controlbutton_order()
        self.__left_system_button_order = self.__env_btn_order[0]
        self.__right_system_button_order = self.__env_btn_order[1]
        self.__set_button_order()

        self.__window_icon = QtWidgets.QLabel()
        self.__window_icon.set_pixmap(
            self.__toplevel.window_icon().pixmap(20))
        margin = self.__gui_env.settings().window_icon_margin()
        self.__window_icon.set_contents_margins(
            margin[0], margin[1], margin[2], margin[3])

        self.__layout = QtWidgets.QHBoxLayout(self)
        self.__layout.set_contents_margins(2, 0, 2, 0)

        self.__minimize_button = QControlButton(self.__toplevel, 0)
        self.__maximize_button = QControlButton(self.__toplevel, 1)
        self.__close_button = QControlButton(self.__toplevel, 2)

        self.__add_buttons_in_order()

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

    def __set_button_order(self):
        if not self.__button_order:
            if self.__side == 'left':
                self.__button_order = self.__left_system_button_order
            else:
                self.__button_order = self.__right_system_button_order

    def __add_buttons_in_order(self) -> None:
        # Add the buttons in the configured order
        buttons_dict = {
            0: self.__minimize_button,
            1: self.__maximize_button,
            2: self.__close_button,
            3: self.__window_icon}
        if self.__button_order:
            for index in self.__button_order:
                self.__layout.add_widget(buttons_dict[index])
