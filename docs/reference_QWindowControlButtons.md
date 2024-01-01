# QWindowControlButtons 

Inherits from [QFrame](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QFrame.html)

![Image](img/window_control_buttons.png "screenshot")

## Overview

Widget with window control buttons, to close, maximize and minimize.

## Class signature

<pre><small>QWindowControlButtons(
    main_window: QApplicationWindow[QtWidgets, QMainWindow],
    button_order: tuple = (0, 1, 2),
) -> None</small></pre>

### Parameters

  - **main_window**: Type `QApplicationWindow` (QtWidgets.QMainWindow)

    Just pass `self` which indicates the top-level window instance:

    
    self.control_buttons = QWindowControlButtons(self, (0, 1, 2))
    
  - **button_order**: Type `tuple`. Default is `(0, 1, 2)`
    In the button order parameter, each number represents a type of button: `0` 
    is the **minimize** button, `1` is the **maximize** button, `2` is the 
    **close** button and `3` is **window icon**.

## Class methods

There are no methods!

## Example

```python
self.control_buttons = QWindowControlButtons(self, (0, 1, 2))
self.layout.add_widget(self.control_buttons)
```
