# Quick start

Download and enter the project folder:

```commandline
git clone https://github.com/reticulardev/pysidex.git && cd pysidex/
```

Configure your virtual environment:

```commandline
python3 -m venv venv && . venv/bin/activate
```

Update pip and install dependencies:

```commandline
python -m pip install --upgrade pip && python -m pip install -r requirements.txt
```

Run the example to see it working:

```commandline
python src/demo.py
```

![Image](img/demo.png "screenshot")

## Imports

The project uses the `snake_case` feature to obtain idiomatic 
code, but does not use the `true_property` feature to avoid 
conflicts, as it does not yet work 100%.

After downloading and configuring, import the `sys` lib, 
import `PySide` to have access to all widgets, import 
`PySideX` to build the CSD window and finally configure the 
`snake_case` feature.

```python
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySideX import QtWidgetsX
from __feature__ import snake_case
```

## The minimal example

A **highly discouraged** minimal example would be:

```python
app = QtWidgets.QApplication(sys.argv)
window = QtWidgetsX.QMainFramelessWindow()
window.show()
sys.exit(app.exec())
```

This would give you a little window that can be resized in any 
direction. However, there is no button to close the application 
and, depending on your platform, it may be difficult to close 
the application:

![Image](img/min_window.png "screenshot")

A better minimal example in this situation includes adding a 
headerbar to access the window control buttons:

```python
class MainWindow(QtWidgetsX.QMainFramelessWindow):
    def __init__(self):
        super().__init__()
        
        self.main_layout = QtWidgets.QVBoxLayout()
        self.central_widget().set_layout(self.main_layout)
        
        self.main_layout.set_contents_margins(0, 0, 0, 0)
        self.main_layout.set_alignment(QtCore.Qt.AlignTop)

        self.headerbar = QtWidgetsX.QHeaderBar(self)
        self.main_layout.add_widget(self.headerbar)
        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

Note that a central widget with appropriate settings already exists. 
As it is already accessed directly, there is no need to create one.

```python
self.central_widget().set_layout(self.main_layout)
```

Also note that the headerbar widget is independent, meaning you can 
place it wherever you want, which is why we aligned it at the top.

```python
self.main_layout.set_contents_margins(0, 0, 0, 0)
self.main_layout.set_alignment(QtCore.Qt.AlignTop)
```

This is the result:

![Image](img/better_min_window_.png "screenshot")
