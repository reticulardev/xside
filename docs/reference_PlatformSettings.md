# PlatformSettings

User platform settings information.

## Overview

It is a utility that provides information about the user's platform that is 
relevant for customizing the application Window. This is information about the 
theme, operating system, order of the window control buttons, border shape and 
things like that.

## Class signature

<pre><small>PlatformSettings(platform_integration: bool = True)</small></pre>

### Parameters

  - **platform_integration**: Type `bool`. Default is `True`

    Using `False` will not bring platform information, it will bring library 
    defaults. Using `True` will obtain platform information, only when possible 
    and if it is supported.

## Properties

- [desktop_environment](#desktop_environment)

- [operational_system](#operational_system)

### desktop_environment

Signature: `desktop_environment() -> DesktopEnvironment[Enum]`

So far supports KDE, GNOME, CINNAMON, XFCE and UNKNOWN

```python
DesktopEnvironment = Enum(
    'DesktopEnvironment', ['UNKNOWN', 'KDE', 'GNOME', 'CINNAMON', 'XFCE'])
```

---

### operational_system

Signature: `operational_system() -> OperationalSystem[Enum]`

So far supports LINUX, BSD, MAC, WINDOWS and UNKNOWN

```python
OperationalSystem = Enum(
    'OperationalSystem', ['UNKNOWN', 'LINUX', 'BSD', 'MAC', 'WINDOWS'])
```

## Methods

- [window_control_button_style](#window_control_button_style)

- [window_control_button_order](#window_control_button_order)

- [window_border_radius](#window_border_radius)

- [window_use_global_menu](#window_use_global_menu)

### window_control_button_style

Signature: `window_control_button_style(window_is_dark: bool, button_name: str, button_state: str) -> str | None`

Parameter `window_is_dark`: `bool`, Inform if the Window is dark

Parameter `button_name`: `str`, Inform if is 'minimize', 'maximize', 'restore' or 'close'

Parameter `button_state`: `str`, Inform if is 'normal', 'hover', 'inactive'

Returns a `str` with the button's **QSS** style or `None`

---

### window_control_button_order

Signature: `window_control_button_order() -> tuple | None`

A `int` tuple with the order of the buttons: (0, 1, 2)

---

### window_border_radius

Signature: `window_border_radius() -> tuple | None`

A `int` tuple with the radius of the 4 corners of the window: (5, 5, 5, 5)

---

### window_use_global_menu

Signature: `window_use_global_menu() -> bool`

`True` if the platform is using a global menu, otherwise returns `False`

---
