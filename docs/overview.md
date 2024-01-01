# Overview

This is a work that uses Qt's Python bind to build a window with its own 
decoration ([CSD](https://en.wikipedia.org/wiki/Client-side_decoration)), which eliminates the decoration of the operating system's 
window server ([SSD](https://en.wikipedia.org/wiki/Window_(computing)#Window_decoration)).

Qt is an old and mature lib, but it was not originally designed to provide CSD 
support. Although it has added initial native support to CSD in recent years, 
it is still an incomplete work. Therefore, the **PySideX** and [MPX](https://github.com/reticulardev/mpx) projects are CSD 
implementations usable within the limits of Qt. So some hacks were made so that 
it was possible to have a usable window with desirable features such as a 
headerbar, customization of window borders, window control buttons with native 
platform integration, window resizing and movement.

## Targets

There are necessary and some desirable goals to be met, and as a parameter, we 
use the "[Client-Side Decorations Initiative](https://wiki.gnome.org/Initiatives/CSD)" 
of the Gnome project as a necessary goal to be met. This initiative contains a 
list of reasonable goals to achieve:

  * No title bar
  * Native-looking close/maximize/minimize icons
  * Respect the setting for showing/hiding minimize and maximize
  * Respect the setting for buttons to be on the left/right side of the window
  * Provide native system context menu on right click

## Limitations and mitigations

Desirable goals to be achieved are part of some limitations. Some of the Qt 
Company's difficulties in supporting CSD were addressed in article 
"[Custom client-side window decorations in Qt 5.15](https://www.qt.io/blog/custom-window-decorations)" 
on group blog.

One of the details that has not yet been resolved is maintaining the window 
shadow when using the 'FramelessWindowHint' flag, which removes the server-side 
decorations. We could request 1 edge pixel from the window server, but this 
would prevent us from customizing the corners in a satisfactory way. When 
remembering that customizing the edges is the biggest gain in CSD, messing it 
up would destroy the most significant part of the project. Therefore, we chose 
to provide a non-native shadow using Qt effects, which can be easily 
manipulated or removed, and also easy to change when an update to this feature 
becomes available.

Another particularity to be resolved is the menu bar. As it is not rendered 
properly in the translucent part of the QMainWindow, which is modified to 
adapt the borders, it loses integration with global menus. The interesting 
thing here is that the CSD was designed for "UX/UI design" which does not match 
menu bars, as many have already observed. The reason for this, is because they 
are very large and disorganized. In modern programs they are already disabled, 
or sometimes with access shortcut. An alternative UX design approach is 
recommended in this case.

Another inconvenience is windows with a blurred background. It's not impossible 
or very complicated to blur the background of the QMainWindow, but we had some 
pertinent problems with the window mask. It is not always able to remove the 
effect outside the rounded edges, leaving those little points slightly visible. 
Believe me, even those who don't have "OCD" start to acquire it after looking 
at it for a while. Therefore, as providing windows with blurred backgrounds by 
default is not a priority, this has temporarily fallen out of the plans.

## Maintainability

The extra widgets are designed to be limited to the minimum possible, just to 
provide a CSD Window. This means that all graphics library support officially 
remains with the Qt Company. This decision makes the project small and gives us 
the chance to keep it actively updated with the latest stable versions of 
Pyside. It also provides the security of being able to continue officially 
using the robust original Qt.

## Code style

Qt originally uses the camelCase code style and this is reflected in PySide 
which also uses it by default. In an effort to make Python code idiomatic, the 
snake_case and true_property features were introduced.

Find out more about the feature in the official [Pyside documentation](https://doc.qt.io/qtforpython-6/considerations.html#features)

In our tests, the true_property feature didn't work well in every way, but the 
snake_case style was maintained. Anyone who has worked with PyGObject, the GTK 
bind to Python, will feel right at home.

This is a project based on QtWidgets and for now there are no plans to support 
QML.

## Conclusion

As Qt Company progresses with CSD support, this project will be improved. And 
fortunately, it is now possible to obtain a usable and satisfactory result. 
The Widgets that were created are very flexible and easy to implement.
