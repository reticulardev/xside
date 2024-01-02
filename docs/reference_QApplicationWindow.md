# QApplicationWindow

Inherits from [QMainWindow](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QMainWindow.html)

![Image](img/min_window.png "screenshot")

## Overview
The main window of an application.

It was built under [QMainWindow](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QMainWindow.html) 
and some modifications were made to achieve the CSD feature. 

## Class signature

<pre><small>QApplicationWindow(is_decorated: bool = False, platform: bool = True)</small></pre>

### Parameters
  - **is_decorated**: Type `bool`, default is `False`

    Use `False` if it is an undecorated **CSD** window and `True` if it is 
server-side decorated.


  - **platform**: Type `bool`, default is `True`

    The default is `True`, which is used to follow the user's platform style. 
These are the control button styles, color and shape of the window borders. 
Setting `False` will make the window use an alternative default style.

## Class methods

Only new ones. See the 
[**QMainWindow** documentation](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QMainWindow.html) 
for more.

- [central_widget](#central_widget)

- [is_decorated](#is_decorated)

- [platform_settings](#platform_settings)

- [reset_style](#reset_style)

### central_widget

Signature: `central_widget() -> QWidget`

A pre-configured [QWidget](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html). 
Is a central part of the **QApplicationWindow**. The main 
layout of your application must be added to it.

```python
self.layout = QtWidgets.QVBoxLayout()
self.central_widget().set_layout(self.layout)
```

---

### is_decorated
Signature: `is_decorated() -> bool`

Returns `False` if it is an undecorated **CSD** window and `True` if it is 
server-side decorated.

---

### platform_settings

Signature: `platform_settings() -> PlatformSettings`

A [PlatformSettings](https://reticulardev.github.io/pysidex/reference_PlatformSettings/) 
object that brings information from the user's platform that is relevant to the 
composition of the window.

---

### reset_style

Signature: `reset_style() -> None`

Changes the window style back to the default.

## Signals

**resize_event_signal** = QtCore.Signal(object)

## Changes

A pre-configured *central widget* already exists and is a central part of the 
**QApplicationWindow**. You will get it for use through the `central_widget` 
method.

The `set_object_name` method does not work for the **QApplicationWindow** nor 
for its *central widget*. To change the [**QSS** style](https://reticulardev.github.io/pysidex/styling/) 
you need to use the base name "QApplicationWindow{...}".

The `event_filter` method has been rewritten, so it is not currently 
accessible. So consider using specific event methods like `enter_event` and 
`leave_vent`.

## Examples

A **highly discouraged** minimal example would be:

```python
app = QtWidgets.QApplication(sys.argv)
window = QtWidgetsX.QApplicationWindow()
window.show()
sys.exit(app.exec())
```

This would give you a little window that can be resized in any direction. 
However, there is no button to close the application and, depending on your 
platform, it may be difficult to close the application:

![Image](img/min_window.png "screenshot")

A better minimal example in this situation includes adding a headerbar to 
access the window control buttons:

```python
class Window(QtWidgetsX.QApplicationWindow):
    def __init__(self):
        super().__init__()

        self.main_layout = QtWidgets.QVBoxLayout()
        self.central_widget().set_layout(self.main_layout)

        self.main_layout.set_contents_margins(0, 0, 0, 0)
        self.main_layout.set_alignment(QtCore.Qt.AlignTop)

        self.headerbar = QtWidgetsX.QHeaderBar(self)
        self.main_layout.add_widget(self.headerbar)


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
```

Note that a central widget with appropriate settings already exists. As it is 
already accessed directly, there is no need to create one.

```python
self.central_widget().set_layout(self.main_layout)
```

Also note that the headerbar widget is independent, meaning you can place it 
wherever you want, which is why we aligned it at the top.

```python
self.main_layout.set_contents_margins(0, 0, 0, 0)
self.main_layout.set_alignment(QtCore.Qt.AlignTop)
```

This is the result:

![Image](img/better_min_window.png "screenshot")

### A more complete minimal example

In this example, we will add the `os` library to add an icon with a dynamic 
path. The icon, once configured in the window, will be automatically recognized 
by the header bar.

The title is not automatically recognized by the header bar as in the case of 
the icon, because not in all use cases a window needs to have the title 
displayed. In our case, if we want to see the window title, we need to manually 
redirect it to the header bar.

```python
#!/usr/bin/env python3
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySideX import QtWidgetsX
from __feature__ import snake_case

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class Window(QtWidgetsX.QApplicationWindow):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Window icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        window_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(window_icon)

        # Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.set_contents_margins(0, 0, 0, 0)
        self.main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.central_widget().set_layout(self.main_layout)

        # Headerbar
        self.headerbar = QtWidgetsX.QHeaderBar(self)
        self.main_layout.add_widget(self.headerbar)

        # Window title
        self.set_window_title('App title')
        self.headerbar.set_text(self.window_title())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
```

This is the result:

![Image](img/complete_min_window.png "screenshot")

### Using all concepts

We created the following example to use all the practical concepts in this 
window, such as using specific event methods instead of `event_filter`, and 
also using the "QApplicationWindow" **id** for [**QSS** style](https://reticulardev.github.io/pysidex/styling/).

```python
#!/usr/bin/env python3
import os
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySideX import QtWidgetsX
from __feature__ import snake_case

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SRC_DIR)


class Window(QtWidgetsX.QApplicationWindow):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Window icon
        icon_path = os.path.join(SRC_DIR, 'icon.svg')
        window_icon = QtGui.QIcon(QtGui.QPixmap(icon_path))
        self.set_window_icon(window_icon)

        # Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.set_contents_margins(0, 0, 0, 0)
        self.main_layout.set_alignment(QtCore.Qt.AlignTop)
        self.central_widget().set_layout(self.main_layout)

        # Headerbar
        self.headerbar = QtWidgetsX.QHeaderBar(self)
        self.main_layout.add_widget(self.headerbar)

        # Window title
        self.set_window_title('App title')
        self.headerbar.set_text(self.window_title())
    
    def enter_event(self, event: QtGui.QEnterEvent) -> None:
        self.set_attribute(QtCore.Qt.WA_TranslucentBackground)
        self.set_style_sheet(
            'QApplicationWindow {'
            '   background-color: rgba(65, 50, 75, 0.8);'
            '   border-radius: 10px;'
            '   border: 1px solid #555;}')

    def leave_event(self, event: QtGui.QEnterEvent) -> None:
        self.reset_style()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
```

This is the result:

![Image](img/ref_window_enter_and_leav_event.png "screenshot")
