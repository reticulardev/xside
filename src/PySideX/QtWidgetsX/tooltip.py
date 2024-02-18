#!/usr/bin/env python3
import logging
import os

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.applicationwindow import QApplicationWindow
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv
from PySideX.QtWidgetsX.modules.dynamicstyle import StyleParser
import PySideX.QtWidgetsX.modules.color as color


class QTooltip(QtWidgets.QFrame):
    """..."""
    def __init__(
            self,
            toplevel: QApplicationWindow,
            parent: QtWidgets.QWidget,
            text: str,
            shortcut: QtGui.QKeySequence | None = None,
            *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param toplevel: QApplicationWindow app main window instance
        """
        super().__init__(*args, **kwargs)
        self.__toplevel = toplevel
        self.__parent = parent
        self.__shortcut = f'({shortcut.to_string()})' if shortcut else ''

        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment())

        self.__is_dark = self.__gui_env.settings().window_is_dark()
        self.__style_saved = self.__toplevel.style_sheet()
        self.__style_parser = StyleParser(self.__style_saved)

        # Main layout
        self.__main_box = QtWidgets.QHBoxLayout()
        self.set_layout(self.__main_box)

        self.__main_widget = QtWidgets.QFrame()
        self.__main_widget.set_object_name('QTooltip')
        self.__main_box.add_widget(self.__main_widget)

        # Layout
        self.__body_box = QtWidgets.QVBoxLayout()
        self.__body_box.set_contents_margins(0, 0, 0, 0)
        self.__main_widget.set_layout(self.__body_box)

        # Label box
        self.__label_box = QtWidgets.QHBoxLayout()
        self.__label_box.set_contents_margins(0, 0, 0, 0)
        self.__label_box.set_alignment(QtCore.Qt.AlignLeft)
        self.__body_box.add_layout(self.__label_box)

        self.__label = QtWidgets.QLabel(text)
        self.__label_box.add_widget(self.__label)

        self.__shortcut_label = QtWidgets.QLabel(self.__shortcut)
        self.__shortcut_label.set_enabled(False)
        self.__label_box.add_widget(self.__shortcut_label)

        self.__body_box.add_widget(QtWidgets.QLabel('test test test...'))

        # Shadow
        self.__shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self)
        self.__shadow_effect.set_blur_radius(5)
        self.__shadow_effect.set_offset(QtCore.QPointF(0.0, 0.0))

        if self.__is_dark:
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 100))
        else:
            self.__shadow_effect.set_color(QtGui.QColor(10, 10, 10, 70))
        self.__main_widget.set_graphics_effect(self.__shadow_effect)

        self.__toplevel.set_style_signal.connect(self.__set_style_signal)
        self.__toplevel.reset_style_signal.connect(self.__set_style_signal)
        self.set_mouse_tracking(True)

    def exec(self) -> None:
        """..."""
        self.__main_widget.set_style_sheet(self.__set_style())
        point = QtGui.QCursor.pos()
        self.move(
            point.x() + self.__parent.x(),
            point.y() + (self.__parent.y() + self.__parent.height()))
        self.show()

    def mouse_move_event(self, event: QtGui.QMouseEvent) -> None:
        logging.info(event)
        self.close()

    def __set_dynamic_positioning(self) -> None:
        # ...
        x = self.geometry().x()
        y = self.geometry().y()
        screen_width = self.__toplevel.screen().geometry().width()
        screen_height = self.__toplevel.screen().geometry().height()

        if self.geometry().x() + self.geometry().width() > screen_width:
            x = screen_width - self.geometry().width()

        if self.geometry().y() + self.geometry().height() > screen_height:
            y = self.geometry().y() - self.geometry().height() + 20

        self.move(x, y)

    def __set_style_signal(self) -> None:
        # ...
        self.__style_saved = self.__toplevel.style_sheet()
        self.__style_parser.set_style_sheet(self.__style_saved)

    def __set_style(self) -> str:
        # ...
        if not self.__style_saved:
            self.__set_style_signal()

        return ('#QTooltip {'
                f'{self.__style_parser.widget_scope("QQuickContextMenu")}' '}')
