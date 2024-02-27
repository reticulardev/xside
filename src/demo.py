#!/usr/bin/env python3
import logging
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from PySideX import QtWidgetsX
from __feature__ import snake_case

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class SideViewWindow(QtWidgetsX.QApplicationWindowSideView):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        # self.set_minimize_window_button_visible(False)
        # self.set_maximize_window_button_visible(False)
        # self.set_close_window_button_visible(False)
        # self.set_right_control_buttons_visible(False)

        # Icon
        icon_path = os.path.join(SRC_DIR, 'icon_b.svg')
        self.__app_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(self.__app_icon)
        self.set_headerbar_icon(self.__app_icon)

        # Title
        self.set_window_title("My custom MPX app")
        self.set_headerbar_title(self.window_title())

        # Search
        self.tbutton = QtWidgets.QToolButton()  # edit-find-symbolic
        self.tbutton.set_icon(QtGui.QIcon.from_theme('system-search-symbolic'))
        self.sideview_headerbar().add_widget_to_right(self.tbutton)

        for i in ['Download', 'Pictures', 'Documents', 'Videos', 'Music']:
            btn = QtWidgets.QPushButton(i)
            btn.clicked.connect(self.on_btn)
            self.sideview_layout().add_widget(btn)

        # Image
        self.image = QtWidgets.QLabel()
        self.image.set_pixmap(
            QtGui.QIcon.from_theme('folder-download-symbolic').pixmap(96, 96))
        self.frameview_layout().add_widget(self.image)
        self.frameview_layout().set_alignment(QtCore.Qt.AlignCenter)

        # Image: context menu
        self.image_qcontext = QtWidgetsX.QQuickContextMenu(self)
        self.image_qcontext.add_action(
            'Delete', lambda: self.__context_menu_cal('Delete'))
        self.image_qcontext.add_action(
            'Save', lambda: self.__context_menu_cal('Save'))

        self.image.set_context_menu_policy(QtGui.Qt.CustomContextMenu)
        self.image.customContextMenuRequested.connect(
            self.context_menu_for_image)

        # Style button
        self.set_style_button = QtWidgets.QPushButton('Set style')
        self.set_style_button.clicked.connect(self.on_set_style_button)
        self.frameview_layout().add_widget(self.set_style_button)

        # self.sideview_opened_signal.connect(lambda event: print(event))
        # self.sideview_closed_signal.connect(lambda event: print(event))
        # self.adaptive_mode_signal.connect(lambda event: print(event))
        # self.wide_mode_signal.connect(lambda event: print(event))

        # Text  and their context menu (Global: use context_menu_event)
        self.context_menu_label = QtWidgets.QLabel('Menu text here')
        self.frameview_layout().add_widget(self.context_menu_label)

        self.qcontext_menu = QtWidgetsX.QQuickContextMenu(
            self, quick_action_label_as_tooltip=True, force_quick_mode=True)
        self.qcontext_menu.add_action(
            'Copy', lambda: self.__context_menu_cal('Copy'),
            icon=QtGui.QIcon.from_theme('edit-copy-symbolic'),
            shortcut=QtGui.QKeySequence('Ctrl+C'), is_quick_action=True)
        self.qcontext_menu.add_action(
            'Cut', lambda: self.__context_menu_cal('Cut'),
            icon=QtGui.QIcon.from_theme('edit-cut-symbolic'),
            shortcut=QtGui.QKeySequence('Ctrl+X'), is_quick_action=True)
        self.qcontext_menu.add_action(
            'Paste', lambda: self.__context_menu_cal('Paste'),
            icon=QtGui.QIcon.from_theme('edit-paste-symbolic'),
            shortcut=QtGui.QKeySequence('Ctrl+V'), is_quick_action=True)
        self.qcontext_menu.add_action(
            'Rename', lambda: self.__context_menu_cal('Rename'),
            icon=QtGui.QIcon.from_theme('document-edit-symbolic'),
            shortcut=QtGui.QKeySequence('F2'), is_quick_action=True)
        self.qcontext_menu.add_action(
            'Terminal', lambda: self.__context_menu_cal('Terminal'),
            icon=QtGui.QIcon.from_theme('dialog-scripts-symbolic'),
            shortcut=QtGui.QKeySequence('Alt+Shift+F4'))
        self.qcontext_menu.add_action(
            'Open', lambda: self.__context_menu_cal('Open'),
            icon=QtGui.QIcon.from_theme('document-open-symbolic'),
            shortcut=QtGui.QKeySequence('Ctrl+V'))

        self.qcontext_menu.add_separator()
        # self.qcontext_menu.set_separators_margins(8, 0, 8, 0)

        self.qcontext_menu.add_group('color', 'Change color:')
        self.qcontext_menu.add_separator()
        self.qcontext_menu.add_group_action(
            'color', 'RED', lambda: self.__context_menu_cal('RED'),
            icon=QtGui.QIcon('red.png'))
        self.qcontext_menu.add_group_action(
            'color', 'GREEN', lambda: self.__context_menu_cal('GREEN'),
            icon=QtGui.QIcon('green.png'))
        self.qcontext_menu.add_group_action(
            'color', 'BLUE', lambda: self.__context_menu_cal('BLUE'),
            icon=QtGui.QIcon('blue.png'))
        self.qcontext_menu.add_group_action(
            'color', 'More', lambda: self.__context_menu_cal('More'),
            icon=QtGui.QIcon.from_theme('list-add-symbolic'))

        self.qcontext_menu.add_action(
            'Delete', lambda: self.__context_menu_cal('Delete'))
        self.qcontext_menu.add_action(
            'Save', lambda: self.__context_menu_cal('Save'))

        # self.set_sideview_close_button_visible(True)
        # self.set_sideview_fixed_width(500)
        # self.qcontext_menu.set_contents_paddings(1, 6, 1, 6)

    def context_menu_event(self, event):
        self.qcontext_menu.exec(event.global_pos())

    def context_menu_for_image(self):
        self.image_qcontext.exec(QtGui.QCursor.pos())

    def __context_menu_cal(self, text):
        self.context_menu_label.set_text(text)

    def on_set_style_button(self) -> None:
        color = self.palette().color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)
        accent_color = "#{:02x}{:02x}{:02x}".format(
            color.red(), color.green(), color.blue())
        if self.set_style_button.text() == 'Set style':
            self.set_sideview_color((0, 0, 0, 0.1))
            self.set_style_sheet(
                'QMainWindow {'
                '  background-color: rgba(44, 44, 50, 0.9);'
                '  border: 1px solid #283690;'
                '  border-radius: 10px;}'
                'QToolButton {'
                '  background: transparent;'
                '  padding: 2px;'
                '  border: 0px;'
                '  border-radius: 3px;'
                '  background-color: rgba(100, 100, 100, 0.2);}'
                'QToolButton:hover {'
                '  background: transparent;'
                '  background-color: rgba(100, 100, 100, 0.3);}'
                'QQuickContextMenu {'
                '  padding: 4;'
                '  background-color: rgba(44, 44, 50, 0.9);'
                '  border: 1px solid #283690;}'
                'QQuickContextMenuButton:hover {'
                '  border: 1px solid green;'
                '  background-color: darkgreen;}'
                'QQuickContextMenuButtonLabel {'
                '  color: white;}'
                'QQuickContextMenuButtonLabel:hover {'
                '  color: yellow;}'
                'QPushButton {'
                '  background-color: #363636;}'
                'QPushButton:hover {'
                f' background-color: {accent_color};' + '}')
            self.set_style_button.set_text('Reset style')
        else:
            self.reset_style()
            self.set_style_button.set_text('Set style')

    def on_btn(self) -> None:
        self.image.set_pixmap(QtGui.QIcon.from_theme(
            f'folder-{self.sender().text().lower()}-symbolic').pixmap(96, 96))
        self.close_sideview()


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

        # Context menu
        self.context_menu_label = QtWidgets.QLabel('Context menu text here')
        self.body_layout.add_widget(self.context_menu_label)

        self.ctx_menu = QtWidgetsX.QQuickContextMenu(self)
        self.ctx_menu.add_action(
            'Copy', lambda: self.context_menu_cal('Copy'),
            icon=QtGui.QIcon.from_theme('edit-copy'),
            shortcut=QtGui.QKeySequence('Ctrl+Shift+C'))
        self.ctx_menu.add_action(
            'Paste', lambda: self.context_menu_cal('Paste'),
            icon=QtGui.QIcon.from_theme('edit-paste'),
            shortcut=QtGui.QKeySequence('Ctrl+V'))

        self.ctx_menu.add_separator()
        # self.ctx_menu.set_contents_paddings(10, 10, 10, 10)
        # self.ctx_menu.set_spacing(5)
        # self.ctx_menu.set_separators_margins(10, 0, 10, 0)

        self.ctx_menu.add_action(
            'Delete', lambda: self.context_menu_cal('Delete'))
        self.ctx_menu.add_action(
            'Save', lambda: self.context_menu_cal('Save'))

    def context_menu_event(self, event):
        self.ctx_menu.exec(event.global_pos())

    def context_menu_cal(self, text):
        self.context_menu_label.set_text(text)

    def on_set_style(self):
        self.set_style_sheet(
            'QMainWindow {'
            '  background-color: rgba(59, 59, 59, 0.8);'
            '  border-radius: 10px;'
            '  border: 1px solid #555;'
            '}'
            'QPushButton {'
            '  background-color: #363636;}'
            'QPushButton:hover {'
            '  background-color: #513258;'
            '}'
            'QToolButton {'
            '  background-color: rgba(80, 80, 80, 0.6);'
            '  padding: 5px;'
            '  border-radius: 5px;'
            '  border: 0px;}'
            'QToolButton:hover {'
            '  background: transparent;'
            '  border: 0px;'
            '  background-color: rgba(125, 77, 136, 0.6);'
            '}'
            'QControlButton {'
            '  padding: 0px;'
            '  background: transparent;'
            '  border-radius: 9px;}'
            'QControlButton:hover {'
            '  padding: 0px;'
            '  background: transparent;'
            '  border-radius: 9px;'
            '  background-color: rgba(100, 100, 100, 0.5);'
            '}'
            'QQuickContextMenu {'
            '  border: 1px solid #0000FF;'
            '}'
            'QQuickContextMenuButton {'
            '  border: 1px solid #FF0000;'
            '}'
            'QQuickContextMenuButtonLabel {color: #FF0000;}')

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
        self.sideview_window = SideViewWindow(
            server_side_decoration=False, follow_platform=True)
        self.window = Window()
        # self.appwindow = CSDWindow()

    def main(self) -> None:
        """Start the app

        Sets basic window details and starts the application.
        """
        self.sideview_window.show()
        print(hex(self.sideview_window.win_id()), '<<<<')
        # self.window.show()
        sys.exit(self.application.exec())


if __name__ == '__main__':
    app = Application(sys.argv)
    app.main()
