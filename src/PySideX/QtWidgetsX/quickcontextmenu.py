#!/usr/bin/env python3
import logging
import os

from PySide6 import QtCore, QtGui, QtWidgets
from __feature__ import snake_case

from PySideX.QtWidgetsX.applicationwindow import QApplicationWindow
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv
from PySideX.QtWidgetsX.modules.dynamicstyle import StyleParser
import PySideX.QtWidgetsX.modules.color as color


SRC_DIR = os.path.dirname(os.path.abspath(__file__))


class QQuickContextMenuSeparatorLine(QtWidgets.QFrame):
    """..."""
    def __init__(self, color: QtGui.QColor, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__color = color
        self.set_frame_shape(QtWidgets.QFrame.HLine)
        self.set_frame_shadow(QtWidgets.QFrame.Plain)
        self.set_line_width(0)
        self.set_mid_line_width(3)
        self.set_color(self.__color)

    def set_color(self, color: QtGui.QColor) -> None:
        """..."""
        palette = self.palette()
        palette.set_color(QtGui.QPalette.WindowText, color)
        self.set_palette(palette)


class QQuickContextMenuSeparator(QtWidgets.QFrame):
    """..."""
    def __init__(self, color: QtGui.QColor, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__color = color
        box = QtWidgets.QVBoxLayout()
        box.set_contents_margins(0, 0, 0, 0)
        self.set_layout(box)

        line = QQuickContextMenuSeparatorLine(self.__color)
        line.set_contents_margins(0, 0, 0, 0)
        box.add_widget(line)


class QQuickContextMenuButtonLabel(QtWidgets.QLabel):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """..."""


class QQuickContextMenuButton(QtWidgets.QFrame):
    """..."""
    enter_event_signal = QtCore.Signal(object)
    leave_event_signal = QtCore.Signal(object)
    mouse_press_event_signal = QtCore.Signal(object)
    mouse_release_event_signal = QtCore.Signal(object)

    def __init__(
            self,
            toplevel: QApplicationWindow,
            context_menu: QtWidgets.QWidget,
            text: str,
            receiver: callable,
            icon: QtGui.QIcon | None = None,
            shortcut: QtGui.QKeySequence | None = None,
            gui_env=None,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__toplevel = toplevel
        self.__context_menu = context_menu
        self.__text = text
        self.__receiver = receiver
        self.__icon = icon
        self.__shortcut = shortcut
        self.__gui_env = gui_env

        self.__shortcut_color = self.__gui_env.settings().text_disabled_color()
        self.__is_dark = self.__gui_env.settings().window_is_dark()

        self.__style_parser = StyleParser(self.__toplevel.style_sheet())
        self.__normal_style = self.__updated_normal_style()
        self.__hover_style = self.__updated_hover_style()
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__main_layout.set_contents_margins(0, 0, 0, 0)
        self.__main_layout.set_spacing(0)
        self.set_layout(self.__main_layout)

        self.__left_layout = QtWidgets.QHBoxLayout()
        self.__left_layout.set_alignment(QtCore.Qt.AlignLeft)
        self.__main_layout.add_layout(self.__left_layout)

        self.__configure_icon()
        icon_label = QtWidgets.QLabel()
        icon_label.set_pixmap(self.__icon.pixmap(QtCore.QSize(16, 16)))
        icon_label.set_contents_margins(0, 0, 5, 0)
        icon_label.set_alignment(QtCore.Qt.AlignLeft)
        self.__left_layout.add_widget(icon_label)

        self.__text_label = QQuickContextMenuButtonLabel(self.__text)
        self.__text_label.set_alignment(QtCore.Qt.AlignLeft)
        self.__left_layout.add_widget(self.__text_label)

        txt_shortcut = self.__shortcut.to_string() if self.__shortcut else ' '
        shortcut_label = QtWidgets.QLabel(txt_shortcut)

        shortcut_label.set_style_sheet(
            'color: rgba('
            f'{self.__shortcut_color.red()},'
            f'{self.__shortcut_color.green()},'
            f'{self.__shortcut_color.blue()},'
            f'{self.__shortcut_color.alpha_f()});')
        shortcut_label.set_contents_margins(20, 0, 0, 0)
        shortcut_label.set_alignment(QtCore.Qt.AlignRight)
        self.__main_layout.add_widget(shortcut_label)

        self.__toplevel.set_style_signal.connect(self.__set_style_signal)
        self.__toplevel.reset_style_signal.connect(self.__set_style_signal)

    def text(self) -> str:
        """..."""
        return self.__text

    def __configure_icon(self):
        # ...
        if not self.__icon:
            symblc = '-symbolic' if self.__is_dark else ''
            icon_path = os.path.join(
                SRC_DIR, 'modules', 'static', f'context-menu-item{symblc}.svg')
            self.__icon = QtGui.QIcon(QtGui.QPixmap(icon_path))

    def __updated_hover_style(self) -> str:
        # ...
        updated_hover_style = self.__style_parser.widget_scope(
            'QQuickContextMenuButtonLabel', 'hover')
        if not updated_hover_style:
            fg = self.__gui_env.settings(
                ).contextmenubutton_foreground_hover_color()
            return (
                'color: rgba'
                f'({fg.red()}, {fg.green()}, {fg.blue()}, {fg.alpha()});')

        return updated_hover_style

    def __updated_normal_style(self) -> str:
        # ...
        updated_normal_style = self.__style_parser.widget_scope(
            'QQuickContextMenuButtonLabel')
        if not updated_normal_style:
            fg = self.__gui_env.settings().window_foreground_color()
            return (
                'color: rgba'
                f'({fg.red()}, {fg.green()}, {fg.blue()}, {fg.alpha()});')

        return updated_normal_style

    def __set_style_signal(self) -> None:
        # ...
        self.__style_parser.set_style_sheet(self.__toplevel.style_sheet())
        self.__normal_style = self.__updated_normal_style()
        self.__hover_style = self.__updated_hover_style()
        self.__text_label.set_style_sheet(self.__normal_style)

    def enter_event(self, event: QtGui.QEnterEvent) -> None:
        """..."""
        self.enter_event_signal.emit(event)
        self.__text_label.set_style_sheet(self.__hover_style)

    def leave_event(self, event: QtGui.QEnterEvent) -> None:
        """..."""
        self.leave_event_signal.emit(event)
        self.__text_label.set_style_sheet(self.__normal_style)

    def mouse_press_event(self, event: QtGui.QMouseEvent) -> None:
        self.mouse_press_event_signal.emit(event)

    def mouse_release_event(self, event: QtGui.QMouseEvent) -> None:
        """..."""
        self.mouse_release_event_signal.emit(event)
        if self.under_mouse():
            self.__receiver()
            self.__text_label.set_style_sheet(self.__normal_style)
            self.__context_menu.close()


class QQuickContextMenu(QtWidgets.QFrame):
    """..."""

    def __init__(self, toplevel: QtWidgets.QWidget, *args, **kwargs) -> None:
        """Class constructor

        Initialize class attributes

        :param toplevel: QApplicationWindow app main window instance
        """
        super().__init__(*args, **kwargs)
        self.__toplevel = toplevel

        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_window_flags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.set_minimum_width(50)
        self.set_minimum_height(35)

        self.__gui_env = GuiEnv(
            self.__toplevel.platform().operational_system(),
            self.__toplevel.platform().desktop_environment())

        self.__is_dark = self.__gui_env.settings().window_is_dark()
        self.__style_saved = self.__toplevel.style_sheet()
        self.__style_parser = StyleParser(self.__style_saved)
        self.__context_separators = []
        self.__context_buttons = []
        self.__point_x = None
        self.__point_y = None

        # Main layout
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.set_layout(self.__main_layout)

        self.__main_widget = QtWidgets.QFrame()
        self.__main_widget.set_object_name('QQuickContextMenu')
        self.__main_layout.add_widget(self.__main_widget)

        # Layout
        self.__menu_context_layout = QtWidgets.QVBoxLayout()
        self.__menu_context_layout.set_contents_margins(0, 0, 0, 0)
        self.__menu_context_layout.set_spacing(0)
        self.__main_widget.set_layout(self.__menu_context_layout)

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

    def add_action(
            self,
            text: str,
            receiver: callable,
            icon: QtGui.QIcon | None = None,
            shortcut: QtGui.QKeySequence | None = None) -> None:
        """..."""
        labels_box = QtWidgets.QHBoxLayout()
        # self.__labels_box.append(labels_box)

        ctx_btn = QQuickContextMenuButton(
            self.__toplevel, self, text, receiver, icon, shortcut,
            self.__gui_env)
        ctx_btn.set_style_sheet(self.__style_saved)
        labels_box.add_widget(ctx_btn)

        self.__menu_context_layout.add_layout(labels_box)

        # self.__context_buttons_layout.append(labels_box)
        self.__context_buttons.append(ctx_btn)

    def add_separator(self, color: QtGui.QColor = None) -> None:
        """..."""
        color = color if color else self.__gui_env.settings(
            ).contextmenu_separator_color()

        separator_layout = QtWidgets.QVBoxLayout()
        separator = QQuickContextMenuSeparator(color)
        separator_layout.add_widget(separator)

        self.__menu_context_layout.add_layout(separator_layout)
        self.__context_separators.append(separator)

    def exec(self, point: QtCore.QPoint) -> None:
        """..."""
        self.__point_x = point.x()
        self.__point_y = point.y()

        self.__main_widget.set_style_sheet(self.__set_style())
        for btn in self.__context_buttons:
            btn.set_style_sheet(self.__style_saved)

        for sep in self.__context_separators:
            sep.set_style_sheet(self.__style_saved)

        self.move(self.__point_x - 10, self.__point_y - 10)
        self.show()
        self.__set_dynamic_positioning()

    def mouse_press_event(self, event: QtGui.QMouseEvent) -> None:
        """..."""
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
            y = self.geometry().y() - self.geometry().height() + 10

        self.move(x, y)

    def __set_style_signal(self) -> None:
        # ...
        self.__style_saved = self.__toplevel.style_sheet()
        self.__style_parser.set_style_sheet(self.__style_saved)

    def __set_style(self) -> str:
        # ...
        if not self.__style_saved:
            self.__set_style_signal()

        return ('#QQuickContextMenu {'
                f'{self.__style_parser.widget_scope("QQuickContextMenu")}' '}')
