#!/usr/bin/env python3
import logging
import os
import pathlib

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case


SRC_DIR = os.path.dirname(os.path.abspath(__file__))


class QQuickContextMenuButton(QtWidgets.QFrame):
    """..."""
    def __init__(
            self,
            parent_window: QtWidgets,
            parent_context_menu: QtWidgets,
            text: str,
            receiver: callable,
            icon: QtGui.QIcon | None = None,
            shortcut: QtGui.QKeySequence | None = None,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.set_contents_margins(0, 0, 0, 0)

        self.__parent_window = parent_window
        self.__parent = parent_context_menu
        self.__text = text
        self.__receiver = receiver
        self.__icon = icon
        self.__shortcut = shortcut

        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_spacing(0)
        self.set_layout(self.__main_layout)

        self.__left_layout = QtWidgets.QHBoxLayout()
        self.__left_layout.set_alignment(QtCore.Qt.AlignLeft)
        self.__main_layout.add_layout(self.__left_layout)

        if not self.__icon:
            symbolic = ''
            if self.__parent_window.platform_settings().is_dark_widget(self):
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
        self.__parent.close()
