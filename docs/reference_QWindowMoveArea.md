# QWindowMoveArea 

Inherits from [QFrame](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QFrame.html)

![Image](img/windowmovearea.png "screenshot")

## Overview

The area where you click and drag to move the window.

## Class signature

<pre><small>QWindowMoveArea(main_window: QApplicationWindow[QtWidgets, QMainWindow])</small></pre>

### Parameters

  - **main_window**: Type `QApplicationWindow` (QtWidgets.QMainWindow)

    Just pass `self` which indicates the top-level window instance:

    
    self.move_area = QHeaderBar(self)

## Signals

**mouse_press_event_signal** = QtCore.Signal(object)

**mouse_double_click_event_signal** = QtCore.Signal(object)

## Changes

Methods `mouse_press_event` and `mouse_double_click_event` have been rewritten, 
so use the `mouse_press_event_signal` and 
`mouse_double_click_event_signal` signals, or consider using event-specific 
methods such as `event_filter`.

## Example

```python
self.move_area = QHeaderBar(self)
self.layout.add_widget(self.move_area)
```
