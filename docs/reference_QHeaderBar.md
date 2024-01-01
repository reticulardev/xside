# QHeaderBar 

Inherits from [QFrame](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QFrame.html)

![Image](img/headerbar.png "screenshot")

## Overview

The main control area of an application window, where there are close, maximize 
and minimize buttons, along with a movement area and the application icon.

It's a regular widget and can be aligned wherever you want, not just at the top 
of the window, but also in other places like the middle or bottom if you're a 
psychopath.

## Class signature

QHeaderBar(main_window: QApplicationWindow[QtWidgets, QMainWindow])

### Parameters

  - **main_window**: Type = `QApplicationWindow`[QtWidgets, QMainWindow]

    Just pass `self` which indicates the top-level window instance.

    
    self.headerbar = QHeaderBar(self)
    

## Class methods

Only new ones. See the
[**QFrame** documentation](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QFrame.html) 
for more.

- [add_widget_to_left](#add_widget_to_left)

- [add_widget_to_right](#add_widget_to_right)

- [lef_layout](#lef_layout)

- [right_layout](#right_layout)

- [set_left_control_buttons_visible](#set_left_control_buttons_visible)

- [set_right_control_buttons_visible](#set_right_control_buttons_visible)

- [set_text](#set_text)

- [text](#text)

### add_widget_to_left

Signature: `add_widget_to_left(widget: QtWidgets.QWidget) -> None`

...

---

### add_widget_to_right

Signature: `add_widget_to_right(widget: QtWidgets.QWidget) -> None`

...

---

### lef_layout

Signature: `lef_layout() -> QtWidgets.QHBoxLayout`

...

---

### right_layout

Signature: `right_layout() -> QtWidgets.QHBoxLayout`

...

---

### set_left_control_buttons_visible

Signature: `set_left_control_buttons_visible(visible: bool) -> None`

...

---

### set_right_control_buttons_visible

Signature: `set_right_control_buttons_visible(visible: bool) -> None`

...

---

### set_text

Signature: `set_text(text: str) -> None`

...

---

### text

Signature: `text() -> str`

...

---

## Changes

The `resize_event` method needed, at least temporarily, to be 
rewritten and is therefore not currently accessible. So consider using specific 
event methods like `event_filter`.

## Examples

...

