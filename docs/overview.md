# Overview

This is a work that uses Qt's Python bind to build a window with 
its own decoration (CSD), which eliminates the decoration of the 
operating system's window server (SSD).

Qt is an old and mature lib, but it was not originally designed 
to provide CSD support. Although it has added initial native support 
to CSD in recent years, it is still an incomplete work. Therefore, 
the PySideX and MPX projects are CSD implementations usable within 
the limits of Qt. So some hacks were made so that it was possible 
to have a usable window with desirable features such as a headerbar, 
customization of window borders, window control buttons with native 
platform integration, window resizing and movement.

## Targets
There are necessary and some desirable goals to be met, and as a 
parameter, we use the "[Client-Side Decorations Initiative](https://wiki.gnome.org/Initiatives/CSD)" of the Gnome project as a necessary goal 
to be met. This initiative contains a reasonable list of targets 
that we were fortunately able to achieve:

  * No title bar
  * Native-looking close/maximize/minimize icons
  * Respect the setting for showing/hiding minimize and maximize
  * Respect the setting for buttons to be on the left/right side of the window
  * Provide native system context menu on right click

## Limitations
Desirable goals to be achieved are part of some limitations.
Some of the Qt Company's difficulties in supporting CSD were 
addressed in article "[Custom client-side window decorations in Qt 5.15](https://www.qt.io/blog/custom-window-decorations)" 
on group blog.

One of the details that has not yet been resolved is maintaining 
the window shadow when using the 'FramelessWindowHint' flag, which 
removes the server-side decorations. 

Another particularity to be resolved is the menu bar. As it is not 
rendered properly in the translucent part of the QMainWindow, which 
is modified to adapt the borders, it loses integration with global 
menus.

Another inconvenience is windows with a blurred background. It's 
not impossible or very complicated to blur the background of the 
QMainWindow, but we had some pertinent problems with the window 
mask. It is not always able to remove the effect outside the 
rounded edges, leaving those little points slightly visible.

## Mitigation
