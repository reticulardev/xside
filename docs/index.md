### PySideX

PySide eXtras is a collection of extra resources for pyside with a focus on CSD ([Client-side decoration](https://en.wikipedia.org/wiki/Client-side_decoration)). It is the basis of the ([MPX](https://github.com/reticulardev/mpx)) project.

Conforms to the list of objectives specified in the "[Client-Side Decorations Initiative](https://wiki.gnome.org/Initiatives/CSD)" of the Gnome project.

![Image](img/screen.png "screenshot")

Extra widgets:

 * **QMainFramelessWindow**:
A CSD (Client-side decoration) window without server-side decoration 
(SSD). It is resizable in all corners and has a shadow (optional).

 * **QControlButton**: 
A Window control button. It could be the "close", "minimize" or 
"maximize" button.

 * **QWindowControlButtons**: 
The buttons to "close", "maximize" and "minimize" the window.

 * **QWindowMoveArea**: 
An area to drag the window. It is also possible to maximize and 
demaximize the window by double-clicking.

 * **QHeaderBar**: 
A ready-made header bar, with drag area (QWindowMoveArea), control 
buttons (QWindowControlButtons), the window icon and methods for 
adding widgets to its right and left. When possible, the control 
buttons respect the positioning settings, the global menu and the 
system theme. They also behave desirably when the window is full 
screen.

*The theme is still the PySide default