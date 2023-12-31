#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from PySideX import QtWidgetsX
from __feature__ import snake_case

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class Window(QtWidgetsX.QApplicationWindow):
    """App window instance"""

    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes.
        """
        super().__init__(*args, **kwargs)
        # title
        self.set_window_title('My app')

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(app_icon)

        # Size
        self.set_minimum_height(500)
        self.set_minimum_width(500)

        # Main layout -> Central widget
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.set_contents_margins(0, 0, 0, 0)
        self.main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.central_widget().set_layout(self.main_layout)

        self.headerbar = QtWidgetsX.QHeaderBar(self)
        self.main_layout.add_widget(self.headerbar)
        self.headerbar.set_text(self.window_title())

        self.search_button = QtWidgets.QToolButton()
        self.search_button.set_icon(QtGui.QIcon.from_theme('search'))
        self.headerbar.add_widget_to_left(self.search_button)

        self.trash_button = QtWidgets.QToolButton()
        self.trash_button.set_icon(QtGui.QIcon.from_theme('trash-empty'))
        self.headerbar.add_widget_to_left(self.trash_button)

        self.menu_button = QtWidgets.QToolButton()
        self.menu_button.set_icon(QtGui.QIcon.from_theme('application-menu'))
        self.headerbar.add_widget_to_right(self.menu_button)

        self.body_layout = QtWidgets.QVBoxLayout()
        self.body_layout.set_contents_margins(6, 0, 6, 6)
        self.body_layout.set_alignment(QtCore.Qt.AlignTop)
        self.main_layout.add_layout(self.body_layout)

        self.set_style_button = QtWidgets.QPushButton('Set custom style')
        self.set_style_button.clicked.connect(self.on_set_style)
        self.body_layout.add_widget(self.set_style_button)

        self.reset_style_button = QtWidgets.QPushButton('Reset style')
        self.reset_style_button.clicked.connect(self.on_reset_style)
        self.body_layout.add_widget(self.reset_style_button)

    def on_set_style(self):
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_style_sheet(
            'QApplicationWindow {'
            '   background-color: rgba(59, 59, 59, 0.8);'
            '   border-radius: 10px;'
            '   border: 1px solid #555;}'
            'QPushButton {'
            '   background-color: #363636;}'
            'QPushButton:hover {'
            '   background-color: #513258;}'
            'QToolButton {'
            '   background-color: rgba(80, 80, 80, 0.6);'
            '   padding: 5px;'
            '   border-radius: 5px;'
            '   border: 0px;}'
            'QToolButton:hover {'
            '   background: transparent;'
            '   border: 0px;'
            '   background-color: rgba(125, 77, 136, 0.6);}'
            'QControlButton {'
            '   padding: 0px;'
            '   background: transparent;'
            '   border-radius: 9px;}'
            'QControlButton:hover {'
            '   background-color: rgba(100, 100, 100, 0.5);}')

    def on_reset_style(self):
        self.reset_style()


class Application(object):
    """..."""
    def __init__(self, args: list) -> None:
        """Class constructor

        Initialize class attributes.

        :param args: List of command line arguments
        """
        self.application = QtWidgets.QApplication(args)
        self.window = Window(is_decorated=False, platform=True)

    def main(self) -> None:
        """Start the app

        Sets basic window details and starts the application.
        """
        self.window.show()
        sys.exit(self.application.exec())


if __name__ == '__main__':
    app = Application(sys.argv)
    app.main()
