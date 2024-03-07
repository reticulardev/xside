#!/usr/bin/env python3
import logging
import os

from PySide6 import QtWidgets
from __feature__ import snake_case


class ContextLabel(QtWidgets.QLabel):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """..."""
